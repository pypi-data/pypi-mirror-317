# coding: utf-8

"""
Custom luigi file system and target objects.
"""

__all__ = [
    "FileSystem", "FileSystemTarget", "FileSystemFileTarget", "FileSystemDirectoryTarget",
    "get_path", "get_scheme", "has_scheme", "add_scheme", "remove_scheme", "localize_file_targets",
]


import os
import sys
import re
from abc import abstractmethod, abstractproperty
from functools import partial
from contextlib import contextmanager

from law.config import Config
import law.target.luigi_shims as shims
from law.target.base import Target
from law.util import map_struct, create_random_string, human_bytes, no_value


class FileSystem(shims.FileSystem):

    @classmethod
    def parse_config(cls, section, config=None, overwrite=False):
        # reads a law config section and returns parsed file system configs
        cfg = Config.instance()

        if config is None:
            config = {}

        # helper to add a config value if it exists, extracted with a config parser method
        def add(option, func):
            if option not in config or overwrite:
                config[option] = func(section, option)

        # read configs
        int_or_none = partial(cfg.get_expanded_int, default=None)
        add("has_permissions", cfg.get_expanded_bool)
        add("default_file_perm", int_or_none)
        add("default_dir_perm", int_or_none)
        add("create_file_dir", cfg.get_expanded_bool)

        return config

    def __init__(self, name=None, has_permissions=True, default_file_perm=None,
            default_dir_perm=None, create_file_dir=True, **kwargs):
        super(FileSystem, self).__init__(**kwargs)

        self.name = name
        self.has_permissions = has_permissions
        self.default_file_perm = default_file_perm
        self.default_dir_perm = default_dir_perm
        self.create_file_dir = create_file_dir

    def __repr__(self):
        return "{}(name={}, {})".format(self.__class__.__name__, self.name, hex(id(self)))

    def dirname(self, path):
        return os.path.dirname(str(path)) if path != "/" else None

    def basename(self, path):
        return os.path.basename(str(path)) if path != "/" else "/"

    def ext(self, path, n=1):
        # split the path
        parts = self.basename(path).lstrip(".").split(".")

        # empty extension in the trivial case or use the last n parts except for the first one
        return "" if len(parts) == 1 else ".".join(parts[1:][min(-n, 0):])

    def _unscheme(self, path):
        return remove_scheme(path)

    @abstractproperty
    def default_instance(self):
        return

    @abstractmethod
    def abspath(self, path):
        return

    @abstractmethod
    def stat(self, path, **kwargs):
        return

    @abstractmethod
    def exists(self, path, stat=False, **kwargs):
        return

    @abstractmethod
    def isdir(self, path, **kwargs):
        return

    @abstractmethod
    def isfile(self, path, **kwargs):
        return

    @abstractmethod
    def chmod(self, path, perm, silent=True, **kwargs):
        return

    @abstractmethod
    def remove(self, path, recursive=True, silent=True, **kwargs):
        return

    @abstractmethod
    def mkdir(self, path, perm=None, recursive=True, silent=True, **kwargs):
        return

    @abstractmethod
    def listdir(self, path, pattern=None, type=None, **kwargs):
        return

    @abstractmethod
    def walk(self, path, max_depth=-1, **kwargs):
        return

    @abstractmethod
    def glob(self, pattern, cwd=None, **kwargs):
        return

    @abstractmethod
    def copy(self, src, dst, perm=None, dir_perm=None, **kwargs):
        return

    @abstractmethod
    def move(self, src, dst, perm=None, dir_perm=None, **kwargs):
        return

    @abstractmethod
    @contextmanager
    def open(self, path, mode, perm=None, dir_perm=None, **kwargs):
        return


