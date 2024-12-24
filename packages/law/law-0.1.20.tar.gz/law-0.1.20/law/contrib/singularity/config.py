# coding: utf-8

"""
Function returning the config defaults of the singularity package.
"""


def config_defaults(default_config):
    return {
        "singularity_sandbox": {
            "stagein_dir_name": "stagein",
            "stageout_dir_name": "stageout",
            "law_executable": "law",
            "uid": None,
            "gid": None,
            "forward_dir": "/law_forward",
            "python_dir": "py",
            "bin_dir": "bin",
            "allow_binds": True,
            "forward_law": True,
        },
        "singularity_sandbox_env": {},
        "singularity_sandbox_volumes": {},
    }
