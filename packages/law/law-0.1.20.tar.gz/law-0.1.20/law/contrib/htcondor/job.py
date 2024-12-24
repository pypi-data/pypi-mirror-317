# coding: utf-8

"""
HTCondor job manager. See https://research.cs.wisc.edu/htcondor.
"""

__all__ = ["HTCondorJobManager", "HTCondorJobFileFactory"]


import os
import stat
import time
import re
import tempfile
import subprocess

from law.config import Config
from law.job.base import BaseJobManager, BaseJobFileFactory, JobInputFile, DeprecatedInputFiles
from law.target.file import get_path
from law.util import interruptable_popen, make_list, make_unique, quote_cmd
from law.logger import get_logger

from law.contrib.htcondor.util import get_htcondor_version


logger = get_logger(__name__)

_cfg = Config.instance()


class HTCondorJobManager(BaseJobManager):

    # whether to use job grouping or batched submission
    job_grouping_submit = _cfg.get_expanded_bool("job", "htcondor_job_grouping_submit")

    # settings depending on job grouping or batched submission
    merge_job_files = False
    chunk_size_submit = 0
    if not job_grouping_submit:
        # whether to merge jobs files for batched submission
        merge_job_files = _cfg.get_expanded_bool("job", "htcondor_merge_job_files")

        # chunking for batched submission
        chunk_size_submit = (
            _cfg.get_expanded_int("job", "htcondor_chunk_size_submit")
            if merge_job_files
            else 0
        )

    # other chunking settings
    chunk_size_cancel = _cfg.get_expanded_int("job", "htcondor_chunk_size_cancel")
    chunk_size_query = _cfg.get_expanded_int("job", "htcondor_chunk_size_query")

    submission_job_id_cre = re.compile(r"^(\d+) job\(s\) submitted to cluster (\d+)\.$")
    long_block_cre = re.compile(r"(\w+) \= \"?([^\"\n]*)\"?\n")

    def __init__(self, pool=None, scheduler=None, user=None, threads=1):
        super(HTCondorJobManager, self).__init__()

        self.pool = pool
        self.scheduler = scheduler
        self.user = user
        self.threads = threads

        # determine the htcondor version once
        self.htcondor_version = get_htcondor_version()

        # flags for versions with some important changes
        self.htcondor_ge_v833 = self.htcondor_version and self.htcondor_version >= (8, 3, 3)
        self.htcondor_ge_v856 = self.htcondor_version and self.htcondor_version >= (8, 5, 6)

    def cleanup(self, *args, **kwargs):
        raise NotImplementedError("HTCondorJobManager.cleanup is not implemented")

    def cleanup_batch(self, *args, **kwargs):
        raise NotImplementedError("HTCondorJobManager.cleanup_batch is not implemented")

    def submit(self, job_file, job_files=None, pool=None, scheduler=None, spool=False, retries=0,
            retry_delay=3, silent=False):
        # signature is the superset for both grouped and batched submission, and the dispatching to
        # the actual submission implementation is based on the presence of job_files
        kwargs = {
            "pool": pool,
            "scheduler": scheduler,
            "spool": spool,
            "retries": retries,
            "retry_delay": retry_delay,
            "silent": silent,
        }

        if job_files is None:
            func = self._submit_impl_batched
        else:
            kwargs["job_files"] = job_files
            func = self._submit_impl_grouped

        return func(job_file, **kwargs)

    def _submit_impl_batched(self, job_file, pool=None, scheduler=None, spool=False, retries=0,
            retry_delay=3, silent=False):
        # default arguments
        if pool is None:
            pool = self.pool
        if scheduler is None:
            scheduler = self.scheduler

        # when job_file is a sequence of files, merge them all into one and submit it
        # however, this only for job files being located in the same directory or if they have an
        # "initialdir" defined
        def has_initialdir(job_file):
            with open(job_file, "r") as f:
                for line in f.readlines():
                    if line.lower().strip().replace(" ", "").startswith("initialdir="):
                        return True
            return False

        chunking = isinstance(job_file, (list, tuple))
        job_files = list(map(str, make_list(job_file)))
        job_file_dir = None
        for i, job_file in enumerate(job_files):
            dirname, basename = os.path.split(job_file)
            if job_file_dir is None:
                if i == len(job_files) - 1 or not has_initialdir(job_file):
                    job_file_dir = dirname
            elif dirname != job_file_dir:
                if not has_initialdir(job_file):
                    raise Exception(
                        "cannot performed chunked submission as job file '{}' is not located in a "
                        "previously seen directory '{}' and has no initialdir".format(
                            job_file, job_file_dir,
                        ),
                    )

        # define a single, merged job file if necessary
        if self.merge_job_files and len(job_files) > 1:
            _job_file = tempfile.mkstemp(prefix="merged_job_", suffix=".jdl", dir=job_file_dir)[1]
            with open(_job_file, "w") as f:
                for job_file in job_files:
                    with open(job_file, "r") as _f:
                        f.write(_f.read() + "\n")
            job_files = [_job_file]

        # build the command
        cmd = ["condor_submit"]
        if pool:
            cmd += ["-pool", pool]
        if scheduler:
            cmd += ["-name", scheduler]
        if spool:
            cmd.append("-spool")
        cmd += list(map(os.path.basename, job_files))
        cmd = quote_cmd(cmd)

        # define the actual submission in a loop to simplify retries
        while True:
            # run the command
            logger.debug("submit htcondor job with command '{}'".format(cmd))
            code, out, err = interruptable_popen(cmd, shell=True, executable="/bin/bash",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(job_files[0]))

            # get the job id(s)
            if code == 0:
                # loop through all lines and try to match the expected pattern
                job_ids = []
                for line in out.strip().split("\n"):
                    m = self.submission_job_id_cre.match(line.strip())
                    if m:
                        job_ids.extend([
                            "{}.{}".format(m.group(2), i)
                            for i in range(int(m.group(1)))
                        ])
                if not job_ids:
                    code = 1
                    err = "cannot parse htcondor job id(s) from output:\n{}".format(out)

            # retry or done?
            if code == 0:
                return job_ids if chunking else job_ids[0]

            job_files_repr = ",".join(map(os.path.basename, job_files))
            logger.debug("submission of htcondor job(s) '{}' failed with code {}:\n{}".format(
                job_files_repr, code, err))

            if retries > 0:
                retries -= 1
                time.sleep(retry_delay)
                continue

            if silent:
                return None

            raise Exception("submission of htcondor job(s) '{}' failed:\n{}".format(
                job_files_repr, err))

    def _submit_impl_grouped(self, job_file, job_files=None, pool=None, scheduler=None, spool=False,
            retries=0, retry_delay=3, silent=False):
        # default arguments
        if pool is None:
            pool = self.pool
        if scheduler is None:
            scheduler = self.scheduler

        # build the command
        cmd = ["condor_submit"]
        if pool:
            cmd += ["-pool", pool]
        if scheduler:
            cmd += ["-name", scheduler]
        if spool:
            cmd.append("-spool")
        cmd.append(os.path.basename(job_file))
        cmd = quote_cmd(cmd)

        # define the actual submission in a loop to simplify retries
        while True:
            # run the command
            logger.debug("submit htcondor job with command '{}'".format(cmd))
            code, out, err = interruptable_popen(cmd, shell=True, executable="/bin/bash",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=os.path.dirname(job_file))

            # get the job id(s)
            if code == 0:
                # loop through all lines and try to match the expected pattern
                job_ids = []
                for line in out.strip().split("\n"):
                    m = self.submission_job_id_cre.match(line.strip())
                    if m:
                        job_ids.extend([
                            "{}.{}".format(m.group(2), i)
                            for i in range(int(m.group(1)))
                        ])
                if not job_ids:
                    code = 1
                    err = "cannot parse htcondor job id(s) from output:\n{}".format(out)

            # retry or done?
            if code == 0:
                return job_ids

            logger.debug("submission of htcondor job(s) '{}' failed with code {}:\n{}".format(
                job_file, code, err))

            if retries > 0:
                retries -= 1
                time.sleep(retry_delay)
                continue

            if silent:
                return None

            raise Exception("submission of htcondor job(s) '{}' failed:\n{}".format(job_file, err))

    def cancel(self, job_id, pool=None, scheduler=None, silent=False):
        # default arguments
        if pool is None:
            pool = self.pool
        if scheduler is None:
            scheduler = self.scheduler

        chunking = isinstance(job_id, (list, tuple))
        job_ids = make_list(job_id)

        # build the command
        cmd = ["condor_rm"]
        if pool:
            cmd += ["-pool", pool]
        if scheduler:
            cmd += ["-name", scheduler]
        cmd += job_ids
        cmd = quote_cmd(cmd)

        # run it
        logger.debug("cancel htcondor job(s) with command '{}'".format(cmd))
        code, out, err = interruptable_popen(cmd, shell=True, executable="/bin/bash",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # check success
        if code != 0 and not silent:
            raise Exception("cancellation of htcondor job(s) '{}' failed with code {}:\n{}".format(
                job_id, code, err))

        return {job_id: None for job_id in job_ids} if chunking else None

    def query(self, job_id, pool=None, scheduler=None, user=None, silent=False):
        # default arguments
        if pool is None:
            pool = self.pool
        if scheduler is None:
            scheduler = self.scheduler
        if user is None:
            user = self.user

        chunking = isinstance(job_id, (list, tuple))
        job_ids = make_list(job_id)

        # default ClassAds to getch
        ads = "ClusterId,ProcId,JobStatus,ExitCode,ExitStatus,HoldReason,RemoveReason"

        # build the condor_q command
        cmd = ["condor_q"] + job_ids
        if pool:
            cmd += ["-pool", pool]
        if scheduler:
            cmd += ["-name", scheduler]
        cmd += ["-long"]
        # since v8.3.3 one can limit the number of jobs to query
        if self.htcondor_ge_v833:
            cmd += ["-limit", str(len(job_ids))]
        # since v8.5.6 one can define the attributes to fetch
        if self.htcondor_ge_v856:
            cmd += ["-attributes", ads]
        cmd = quote_cmd(cmd)

        logger.debug("query htcondor job(s) with command '{}'".format(cmd))
        code, out, err = interruptable_popen(cmd, shell=True, executable="/bin/bash",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # handle errors
        if code != 0:
            if silent:
                return None
            raise Exception("queue query of htcondor job(s) '{}' failed with code {}:"
                "\n{}".format(job_id, code, err))

        # parse the output and extract the status per job
        query_data = self.parse_long_output(out)

        # some jobs might already be in the condor history, so query for missing job ids
        missing_ids = [_job_id for _job_id in job_ids if _job_id not in query_data]
        if missing_ids:
            # build the condor_history command, which is fairly similar to the condor_q command
            cmd = ["condor_history"] + missing_ids
            if pool:
                cmd += ["-pool", pool]
            if scheduler:
                cmd += ["-name", scheduler]
            cmd += ["-long"]
            # since v8.3.3 one can limit the number of jobs to query
            if self.htcondor_ge_v833:
                cmd += ["-limit", str(len(missing_ids))]
            # since v8.5.6 one can define the attributes to fetch
            if self.htcondor_ge_v856:
                cmd += ["-attributes", ads]
            cmd = quote_cmd(cmd)

            logger.debug("query htcondor job history with command '{}'".format(cmd))
            code, out, err = interruptable_popen(cmd, shell=True, executable="/bin/bash",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # handle errors
            if code != 0:
                if silent:
                    return None
                raise Exception("history query of htcondor job(s) '{}' failed with code {}:"
                    "\n{}".format(job_id, code, err))

            # parse the output and update query data
            query_data.update(self.parse_long_output(out))

        # compare to the requested job ids and perform some checks
        for _job_id in job_ids:
            if _job_id not in query_data:
                if not chunking:
                    if silent:
                        return None
                    raise Exception("htcondor job(s) '{}' not found in query response".format(
                        job_id))

                query_data[_job_id] = self.job_status_dict(job_id=_job_id, status=self.FAILED,
                    error="job not found in query response")

        return query_data if chunking else query_data[job_id]

    @classmethod
    def parse_long_output(cls, out):
        # retrieve information per block mapped to the job id
        query_data = {}
        for block in out.strip().split("\n\n"):
            data = dict(cls.long_block_cre.findall(block + "\n"))
            if not data:
                continue

            # build the job id
            if "ClusterId" not in data and "ProcId" not in data:
                continue
            job_id = "{ClusterId}.{ProcId}".format(**data)

            # get the job status code
            status = cls.map_status(data.get("JobStatus"))

            # get the exit code
            code = int(data.get("ExitCode") or data.get("ExitStatus") or "0")

            # get the error message, undefined counts as None
            error = data.get("HoldReason", "undefined")
            if error.lower() == "undefined":
                error = None
            remove_error = data.get("RemoveReason", "undefined")
            if remove_error.lower() == "undefined":
                remove_error = None
            # prefer remove error
            if remove_error:
                error = remove_error

            # handle inconsistencies between status, code and the presence of an error message
            if code != 0:
                if status != cls.FAILED:
                    status = cls.FAILED
                    if not error:
                        error = "job status set to '{}' due to non-zero exit code {}".format(
                            cls.FAILED, code)

            # store it
            query_data[job_id] = cls.job_status_dict(job_id=job_id, status=status, code=code,
                error=error)

        return query_data

    @classmethod
    def map_status(cls, status_flag):
        # see http://pages.cs.wisc.edu/~adesmet/status.html
        if status_flag in ("0", "1", "U", "I"):
            return cls.PENDING
        elif status_flag in ("2", "R"):
            return cls.RUNNING
        elif status_flag in ("4", "C"):
            return cls.FINISHED
        elif status_flag in ("5", "6", "H", "E"):
            return cls.FAILED
        else:
            return cls.FAILED


class HTCondorJobFileFactory(BaseJobFileFactory):

    config_attrs = BaseJobFileFactory.config_attrs + [
        "file_name", "command", "executable", "arguments", "input_files", "output_files", "log",
        "stdout", "stderr", "postfix_output_files", "postfix", "universe",
        "notification", "custom_content", "absolute_paths",
    ]

    def __init__(self, file_name="htcondor_job.jdl", command=None, executable=None, arguments=None,
            input_files=None, output_files=None, log="log.txt", stdout="stdout.txt",
            stderr="stderr.txt", postfix_output_files=True, postfix=None, universe="vanilla",
            notification="Never", custom_content=None, absolute_paths=False, **kwargs):
        # get some default kwargs from the config
        cfg = Config.instance()
        if kwargs.get("dir") is None:
            kwargs["dir"] = cfg.get_expanded("job", cfg.find_option("job",
                "htcondor_job_file_dir", "job_file_dir"))
        if kwargs.get("mkdtemp") is None:
            kwargs["mkdtemp"] = cfg.get_expanded_bool("job", cfg.find_option("job",
                "htcondor_job_file_dir_mkdtemp", "job_file_dir_mkdtemp"))
        if kwargs.get("cleanup") is None:
            kwargs["cleanup"] = cfg.get_expanded_bool("job", cfg.find_option("job",
                "htcondor_job_file_dir_cleanup", "job_file_dir_cleanup"))

        super(HTCondorJobFileFactory, self).__init__(**kwargs)

        self.file_name = file_name
        self.command = command
        self.executable = executable
        self.arguments = arguments
        self.input_files = DeprecatedInputFiles(input_files or {})
        self.output_files = output_files or {}
        self.log = log
        self.stdout = stdout
        self.stderr = stderr
        self.postfix_output_files = postfix_output_files
        self.postfix = postfix
        self.universe = universe
        self.notification = notification
        self.custom_content = custom_content
        self.absolute_paths = absolute_paths

    def create(self, grouped_submission=False, **kwargs):
        # merge kwargs and instance attributes
        c = self.get_config(**kwargs)

        # some sanity checks
        if not c.file_name:
            raise ValueError("file_name must not be empty")
        if not c.arguments:
            raise ValueError("arguments must not be empty")
        c.arguments = make_list(c.arguments)
        if grouped_submission and c.postfix:
            c.postfix = make_list(c.postfix)
            if len(c.postfix) != len(c.arguments):
                raise ValueError("number of postfixes does not match the number of arguments")
        if c.postfix_output_files and not c.postfix:
            raise ValueError("postfix must not be empty when postfix_output_files is set")
        if not c.command and not c.executable:
            raise ValueError("either command or executable must not be empty")
        if not c.universe:
            raise ValueError("universe must not be empty")

        # ensure that output_files is a dict mapping remote paths on the job node
        # to local paths on the submission node
        # (relative local paths will be resolved relative to the initial dir)
        c.output_files = {
            str(k): str(v)
            for k, v in (
                c.output_files.items()
                if isinstance(c.output_files, dict)
                else zip(c.output_files, c.output_files)
            )
        }

        # ensure that the custom log file is an output file
        if c.custom_log_file:
            c.custom_log_file = str(c.custom_log_file)
            custom_log_file_base = os.path.basename(c.custom_log_file)
            if custom_log_file_base not in c.output_files:
                c.output_files[custom_log_file_base] = c.custom_log_file
            c.custom_log_file = custom_log_file_base

        # postfix certain output files
        postfix = "$(law_job_postfix)" if grouped_submission else c.postfix
        if c.postfix_output_files:
            skip_postfix_cre = re.compile(r"^(/dev/).*$")
            skip_postfix = lambda s: bool(skip_postfix_cre.match(str(s)))
            add_postfix = lambda s: s if skip_postfix(s) else self.postfix_output_file(s, postfix)
            c.output_files = {add_postfix(k): add_postfix(v) for k, v in c.output_files.items()}
            for attr in ["log", "stdout", "stderr", "custom_log_file"]:
                if c[attr]:
                    c[attr] = add_postfix(c[attr])

        # ensure that all input files are JobInputFile objects
        c.input_files = {
            key: JobInputFile(f)
            for key, f in c.input_files.items()
        }

        # ensure that the executable is an input file, remember the key to access it
        if c.executable:
            executable_keys = [
                k
                for k, v in c.input_files.items()
                if get_path(v) == get_path(c.executable)
            ]
            if executable_keys:
                executable_key = executable_keys[0]
            else:
                executable_key = "executable_file"
                c.input_files[executable_key] = JobInputFile(c.executable)

        # prepare input files
        def prepare_input(f):
            # when not copied or forwarded, just return the absolute, original path
            abs_path = os.path.abspath(f.path)
            if not f.copy or f.forward:
                return abs_path
            # copy the file
            abs_path = self.provide_input(
                src=abs_path,
                postfix=c.postfix if f.postfix and not f.share and not grouped_submission else None,
                dir=c.dir,
                skip_existing=f.share,
                increment_existing=f.increment and not f.share and grouped_submission,
            )
            return abs_path

        # absolute input paths
        for key, f in c.input_files.items():
            f.path_sub_abs = prepare_input(f)

        # input paths relative to the submission or initial dir
        # forwarded files are skipped as they are not treated as normal inputs
        for key, f in c.input_files.items():
            if f.forward:
                continue
            f.path_sub_rel = (
                os.path.basename(f.path_sub_abs)
                if f.copy and not c.absolute_paths else
                f.path_sub_abs
            )

        # input paths as seen by the job, before and after potential rendering
        for key, f in c.input_files.items():
            f.path_job_pre_render = (
                f.path_sub_abs
                if f.forward else
                os.path.basename(f.path_sub_abs)
            )
            f.path_job_post_render = (
                f.path_sub_abs
                if f.forward and not f.render_job else
                os.path.basename(f.path_sub_abs)
            )

        # update files in render variables with version after potential rendering
        c.render_variables.update({
            key: f.path_job_post_render
            for key, f in c.input_files.items()
        })

        # add space separated input files before potential rendering to render variables
        c.render_variables["input_files"] = " ".join(
            f.path_job_pre_render
            for f in c.input_files.values()
        )

        # add space separated list of input files for rendering
        c.render_variables["input_files_render"] = " ".join(
            f.path_job_pre_render
            for f in c.input_files.values()
            if f.render_job
        )

        # add the custom log file to render variables
        if c.custom_log_file:
            c.render_variables["log_file"] = c.custom_log_file

        # add the file postfix to render variables
        # (this is done in the wrapper script for grouped submission)
        if not grouped_submission and c.postfix and "file_postfix" not in c.render_variables:
            c.render_variables["file_postfix"] = c.postfix

        # inject arguments into the htcondor wrapper via render variables
        if grouped_submission:
            c.render_variables["htcondor_job_arguments_map"] = ("\n" + 8 * " ").join(
                "['{}']=\"{}\"".format(i + 1, str(args))
                for i, args in enumerate(c.arguments)
            )

        # linearize render variables
        render_variables = self.linearize_render_variables(c.render_variables)

        # prepare the job description file
        job_file = os.path.join(c.dir, str(c.file_name))
        if not grouped_submission:
            job_file = self.postfix_input_file(job_file, c.postfix)

        # render copied, non-forwarded input files
        for key, f in c.input_files.items():
            if not f.copy or f.forward or not f.render_local:
                continue
            self.render_file(
                f.path_sub_abs,
                f.path_sub_abs,
                render_variables,
                postfix=c.postfix if not grouped_submission and f.postfix else None,
            )

        # prepare the executable when given
        if c.executable:
            c.executable = get_path(c.input_files[executable_key].path_job_post_render)
            # make the file executable for the user and group
            path = os.path.join(c.dir, os.path.basename(c.executable))
            if os.path.exists(path):
                os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP)

        # helper to encode lists
        def encode_list(items, sep=" ", quote=True):
            items = make_list(items)
            s = sep.join(map(str, items))
            if quote:
                s = "\"{}\"".format(s)  # noqa: Q003
            return s

        # helper to encode dicts
        def encode_dict(d, sep=" ; ", quote=True):
            s = sep.join("{} = {}".format(k, v) for k, v in d.items())
            if quote:
                s = "\"{}\"".format(s)  # noqa: Q003
            return s

        # job file content
        content = []
        content.append(("universe", c.universe))
        output_remaps = {}
        if c.command:
            cmd = quote_cmd(c.command) if isinstance(c.command, (list, tuple)) else c.command
            content.append(("executable", cmd))
        else:
            content.append(("executable", c.executable))
        if c.log:
            content.append(("log", c.log))
        if c.stdout:
            c.stdout = str(c.stdout)
            stdout_base = os.path.basename(c.stdout)
            content.append(("output", stdout_base))
            if stdout_base != c.stdout:
                output_remaps[stdout_base] = c.stdout
        if c.stderr:
            c.stderr = str(c.stderr)
            stderr_base = os.path.basename(c.stderr)
            content.append(("error", stderr_base))
            if stderr_base != c.stderr:
                output_remaps[stderr_base] = c.stderr
        if c.input_files or c.output_files:
            content.append(("should_transfer_files", "YES"))
        if c.input_files:
            content.append(("transfer_input_files", encode_list(
                make_unique(
                    f.path_sub_rel
                    for f in c.input_files.values()
                    if f.path_sub_rel
                ),
                sep=",",
                quote=False,
            )))
        if c.output_files:
            content.append(("transfer_output_files", encode_list(
                c.output_files.keys(),
                sep=",",
                quote=False,
            )))
            # add mapping to local paths when different
            output_remaps.update({
                remote_path: local_path
                for remote_path, local_path in c.output_files.items()
                if remote_path != local_path
            })
            content.append(("when_to_transfer_output", "ON_EXIT"))
        if output_remaps:
            content.append(("transfer_output_remaps", encode_dict(output_remaps)))
        if c.notification:
            content.append(("notification", c.notification))

        # add custom content
        if c.custom_content:
            content += c.custom_content

        # add htcondor specific env variables
        env_vars = []
        _content = []
        for obj in content:
            if isinstance(obj, tuple) and len(obj) == 2 and obj[0].lower() == "environment":
                env_vars.append(obj[1].strip("\""))  # noqa: Q003
            else:
                _content.append(obj)
        content = _content
        # add new ones and add back to content
        env_vars.append("LAW_HTCONDOR_JOB_CLUSTER=$(Cluster)")
        env_vars.append("LAW_HTCONDOR_JOB_PROCESS=$(Process)")
        content.append(("environment", encode_list(env_vars, sep=" ", quote=True)))

        # queue
        if grouped_submission:
            content.append("queue law_job_postfix, arguments from (")
            for i in range(len(c.arguments)):
                pf = log = "''"
                if c.postfix_output_files:
                    pf = c.postfix[i]
                    if c.custom_log_file:
                        log = c.custom_log_file
                content.append("    {0}, {0} {1}".format(pf, log))
            content.append(")")
        elif c.arguments:
            for _arguments in c.arguments:
                content.append(("arguments", _arguments))
                content.append("queue")
        else:
            content.append("queue")

        # write the job file
        with open(job_file, "w") as f:
            for obj in content:
                line = self.create_line(*make_list(obj))
                f.write(line + "\n")

        logger.debug("created htcondor job file at '{}'".format(job_file))

        return job_file, c

    @classmethod
    def create_line(cls, key, value=None):
        if value is None:
            return str(key)
        return "{} = {}".format(key, value)