class FileSystemTarget(Target, shims.FileSystemTarget):

    file_class = None
    directory_class = None

    def __init__(self, path, fs=None, **kwargs):
        if fs:
            self.fs = fs

        self._path = None
        self._unexpanded_path = None

        super(FileSystemTarget, self).__init__(path=path, **kwargs)

    def _repr_pairs(self, color=True):
        pairs = super(FileSystemTarget, self)._repr_pairs()

        # add the fs name
        if self.fs:
            pairs.append(("fs", self.fs.name))

        # add the path
        cfg = Config.instance()
        expand = cfg.get_expanded_bool("target", "expand_path_repr")
        pairs.append(("path", self.path if expand else self.unexpanded_path))

        # optionally add the file size
        if cfg.get_expanded_bool("target", "filesize_repr"):
            stat = self.exists(stat=True)
            pairs.append(("size", human_bytes(stat.st_size, fmt="{:.1f}{}") if stat else "-"))

        return pairs

    def _parent_args(self):
        return (), {}

    @property
    def unexpanded_path(self):
        return self._unexpanded_path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        path = self.fs._unscheme(str(path))
        self._unexpanded_path = path
        self._path = os.path.expandvars(os.path.expanduser(self._unexpanded_path))

    @property
    def dirname(self):
        return self.fs.dirname(self.path)

    @property
    def absdirname(self):
        return self.fs.dirname(self.abspath)

    @property
    def basename(self):
        return self.fs.basename(self.path)

    @property
    def unique_basename(self):
        return "{}_{}".format(hex(self.hash)[2:], self.basename)

    @property
    def parent(self):
        # get the dirname, but favor the unexpanded one to propagate variables
        dirname = self.dirname
        unexpanded_dirname = self.fs.dirname(self.unexpanded_path)
        expanded_dirname = os.path.expandvars(os.path.expanduser(unexpanded_dirname))
        if unexpanded_dirname and self.fs.abspath(dirname) == self.fs.abspath(expanded_dirname):
            dirname = unexpanded_dirname

        args, kwargs = self._parent_args()
        return self.directory_class(dirname, *args, **kwargs) if dirname is not None else None

    def sibling(self, *args, **kwargs):
        parent = self.parent
        if not parent:
            raise Exception("cannot determine parent of {!r}".format(self))

        return parent.child(*args, **kwargs)

    def stat(self, **kwargs):
        return self.fs.stat(self.path, **kwargs)

    def exists(self, **kwargs):
        return self.fs.exists(self.path, **kwargs)

    def remove(self, silent=True, **kwargs):
        self.fs.remove(self.path, silent=silent, **kwargs)

    def chmod(self, perm, silent=False, **kwargs):
        self.fs.chmod(self.path, perm, silent=silent, **kwargs)

    def makedirs(self, *args, **kwargs):
        parent = self.parent
        return None if parent is None else parent.touch(*args, **kwargs)

    @abstractproperty
    def fs(self):
        return

    @abstractproperty
    def abspath(self):
        return

    @abstractmethod
    def uri(self, return_all=False, scheme=True, **kwargs):
        return

    @abstractmethod
    def touch(self, perm=None, dir_perm=None, **kwargs):
        return

    @abstractmethod
    def copy_to(self, dst, perm=None, dir_perm=None, **kwargs):
        return

    @abstractmethod
    def copy_from(self, src, perm=None, dir_perm=None, **kwargs):
        return

    @abstractmethod
    def move_to(self, dst, perm=None, dir_perm=None, **kwargs):
        return

    @abstractmethod
    def move_from(self, src, perm=None, dir_perm=None, **kwargs):
        return

    @abstractmethod
    def copy_to_local(self, *args, **kwargs):
        return

    @abstractmethod
    def copy_from_local(self, *args, **kwargs):
        return

    @abstractmethod
    def move_to_local(self, *args, **kwargs):
        return

    @abstractmethod
    def move_from_local(self, *args, **kwargs):
        return

    @abstractmethod
    @contextmanager
    def localize(self, mode="r", perm=None, dir_perm=None, tmp_dir=None, **kwargs):
        return

    @abstractmethod
    def load(self, *args, **kwargs):
        return

    @abstractmethod
    def dump(self, *args, **kwargs):
        return


