# coding: utf-8

"""
Implementation of a file interface using GFAL.
"""

__all__ = ["GFALFileInterface"]


import os
import sys
import contextlib
import stat as _stat

import six

from law.config import Config
from law.target.file import has_scheme, get_scheme
from law.target.remote.interface import RemoteFileInterface, RetryException
from law.logger import get_logger


logger = get_logger(__name__)


# try to import gfal2
try:
    import gfal2

    HAS_GFAL2 = True

except (ImportError, TypeError):
    HAS_GFAL2 = False

    class GFAL2Dummy(object):

        def __getattr__(self, attr):
            raise Exception("trying to access 'gfal2.{}', but gfal2 is not installed".format(attr))

    gfal2 = GFAL2Dummy()


class GFALFileInterface(RemoteFileInterface):

    @classmethod
    def parse_config(cls, section, config=None, overwrite=False):
        config = super(GFALFileInterface, cls).parse_config(section, config=config,
            overwrite=overwrite)

        cfg = Config.instance()

        # helper to add a config value if it exists, extracted with a config parser method
        def add(option, func, postfix="gfal_", _config=config):
            if option not in config or overwrite:
                _config[option] = func(section, postfix + option)

        # use atomic contexts per operation
        add("atomic_contexts", cfg.get_expanded_bool)

        # transfer config
        config.setdefault("transfer_config", {})
        transfer_specs = [
            ("timeout", cfg.get_expanded_int),
            ("checksum_check", cfg.get_expanded_bool),
            ("nbstreams", cfg.get_expanded_int),
            ("overwrite", cfg.get_expanded_bool),
            ("create_parent", cfg.get_expanded_bool),
            ("strict_copy", cfg.get_expanded_bool),
        ]
        for name, func in transfer_specs:
            add(name, func, "gfal_transfer_", config["transfer_config"])

        return config

    def __init__(self, atomic_contexts=False, gfal_options=None, transfer_config=None, **kwargs):
        super(GFALFileInterface, self).__init__(**kwargs)

        # cache for gfal context objects and transfer parameters per pid for thread safety
        self._contexts = {}
        self._transfer_parameters = {}

        # store gfal options and transfer configs
        self.gfal_options = gfal_options or {}
        self.transfer_config = transfer_config or {}

        # other configs
        self.atomic_contexts = atomic_contexts

    def sanitize_path(self, p):
        # in python 2, the gfal2-bindings do not support unicode but expect strings
        return str(p) if isinstance(p, six.string_types) else p

    @contextlib.contextmanager
    def context(self):
        # context objects are stored per pid, so create one if it does not exist yet
        pid = os.getpid()

        if pid not in self._contexts:
            self._contexts[pid] = ctx = gfal2.creat_context()
            for _type, args_list in six.iteritems(self.gfal_options):
                for args in args_list:
                    getattr(ctx, "set_opt_" + _type)(*args)

        # yield and optionally close it which frees potentially open connections
        try:
            yield self._contexts[pid]
        finally:
            if self.atomic_contexts and pid in self._contexts:
                del self._contexts[pid]

    @contextlib.contextmanager
    def transfer_parameters(self, ctx):
        pid = os.getpid()

        if pid not in self._transfer_parameters:
            self._transfer_parameters[pid] = ctx.transfer_parameters()
            for key, value in six.iteritems(self.transfer_config):
                setattr(self._transfer_parameters[pid], key, value)

        try:
            yield self._transfer_parameters[pid]
        finally:
            if self.atomic_contexts and pid in self._transfer_parameters:
                del self._transfer_parameters[pid]

    def exists(self, path, stat=False, base=None, **kwargs):
        uri = self.uri(path, base_name="stat" if stat else ("exists", "stat"), base=base)
        with self.context() as ctx:
            try:
                logger.debug("invoking gfal2 exists({})".format(uri))
                rstat = ctx.stat(uri)
                return rstat if stat else True
            except gfal2.GError:
                return None if stat else False

    @RemoteFileInterface.retry(uri_base_name="stat")
    def stat(self, path, base=None, **kwargs):
        uri = self.uri(path, base_name="stat", base=base)
        with self.context() as ctx:
            try:
                logger.debug("invoking gfal2 stat({})".format(uri))
                return ctx.stat(uri)

            except gfal2.GError:
                raise RetryException()

    def isdir(self, path, stat=None, base=None, **kwargs):
        if not stat:
            stat = self.exists(path, stat=True, base=base)

        if not stat:
            return False

        # some file protocols do not return standard st_mode values in stat requests,
        # e.g. srm returns file type bits 0o50000 for directories instead of 0o40000,
        # these differences are rather distinct and can be taken into account here,
        # see http://man7.org/linux/man-pages/man7/inode.7.html for info on st_mode values
        return _stat.S_ISDIR(stat.st_mode) or _stat.S_IFMT(stat.st_mode) == 0o50000

    def isfile(self, path, stat=None, base=None, **kwargs):
        if not stat:
            stat = self.exists(path, stat=True, base=base)

        if not stat:
            return False

        return not self.isdir(path, stat=stat, base=base)

    @RemoteFileInterface.retry(uri_base_name="chmod")
    def chmod(self, path, perm, base=None, silent=False, **kwargs):
        if perm is None:
            return True

        uri = self.uri(path, base_name="chmod", base=base)
        with self.context() as ctx:
            try:
                logger.debug("invoking gfal2 chmod({}, {})".format(uri, perm))
                ctx.chmod(uri, perm)
                return True

            except gfal2.GError:
                e = GFALError_chmod(uri)
                # check if the operation should be retried, can fail silently, or raised immediately
                if e.reason == e.UNKNOWN:
                    raise e
                if e.reason in (e.NOT_FOUND, e.NOT_SUPPORTED) and silent:
                    return False
                e.reraise()

    @RemoteFileInterface.retry(uri_base_name="unlink")
    def unlink(self, path, base=None, silent=True, **kwargs):
        uri = self.uri(path, base_name="unlink", base=base)
        with self.context() as ctx:
            try:
                logger.debug("invoking gfal2 unlink({})".format(uri))
                ctx.unlink(uri)
                return True

            except gfal2.GError:
                e = GFALError_unlink(uri)
                # check if the operation should be retried, can fail silently, or raised immediately
                if e.reason == e.UNKNOWN:
                    raise e
                if e.reason == e.NOT_FOUND and silent:
                    return False
                e.reraise()

    @RemoteFileInterface.retry(uri_base_name="rmdir")
    def rmdir(self, path, base=None, silent=True, **kwargs):
        uri = self.uri(path, base_name="rmdir", base=base)
        with self.context() as ctx:
            try:
                logger.debug("invoking gfal2 rmdir({})".format(uri))
                ctx.rmdir(uri)
                return True

            except gfal2.GError:
                e = GFALError_rmdir(uri)
                # check if the operation should be retried, can fail silently, or raised immediately
                if e.reason == e.UNKNOWN:
                    raise e
                if e.reason == e.NOT_FOUND and silent:
                    return False
                e.reraise()

    @RemoteFileInterface.retry(uri_base_name="unlink")
    def remove(self, path, base=None, silent=True, **kwargs):
        """
        Recursive removal is potentially expensive in terms of remote file operations, so this
        method is designed to reduce them as much as possible.
        """
        # most common use case is file removal, so try this first and in case there is an error
        # interpret its message to get more info on the object without further operations
        uri = self.uri(path, base_name="unlink", base=base)
        with self.context() as ctx:
            try:
                logger.debug("invoking gfal2 unlink({})".format(uri))
                ctx.unlink(uri)
                return True

            except gfal2.GError:
                e = GFALError_unlink(uri)
                # handle all cases, except when uri is a directory
                if e.reason != e.IS_DIRECTORY:
                    if e.reason == e.UNKNOWN:
                        raise e
                    if e.reason == e.NOT_FOUND and silent:
                        return False
                    e.reraise()

        # at this point, we are dealing with a directory so try to delete it right away
        uri = self.uri(path, base_name="rmdir", base=base)
        with self.context() as ctx:
            try:
                logger.debug("invoking gfal2 rmdir({})".format(uri))
                ctx.rmdir(uri)
                return True

            except gfal2.GError:
                e = GFALError_rmdir(uri)
                # handle all cases, except when the directory is not empty
                if e.reason != e.NOT_EMPTY:
                    if e.reason == e.UNKNOWN:
                        raise e
                    if e.reason == e.NOT_FOUND and silent:
                        return False
                    e.reraise()

        # the directory is not empty, so there is no other way than deleting contents recursively
        # first, and then removing the directory itself
        path = str(path)
        for elem in self.listdir(path, base=base, retries=0):
            self.remove(os.path.join(path, elem), base=base, silent=silent, retries=0)

        return self.rmdir(path, base=base, silent=silent, retries=0)

    @RemoteFileInterface.retry(uri_base_name="mkdir")
    def mkdir(self, path, perm, base=None, silent=True, **kwargs):
        uri = self.uri(path, base_name="mkdir", base=base)
        with self.context() as ctx:
            try:
                logger.debug("invoking gfal2 mkdir({}, {})".format(uri, perm))
                ctx.mkdir(uri, perm)
                return True

            except gfal2.GError:
                e = GFALError_mkdir(uri)
                # check if the operation should be retried, can fail silently, or raised immediately
                if e.reason == e.UNKNOWN:
                    raise e
                if e.reason == e.EXISTS and silent:
                    # fail silently only when uri is really a dictionary
                    if self.isdir(path, base=base):
                        return False
                e.reraise()

    @RemoteFileInterface.retry(uri_base_name=["mkdir_rec", "mkdir"])
    def mkdir_rec(self, path, perm, base=None, silent=True, **kwargs):
        uri = self.uri(path, base_name="mkdir", base=base)
        with self.context() as ctx:
            try:
                logger.debug("invoking gfal2 mkdir_rec({}, {})".format(uri, perm))
                ctx.mkdir_rec(uri, perm)
                return True

            except gfal2.GError:
                e = GFALError_mkdir(uri)
                # check if the operation should be retried, can fail silently, or raised immediately
                if e.reason == e.UNKNOWN:
                    raise e
                if e.reason == e.EXISTS and silent:
                    # fail silently only when uri is really a dictionary
                    if self.isdir(path, base=base):
                        return False
                e.reraise()

    @RemoteFileInterface.retry(uri_base_name="listdir")
    def listdir(self, path, base=None, **kwargs):
        uri = self.uri(path, base_name="listdir", base=base)
        with self.context() as ctx:
            try:
                logger.debug("invoking gfal2 listdir({})".format(uri))
                return ctx.listdir(uri)

            except gfal2.GError:
                e = GFALError_listdir(uri)
                # some protocols throw an error upon listdir on empty directories
                if e.EMPTY:
                    return []
                e.reraise()

    @RemoteFileInterface.retry(uri_base_name="filecopy")
    def filecopy(self, src, dst, base=None, **kwargs):
        if has_scheme(src):
            src_uri = self.sanitize_path(src)
        else:
            src_uri = self.uri(src, base_name="filecopy", base=base)

        if has_scheme(dst):
            dst_uri = self.sanitize_path(dst)
        else:
            dst_uri = self.uri(dst, base_name="filecopy", base=base)

        with self.context() as ctx, self.transfer_parameters(ctx) as params:
            try:
                logger.debug("invoking gfal2 filecopy({}, {})".format(src_uri, dst_uri))
                ctx.filecopy(params, src_uri, dst_uri)

            except gfal2.GError:
                e = GFALError_filecopy(src_uri, dst_uri)
                # check if the operation should be retried or raised immediately
                if e.reason == e.UNKNOWN:
                    raise e
                e.reraise()

        return src_uri, dst_uri


