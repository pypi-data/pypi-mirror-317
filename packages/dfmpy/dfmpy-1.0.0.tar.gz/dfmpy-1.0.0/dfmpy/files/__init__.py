import logging

from dfmpy.files.normalizer import normalize_for_phantom_files
from dfmpy.files.normalizer import normalize_repo_path

LOG = logging.getLogger(__file__)


def mkdir_parents(symlink_path):
    # TODO unit test
    if not symlink_path.parent.exists():
        LOG.warning("Making directory with parents: %s", symlink_path.parent)
        symlink_path.parent.mkdir(parents=True)


def path_is_directory(path):
    # TODO unit test
    return non_symlink_path_exists(path) and path.is_dir() and not path.is_symlink()


def path_is_file(path):
    # TODO unit test
    return non_symlink_path_exists(path) and path.is_file()


def path_is_symlink(path):
    # TODO unit test
    return non_symlink_path_exists(path) and path.is_symlink()


def non_symlink_path_exists(path):
    # TODO docs - explain why path.exists() alone is not safe.
    # TODO unit test
    try:
        # Stat the path, but do not follow symlinks.
        path.lstat()
        return True
    except FileNotFoundError:
        return False