class FileSystemFileTarget(FileSystemTarget):

    type = "f"

    def ext(self, n=1):
        return self.fs.ext(self.path, n=n)

    def open(self, mode, **kwargs):
        return self.fs.open(self.path, mode, **kwargs)

    def touch(self, **kwargs):
        # create the file via open without content
        with self.open("w", **kwargs) as f:
            f.write("")

    def copy_to(self, dst, perm=None, dir_perm=None, **kwargs):
        # TODO: complain when dst not local? forward to copy_from request depending on protocol?
        return self.fs.copy(self.path, get_path(dst), perm=perm, dir_perm=dir_perm, **kwargs)

    def copy_from(self, src, perm=None, dir_perm=None, **kwargs):
        if isinstance(src, FileSystemFileTarget):
            return src.copy_to(self.abspath, perm=perm, dir_perm=dir_perm, **kwargs)

        # when src is a plain string, let the fs handle it
        # TODO: complain when src not local? forward to copy_to request depending on protocol?
        return self.fs.copy(get_path(src), self.path, perm=perm, dir_perm=dir_perm, **kwargs)

    def move_to(self, dst, perm=None, dir_perm=None, **kwargs):
        # TODO: complain when dst not local? forward to copy_from request depending on protocol?
        return self.fs.move(self.path, get_path(dst), perm=perm, dir_perm=dir_perm, **kwargs)

    def move_from(self, src, perm=None, dir_perm=None, **kwargs):
        if isinstance(src, FileSystemFileTarget):
            return src.move_to(self.abspath, perm=perm, dir_perm=dir_perm, **kwargs)

        # when src is a plain string, let the fs handle it
        # TODO: complain when src not local? forward to copy_to request depending on protocol?
        return self.fs.move(get_path(src), self.path, perm=perm, dir_perm=dir_perm, **kwargs)


class FileSystemDirectoryTarget(FileSystemTarget):

    type = "d"

    open = None

    def _child_args(self, path, type):
        return (), {}

    def child(self, path, type=None, mktemp_pattern=False, **kwargs):
        if type not in (None, "f", "d"):
            raise ValueError("invalid child type, use 'f' or 'd'")

        # apply mktemp's feature to replace at least three consecutive 'X' with random characters
        path = get_path(path)
        if mktemp_pattern and "XXX" in path:
            repl = lambda m: create_random_string(l=len(m.group(1)))
            path = re.sub("(X{3,})", repl, path)

        unexpanded_path = os.path.join(self.unexpanded_path, path)
        path = os.path.join(self.path, path)
        if type == "f":
            cls = self.file_class
        elif type == "d":
            cls = self.__class__
        elif not self.fs.exists(path):
            raise Exception("cannot guess type of non-existing path '{}'".format(path))
        elif self.fs.isdir(path):
            cls = self.__class__
            type = "d"
        else:
            cls = self.file_class
            type = "f"

        args, _kwargs = self._child_args(path, type)
        _kwargs.update(kwargs)

        return cls(unexpanded_path, *args, **_kwargs)

    def listdir(self, **kwargs):
        return self.fs.listdir(self.path, **kwargs)

    def glob(self, pattern, **kwargs):
        return self.fs.glob(pattern, cwd=self.path, **kwargs)

    def walk(self, **kwargs):
        return self.fs.walk(self.path, **kwargs)

    def touch(self, **kwargs):
        kwargs.setdefault("silent", True)
        self.fs.mkdir(self.path, **kwargs)

    def copy_to(self, dst, perm=None, dir_perm=None, **kwargs):
        # create the target dir
        _dst = get_path(dst)
        if isinstance(dst, FileSystemDirectoryTarget):
            dst.touch(perm=dir_perm, **kwargs)
        else:
            # TODO: complain when dst not local? forward to copy_from request depending on protocol?
            self.fs.mkdir(_dst, perm=dir_perm, **kwargs)

        # walk and operate recursively
        for path, dirs, files, _ in self.walk(max_depth=0, **kwargs):
            # recurse through directories and files
            for basenames, type_flag in [(dirs, "d"), [files, "f"]]:
                for basename in basenames:
                    t = self.child(basename, type=type_flag)
                    t.copy_to(os.path.join(_dst, basename), perm=perm, dir_perm=dir_perm, **kwargs)

        return _dst

    def copy_from(self, src, perm=None, dir_perm=None, **kwargs):
        # when src is a directory target itself, forward to its copy_to implementation as it might
        # be more performant to use its own directory walking
        if isinstance(src, FileSystemDirectoryTarget):
            return src.copy_to(self, perm=perm, dir_perm=dir_perm, **kwargs)

        # create the target dir
        self.touch(perm=dir_perm, **kwargs)

        # when src is a plain string, let the fs handle it
        # walk and operate recursively
        # TODO: complain when src not local? forward to copy_from request depending on protocol?
        _src = get_path(src)
        for path, dirs, files, _ in self.fs.walk(_src, max_depth=0, **kwargs):
            # recurse through directories and files
            for basenames, type_flag in [(dirs, "d"), [files, "f"]]:
                for basename in basenames:
                    t = self.child(basename, type=type_flag)
                    t.copy_from(os.path.join(_src, basename), perm=perm, dir_perm=dir_perm, **kwargs)

        return self.abspath

    def move_to(self, dst, perm=None, dir_perm=None, **kwargs):
        # create the target dir
        _dst = get_path(dst)
        if isinstance(dst, FileSystemDirectoryTarget):
            dst.touch(perm=dir_perm, **kwargs)
        else:
            # TODO: complain when dst not local? forward to copy_from request depending on protocol?
            self.fs.mkdir(_dst, perm=dir_perm, **kwargs)

        # walk and operate recursively
        for path, dirs, files, _ in self.walk(max_depth=0, **kwargs):
            # recurse through directories and files
            for basenames, type_flag in [(dirs, "d"), [files, "f"]]:
                for basename in basenames:
                    t = self.child(basename, type=type_flag)
                    t.move_to(os.path.join(_dst, basename), perm=perm, dir_perm=dir_perm, **kwargs)

        # finally remove
        self.remove()

        return _dst

    def move_from(self, src, perm=None, dir_perm=None, **kwargs):
        # when src is a directory target itself, forward to its move_to implementation as it might
        # be more performant to use its own directory walking
        if isinstance(src, FileSystemDirectoryTarget):
            return src.move_to(self, perm=perm, dir_perm=dir_perm, **kwargs)

        # create the target dir
        self.touch(perm=dir_perm, **kwargs)

        # when src is a plain string, let the fs handle it
        # walk and operate recursively
        # TODO: complain when src not local? forward to copy_from request depending on protocol?
        _src = get_path(src)
        for path, dirs, files, _ in self.fs.walk(_src, max_depth=0, **kwargs):
            # recurse through directories and files
            for basenames, type_flag in [(dirs, "d"), [files, "f"]]:
                for basename in basenames:
                    t = self.child(basename, type=type_flag)
                    t.copy_from(os.path.join(_src, basename), perm=perm, dir_perm=dir_perm, **kwargs)

        # finally remove
        self.fs.remove(_src)

        return self.abspath


