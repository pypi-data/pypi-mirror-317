import collections
import functools
import logging
import os
import pathlib

import dfmpy.resources.config
import dfmpy.files
import dfmpy.files.normalizer

LOG = logging.getLogger(__file__)

# The cache should never get larger than 2, one for $HOME and one for the repo
# dir.  There should be no need for a cache of any other directory.
_FILE_TREE_CACHE_SIZE = 2


def _ignore(path):
    # TODO unit test
    for pattern in dfmpy.resources.config.get_ignore_globs():
        if path.match(pattern):
            return True
    return False


def _no_permissions_to_stat(path):
    # TODO docs - the path must exist, but is not accessible.
    # TODO unit test
    # TODO is it possible to remove access() in favor or Path() methods?
    return path.exists() and not os.access(path, os.R_OK)


def _find_all_paths(dir_path):  # pylint: disable=inconsistent-return-statements
    # TODO docs - returns all files and (directories with markers)
    # TODO unit test
    marker = dfmpy.resources.config.get_config().marker
    if not dir_path.exists():
        return tuple()

    for path in dir_path.iterdir():
        if _ignore(path):
            LOG.debug("Ignoring: %s", path)

        elif _no_permissions_to_stat(path):
            LOG.error("No permissions to read: %s", path)

        elif dfmpy.files.path_is_directory(path):
            if marker in path.name:
                LOG.debug("Found special directory: %s", path)
                yield path
            else:
                LOG.debug("Traversing down directory: %s", path)
                yield from get_all_paths(path)

        elif dfmpy.files.path_is_file(path):
            LOG.debug("Found file: %s", path)
            yield path

        elif dfmpy.files.path_is_symlink(path):
            LOG.debug("Found symlink: %s", path)
            yield path

        else:
            LOG.error("Found unknown node type: %s", path)


@functools.lru_cache(maxsize=_FILE_TREE_CACHE_SIZE)
def get_all_paths(dir_name):
    # TODO docs - returns the same as __find_all_paths()
    # TODO unit test
    paths = []
    paths.extend(_find_all_paths(pathlib.Path(dir_name)))
    paths.sort()
    return tuple(paths)


@functools.lru_cache(maxsize=_FILE_TREE_CACHE_SIZE)
def get_installed_paths(install_dir, repo_dir):
    # TODO unit test
    LOG.debug("Searching for installed paths under: %s", install_dir)
    installed_paths = get_all_paths(install_dir)
    installed_paths = [p for p in installed_paths if dfmpy.files.path_is_symlink(p)]
    installed_paths = [
        p for p in installed_paths if str(p.resolve()).startswith(repo_dir)
    ]
    mapping = collections.OrderedDict()
    mapping.update([(p, pathlib.Path(p.resolve())) for p in installed_paths])
    return mapping


@functools.lru_cache(maxsize=_FILE_TREE_CACHE_SIZE)
def get_expected_paths(install_dir, repo_dir):
    # TODO unit test
    LOG.debug("Searching for expected paths under: %s", repo_dir)
    marker = dfmpy.resources.config.get_config().marker
    repo_paths = get_all_paths(repo_dir)
    repo_paths = dfmpy.files.normalizer.normalize_for_phantom_files(repo_paths)
    repo_paths = [p for p in repo_paths if not _ignore(p)]
    repo_paths = [p for p in repo_paths if marker not in p.name]
    mapping = collections.OrderedDict()
    for repo_path in repo_paths:
        installed_file = str(repo_path).replace(repo_dir, install_dir)
        installed_path = pathlib.Path(installed_file)
        nrp = dfmpy.files.normalizer.normalize_repo_path(repo_path)
        if nrp.resolve().exists():
            mapping[installed_path] = nrp
    return mapping
