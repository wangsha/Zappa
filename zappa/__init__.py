import sys
from pathlib import Path


def running_in_docker() -> bool:
    """
    Determine if zappa is running in docker.
    - When docker is used allow usage of any python version
    """
    # https://stackoverflow.com/a/20012536/24718
    cgroup_content = Path("/proc/1/cgroup").read_text()
    in_docker = "/docker/" in cgroup_content or "/lxc/" in cgroup_content
    return in_docker


SUPPORTED_VERSIONS = [(3, 7), (3, 8), (3, 9)]
MINIMUM_SUPPORTED_MINOR_VERSION = 7

if not running_in_docker() and sys.version_info[:2] not in SUPPORTED_VERSIONS:
    print(running_in_docker())
    formatted_supported_versions = ["{}.{}".format(*version) for version in SUPPORTED_VERSIONS]
    err_msg = (
        f"This version of Python ({sys.version_info.major}.{sys.version_info.minor}) is not supported!\n"
        f"Zappa (and AWS Lambda) support the following versions of Python: {formatted_supported_versions}"
    )
    raise RuntimeError(err_msg)
elif running_in_docker() and sys.version_info.minor < MINIMUM_SUPPORTED_MINOR_VERSION:
    # when running in docker enforce minimum version only
    err_msg = (
        f"This version of Python ({sys.version_info.major}.{sys.version_info.minor}) is not supported!\n"
        f"Zappa requires a minimum version of 3.{MINIMUM_SUPPORTED_MINOR_VERSION}"
    )
    raise RuntimeError(err_msg)


__version__ = "0.56.0"