FileSystemTarget.file_class = FileSystemFileTarget
FileSystemTarget.directory_class = FileSystemDirectoryTarget


def get_path(target):
    if isinstance(target, FileSystemTarget):
        path = getattr(target, "abspath", no_value)
        if path != no_value:
            return path

    path = getattr(target, "path", no_value)
    if path != no_value:
        return path

    if target:
        return str(target)

    return target


def get_scheme(uri):
    # ftp://path/to/file -> ftp
    # /path/to/file -> None
    m = re.match(r"^(\w+)\:\/\/.*$", str(uri))
    return m.group(1) if m else None


def has_scheme(uri):
    return get_scheme(uri) is not None


def add_scheme(path, scheme):
    # adds a scheme to a path, if it does not already contain one
    path = str(path)
    return "{}://{}".format(scheme.rstrip(":/"), path) if not has_scheme(path) else path


def remove_scheme(uri):
    # ftp://path/to/file -> /path/to/file
    # /path/to/file -> /path/to/file
    return re.sub(r"^(\w+\:\/\/)", "", str(uri))


@contextmanager
def localize_file_targets(struct, *args, **kwargs):
    """
    Takes an arbitrary *struct* of targets, opens the contexts returned by their
    :py:meth:`FileSystemFileTarget.localize` implementations and yields their localized
    representations in the same structure as passed in *struct*. When the context is closed, the
    contexts of all localized targets are closed.
    """
    managers = []

    def enter(target):
        if callable(getattr(target, "localize", None)):
            manager = target.localize(*args, **kwargs)
            managers.append(manager)
            return manager.__enter__()

        return target

    # localize all targets, maintain the structure
    localized_targets = map_struct(enter, struct)

    # prepare exception info
    exc = None
    exc_info = (None, None, None)

    try:
        yield localized_targets

    except (Exception, KeyboardInterrupt) as e:
        exc = e
        exc_info = sys.exc_info()
        raise

    finally:
        exit_exc = []
        for manager in managers:
            try:
                manager.__exit__(*exc_info)
            except Exception as e:
                exit_exc.append(e)

        # when there was no exception during the actual yield and
        # an exception occured in one of the exit methods, raise the first one
        if not exc and exit_exc:
            raise exit_exc[0]
