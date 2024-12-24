# coding: utf-8

"""
Proxy task definition and helpers.
"""

__all__ = ["ProxyTask", "ProxyCommand", "get_proxy_attribute"]


import shlex

import six

from law.task.base import BaseRegister, BaseTask, Task
from law.parameter import TaskInstanceParameter
from law.parser import global_cmdline_args
from law.util import quote_cmd


_forward_workflow_attributes = {"requires", "output", "complete", "run"}

_forward_sandbox_attributes = {"input", "output", "run"}


class ProxyRegister(BaseRegister):
    """
    Meta class for proxy tasks with the sole purpose of disabling instance caching.
    """


# disable instance caching
ProxyRegister.disable_instance_cache()


class ProxyTask(six.with_metaclass(ProxyRegister, BaseTask)):

    task = TaskInstanceParameter()

    exclude_params_req = {"task"}


class ProxyAttributeTask(Task):

    _proxy_attribute_task_init = False

    def __init__(self, *args, **kwargs):
        super(ProxyAttributeTask, self).__init__(*args, **kwargs)

        self._proxy_attribute_task_init = True

    def __getattribute__(self, attr, proxy=None):
        if attr == "_proxy_attribute_task_init":
            return super(ProxyAttributeTask, self).__getattribute__(attr)

        if proxy is None:
            proxy = bool(self._proxy_attribute_task_init)

        return get_proxy_attribute(ProxyAttributeTask, self, attr, proxy=proxy)


class ProxyCommand(object):

    arg_sep = "__law_arg_sep__"

    def __init__(
        self,
        task,
        exclude_task_args=None,
        exclude_global_args=None,
        executable="law",
    ):
        super(ProxyCommand, self).__init__()

        self.task = task
        self.args = self.load_args(
            exclude_task_args=exclude_task_args,
            exclude_global_args=exclude_global_args,
        )
        self.executable = None
        if isinstance(executable, (list, tuple)):
            self.executable = list(executable)
        elif executable:
            self.executable = shlex.split(str(executable))

    def load_args(self, exclude_task_args=None, exclude_global_args=None):
        args = []

        # add cli args as key value tuples
        args.extend(self.task.cli_args(exclude=exclude_task_args).items())

        # add global args as key value tuples
        args.extend(global_cmdline_args(exclude=exclude_global_args).items())

        return args

    def remove_arg(self, key):
        if not key.startswith("--"):
            key = "--" + key.lstrip("-")

        self.args = [tpl for tpl in self.args if tpl[0] != key]

    def add_arg(self, key, value, overwrite=False):
        if not key.startswith("--"):
            key = "--" + key.lstrip("-")

        if overwrite:
            self.remove_arg(key)

        self.args.append((key, value))

    def build_run_cmd(self, executable=None):
        exe = self.executable
        if isinstance(executable, (list, tuple)):
            exe = list(executable)
        elif executable:
            exe = shlex.split(str(executable))
        return exe + ["run", "{}.{}".format(self.task.__module__, self.task.__class__.__name__)]

    def build(self, skip_run=False, executable=None):
        # start with the run command
        cmd = [] if skip_run else self.build_run_cmd(executable=executable)

        # add arguments and insert dummary key value separators which are replaced with "=" later
        for key, value in self.args:
            cmd.extend([key, self.arg_sep, value])

        cmd = " ".join(quote_cmd([c]) for c in cmd)
        cmd = cmd.replace(" " + self.arg_sep + " ", "=")

        return cmd

    def __str__(self):
        # default command
        return self.build()


def get_proxy_attribute(cls, task, attr, proxy=True):
    """
    Returns an attribute *attr* of a *task* taking into account possible proxies such as owned by
    workflow (:py:class:`BaseWorkflow`) or sandbox tasks (:py:class:`SandboxTask`). The reason for
    having an external function to evaluate possible attribute forwarding is the complexity of
    attribute lookup independent of the method resolution order. When the requested attribute is not
    forwarded or *proxy* is *False*, the default lookup implemented in the super method of *cls* is
    used.
    """
    if proxy:
        # priority to workflow proxy forwarding, fallback to sandbox proxy or super class
        if (
            attr in _forward_workflow_attributes and
            isinstance(task, BaseWorkflow) and
            task.is_workflow()
        ):
            return getattr(task.workflow_proxy, attr)

        if attr in _forward_sandbox_attributes and isinstance(task, SandboxTask):
            # forward run method if not sandboxed
            if attr == "run" and not task.is_sandboxed():
                return task.sandbox_proxy.run
            # foward input and output methods
            if attr == "input" and task._proxy_staged_input():
                return task._staged_input
            if attr == "output" and task._proxy_staged_output():
                return task._staged_output

    return super(cls, task).__getattribute__(attr)


# trailing imports
from law.workflow.base import BaseWorkflow
from law.sandbox.base import SandboxTask