class GFALOperationError(RetryException):

    UNKNOWN = "unknown reason"

    def __init__(self, uri, exc=None):
        # store uri and scheme
        self.uri = str(uri)
        self.scheme = get_scheme(uri)

        # get the original error objects and find the error reason
        exc = exc or sys.exc_info()
        self.reason = self._get_reason(str(exc[1]), self.uri, self.scheme)

        # add the error reason to the message
        msg = "{} ({}: {})".format(exc[1], self.__class__.__name__, self.reason)

        super(GFALOperationError, self).__init__(msg=msg, exc=exc)

    @classmethod
    def _get_reason(cls, msg, uri, scheme):
        raise NotImplementedError()


class GFALError_chmod(GFALOperationError):

    NOT_FOUND = "no such file or directory"
    NOT_SUPPORTED = "chmod operation not supported"

    @classmethod
    def _get_reason(cls, msg, uri, scheme):
        lmsg = msg.lower()
        if scheme == "root":
            if "no such file or directory" in lmsg:
                return cls.NOT_FOUND

        elif scheme == "gsiftp":
            if "no such file or directory" in lmsg:
                return cls.NOT_FOUND

        elif scheme == "srm":
            if "no such file or directory" in lmsg:
                return cls.NOT_FOUND
            if "operation not supported" in lmsg:
                return cls.NOT_SUPPORTED

        elif scheme in ("dav", "davs"):
            if "protocol not supported" in lmsg:
                return cls.NOT_SUPPORTED

        elif scheme == "dropbox":
            if "protocol not supported" in lmsg:
                return cls.NOT_SUPPORTED

        else:
            logger.warning("scheme '{}' not known to {}, cannot parse '{}'".format(
                scheme, cls.__name__, msg))

        return cls.UNKNOWN


