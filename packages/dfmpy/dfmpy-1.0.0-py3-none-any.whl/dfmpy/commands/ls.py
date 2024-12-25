import logging

import dfmpy.resources.config
import dfmpy.files.finder

LOG = logging.getLogger(__file__)

# TODO move some "search" methods into a "utils.files.search" module.


def _unique_key_for_value(items, find_value):
    # TODO unit test
    keys = [key for key, value in items if value == find_value]
    keys = tuple(keys)
    if not keys:
        return None
    if len(keys) != 1:
        raise LookupError(f"Multiple keys for value: {find_value} => {keys}")
    return keys[0]


def _get_broken_paths(
    expected_paths, installed_paths
):  # pylint: disable=unused-argument
    # TODO docs - The installed file points to a non-existent file.
    # TODO unit test
    LOG.debug("Finding installed files that point to non-existent files.")
    for installed_path in installed_paths:
        if not installed_path.resolve().exists():
            yield installed_path, installed_path.resolve()


def _get_stale_paths(expected_paths, installed_paths):
    # TODO docs - The installed file resolves to the wrong repo file.
    # TODO unit test
    LOG.debug("Finding installed files that resolve to the wrong file.")
    for installed_path in installed_paths:
        expected = _unique_key_for_value(
            expected_paths.items(), installed_path.resolve()
        )
        if installed_path != expected:
            yield installed_path, expected


def _get_not_installed_paths(expected_paths, installed_paths):
    # TODO docs - The expected file is not pointed to by an installed file.
    # TODO unit test
    LOG.debug("Finding expected files that are not installed.")
    installed_files_keys = installed_paths.keys()
    for expected_path in expected_paths.keys():
        if expected_path not in installed_files_keys:
            yield expected_path, expected_paths[expected_path]


def _get_proper_paths(expected_paths, installed_paths):
    # TODO docs - The expected file is properly installed.
    # TODO unit test
    # TODO this needs testing once "sync" is implemented!
    LOG.debug("Finding installed properly installed files.")
    installed_files_keys = installed_paths.keys()
    for expected_path in expected_paths:
        if expected_path in installed_files_keys:
            installed = installed_paths[expected_path]
            if expected_path.resolve() == installed.resolve():
                yield expected_path, expected_paths[expected_path]


def _print(logger, files, message, comparator_symbol):
    # TODO unit test
    if files:
        for idx, (left, right) in enumerate(files):
            if idx == 0:
                # Since "files" could be a generator, only log the message if we
                # can actually iterate over the items.  Thus only print for the
                # first element.
                logger(message)
            logger("%s %s %s", left, comparator_symbol, right)


# pylint: disable=duplicate-code
def ls():  # pylint: disable=invalid-name
    # TODO unit test
    # TODO add a "--tree" option to the this command

    install_dir = dfmpy.resources.config.get_config().install_dir
    repository_dir = dfmpy.resources.config.get_config().repository_dir

    expected_paths = dfmpy.files.finder.get_expected_paths(install_dir, repository_dir)
    installed_paths = dfmpy.files.finder.get_installed_paths(
        install_dir, repository_dir
    )

    broken = _get_broken_paths(expected_paths, installed_paths)
    _print(LOG.critical, broken, "Found broken files:", "?=")

    stale = _get_stale_paths(expected_paths, installed_paths)
    _print(LOG.error, stale, "Found stale files:", "~=")

    not_installed = _get_not_installed_paths(expected_paths, installed_paths)
    _print(LOG.warning, not_installed, "Found files not installed:", "!=")

    proper = _get_proper_paths(expected_paths, installed_paths)
    _print(LOG.info, proper, "Found installed files:", "==")


def _ls_main(cli):  # pylint: disable=unused-argument
    # TODO unit test
    ls()


def setup_subparser(subparsers, default_args):
    # TODO unit test
    ls_parser = subparsers.add_parser("list")
    ls_parser.set_defaults(main=_ls_main)
    ls_parser.add_argument(*default_args.verbose_args, **default_args.verbose_kwargs)
    return ls_parser
