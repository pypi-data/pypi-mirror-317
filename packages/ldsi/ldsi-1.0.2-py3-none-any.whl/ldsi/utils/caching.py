import os
from pathlib import Path


_DEFAULT_CACHE_DIR = os.path.join(Path.home(), ".ldsi_cache")
LDSI_CACHEDIR = os.environ.get("LDSI_CACHEDIR") or _DEFAULT_CACHE_DIR


def create_subdir_in_cachedir(subdir: str) -> str:
    """Create a subdirectory in the LDSI cache directory."""
    subdir = os.path.join(LDSI_CACHEDIR, subdir)
    subdir = os.path.abspath(subdir)
    os.makedirs(subdir, exist_ok=True)
    return subdir