class GFALError_unlink(GFALOperationError):

    NOT_FOUND = "target not found"
    IS_DIRECTORY = "target is a directory"

    @classmethod
    def _get_reason(cls, msg, uri, scheme):
        lmsg = msg.lower()
        if scheme == "root":
            if "no such file or directory" in lmsg:
                return cls.NOT_FOUND
            if "is a directory" in lmsg:
                return cls.IS_DIRECTORY

        elif scheme == "gsiftp":
            if "no such file or directory" in lmsg:
                return cls.NOT_FOUND
            if "not a file" in lmsg:
                return cls.IS_DIRECTORY

        elif scheme == "srm":
            if "no such file" in lmsg:
                return cls.NOT_FOUND
            if "not a file" in lmsg:
                return cls.IS_DIRECTORY

        elif scheme in ("dav", "davs"):
            if "file not found" in lmsg:
                return cls.NOT_FOUND
            if "is a directory" in lmsg:
                return cls.IS_DIRECTORY

        elif scheme == "dropbox":
            if "not_found" in lmsg:
                return cls.NOT_FOUND

        else:
            logger.warning("scheme '{}' not known to {}, cannot parse '{}'".format(
                scheme, cls.__name__, msg))

        return cls.UNKNOWN


class GFALError_rmdir(GFALOperationError):

    NOT_FOUND = "target not found"
    IS_FILE = "target is a file"
    NOT_EMPTY = "directory is not empty"

    @classmethod
    def _get_reason(cls, msg, uri, scheme):
        lmsg = msg.lower()
        if scheme == "root":
            if "no such file or directory" in lmsg:
                return cls.NOT_FOUND
            if "not a directory" in lmsg:
                return cls.IS_FILE
            if "no such device" in lmsg:
                # cryptic message for non-empty directory
                return cls.NOT_EMPTY

        elif scheme == "gsiftp":
            if "no such file or directory" in lmsg:
                return cls.NOT_FOUND
            if "not a directory" in lmsg:
                return cls.IS_FILE
            if "directory is not empty" in lmsg:
                return cls.NOT_EMPTY

        elif scheme == "srm":
            if "no such file or directory" in lmsg:
                return cls.NOT_FOUND
            if "this file is not a directory" in lmsg:
                return cls.IS_FILE
            if "directory not empty" in lmsg:
                return cls.NOT_EMPTY

        elif scheme in ("dav", "davs"):
            if "file not found" in lmsg:
                return cls.NOT_FOUND

        elif scheme == "dropbox":
            if "not_found" in lmsg:
                return cls.NOT_FOUND

        else:
            logger.warning("scheme '{}' not known to {}, cannot parse '{}'".format(
                scheme, cls.__name__, msg))

        return cls.UNKNOWN


class GFALError_mkdir(GFALOperationError):

    EXISTS = "target already exists"

    @classmethod
    def _get_reason(cls, msg, uri, scheme):
        lmsg = msg.lower()
        if scheme == "root":
            if "file exists" in lmsg:
                return cls.EXISTS

        elif scheme == "gsiftp":
            if "directory already exists" in lmsg:
                return cls.EXISTS

        elif scheme == "srm":
            if "directory already exist" in lmsg:
                return cls.EXISTS

        elif scheme == "dropbox":
            if "the directory already exists" in lmsg:
                return cls.EXISTS

        else:
            logger.warning("scheme '{}' not known to {}, cannot parse '{}'".format(
                scheme, cls.__name__, msg))

        return cls.UNKNOWN


class GFALError_listdir(GFALOperationError):

    EMPTY = "directory is empty"

    @classmethod
    def _get_reason(cls, msg, uri, scheme):
        lmsg = msg.lower()
        if scheme == "root":
            # xrootd throws an expcetion when a directory is empty
            if lmsg.strip().endswith("invalid response (unknown error 303)"):
                return cls.EMPTY

        return cls.UNKNOWN


class GFALError_filecopy(GFALOperationError):

    SRC_NOT_FOUND = "source not found"
    DST_EXISTS = "target already exists"

    def __init__(self, src_uri, dst_uri, exc=None):
        # store uri and scheme
        self.src_uri = str(src_uri)
        self.dst_uri = str(dst_uri)
        self.src_scheme = get_scheme(src_uri)
        self.dst_scheme = get_scheme(dst_uri)

        # get the original error objects and find the error reason
        exc = exc or sys.exc_info()
        self.reason = self._get_reason(str(exc[1]), self.src_uri, self.dst_uri, self.src_scheme,
            self.dst_scheme)

        # add the error reason to the message
        msg = "{} ({}: {})".format(exc[1], self.__class__.__name__, self.reason)

        # bypass the GFALOperationError init
        RetryException.__init__(self, msg=msg, exc=exc)

    @classmethod
    def _get_reason(cls, msg, src_uri, dst_uri, src_scheme, dst_scheme):
        # in gfal, error messages on missing source files or existing target files depend on both
        # source and destination protocols, so all cases need to be handled separately
        lmsg = msg.lower()
        if (src_scheme, dst_scheme) == ("file", "file"):
            if "could not open source" in lmsg:
                return cls.SRC_NOT_FOUND
            if "the file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("file", "root"):
            if "no such file or directory (source)" in lmsg:
                return cls.SRC_NOT_FOUND
            if "file exists (destination)" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("file", "gsiftp"):
            if "local system call no such file or directory" in lmsg:
                return cls.SRC_NOT_FOUND
            if "file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("file", "srm"):
            if "local system call no such file or directory" in lmsg:
                return cls.SRC_NOT_FOUND
            if "file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) in (("file", "dav"), ("file", "davs")):
            if "local system call no such file or directory" in lmsg:
                return cls.SRC_NOT_FOUND

        elif (src_scheme, dst_scheme) == ("file", "dropbox"):
            if "could not open source" in lmsg:
                return cls.SRC_NOT_FOUND
            if "the file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("gsiftp", "file"):
            if "no such file or directory on url" in lmsg:
                return cls.SRC_NOT_FOUND
            if "the file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("gsiftp", "gsiftp"):
            if "file not found" in lmsg:
                return cls.SRC_NOT_FOUND
            if "destination already exist" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) in (("gsiftp", "dav"), ("gsiftp", "davs")):
            if "is a directory" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("srm", "file"):
            if "no such file" in lmsg:
                return cls.SRC_NOT_FOUND
            if "the file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("srm", "root"):
            if "no such file" in lmsg:
                return cls.SRC_NOT_FOUND
            if "the file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("srm", "srm"):
            if "no such file" in lmsg:
                return cls.SRC_NOT_FOUND
            if "file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) in (("srm", "dav"), ("srm", "davs")):
            if "no such file" in lmsg:
                return cls.SRC_NOT_FOUND
            if "file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("root", "file"):
            if "no such file or directory" in lmsg:
                return cls.SRC_NOT_FOUND
            if "file exists (destination)" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("root", "srm"):
            if "no such file or directory" in lmsg:
                return cls.SRC_NOT_FOUND
            if "file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("root", "root"):
            if "destination does not support delegation." in lmsg:
                return cls.SRC_NOT_FOUND
            if "file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) in (("root", "dav"), ("root", "davs")):
            if "failed to open file (block device required)" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) in (("dav", "file"), ("davs", "file")):
            if "file not found" in lmsg:
                return cls.SRC_NOT_FOUND

        elif (src_scheme, dst_scheme) in (("dav", "gsiftp"), ("davs", "gsiftp")):
            if "file not found" in lmsg:
                return cls.SRC_NOT_FOUND
            if "not a file" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) in (("dav", "root"), ("davs", "root")):
            # it appears that there is a bug in gfal when copying via davix to xrootd in that
            # the full dst path is repeated, e.g. "root://url.tld:1090/pnfs/.../root://url..."
            # which causes weird behavior, and as long as this issue persists, there should be no
            # error parsing in law
            pass

        elif (src_scheme, dst_scheme) in (("dav", "srm"), ("davs", "srm")):
            # same issue as for davix -> xrootd, wait until this is resolved
            pass

        elif (src_scheme, dst_scheme) == ("dropbox", "file"):
            if "could not open source" in lmsg:
                return cls.SRC_NOT_FOUND
            if "the file exists" in lmsg:
                return cls.DST_EXISTS

        elif (src_scheme, dst_scheme) == ("dropbox", "dropbox"):
            if "could not open source" in lmsg:
                return cls.SRC_NOT_FOUND
            if "the file exists" in lmsg:
                return cls.DST_EXISTS

        else:
            logger.warning("combination of source scheme '{}' and target scheme '{}' not known to "
                "{}, cannot parse '{}'".format(src_scheme, dst_scheme, cls.__name__, msg))

        return cls.UNKNOWN
