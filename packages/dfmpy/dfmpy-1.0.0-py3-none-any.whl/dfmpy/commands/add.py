import logging
import pathlib

import dfmpy.files.normalizer
import dfmpy.files.syncer
import dfmpy.resources.config
import dfmpy.files

LOG = logging.getLogger(__file__)


def _filter_non_destination_paths(paths):
    # TODO unit test
    install_dir = dfmpy.resources.config.get_config().install_dir
    good_paths = []
    for path in paths:
        if not dfmpy.files.non_symlink_path_exists(path):
            LOG.error("Cannot add non-existent path: %s", path)
        elif not str(path).startswith(install_dir):
            LOG.error("Cannot add path not under destination: %s", path)
        else:
            good_paths.append(path)
    return tuple(good_paths)


def _determine_expected_paths(paths):
    # TODO unit test
    repository_dir = dfmpy.resources.config.get_config().repository_dir
    install_dir = dfmpy.resources.config.get_config().install_dir

    marker = dfmpy.resources.config.get_config().marker
    delimiter = dfmpy.resources.config.get_config().delimiter
    hostname = dfmpy.resources.config.get_config().hostname
    system_type = dfmpy.resources.config.get_config().system

    expected_paths = {}
    for path in paths:
        target_path = str(path).replace(install_dir, repository_dir)
        target_path += marker
        target_path += delimiter.join(hostname, system_type)
        expected_paths[path] = pathlib.Path(target_path)
    return expected_paths


def _move_expected_paths(expected_paths, force):
    # TODO unit test
    for old, new in expected_paths.items():
        if not force:
            LOG.info("Simulated renaming %s -> %s", old, new)
        else:
            dfmpy.files.mkdir_parents(new)
            LOG.info("Renaming %s -> %s", old, new)
            pathlib.Path(old).rename(new)


def add(files=None, force=False, interactive=False):
    # TODO do not overwrite existing files
    # TODO unit test
    # TODO implement interactive
    # TODO implement force
    paths = dfmpy.files.normalizer.normalize_file_names(files)
    paths = _filter_non_destination_paths(paths)
    expected_paths = _determine_expected_paths(paths)
    _move_expected_paths(expected_paths, force)
    # TODO make this the next method public, or move to the "files" utility?
    dfmpy.files.syncer.sync_expected_paths(expected_paths, force, interactive)
    # if interactive:
    #     raise NotImplementedError('Interactive not yet implemented.')
    # _install_file('config.ini', overwrite=force)
    # _install_file('ignore.globs', overwrite=force)


def _add_main(cli):
    # TODO unit test
    add(cli.files, cli.force, cli.interactive)


def setup_subparser(subparsers, default_args):
    # TODO unit test
    add_parser = subparsers.add_parser("add")
    add_parser.set_defaults(main=_add_main)
    add_parser.add_argument(*default_args.verbose_args, **default_args.verbose_kwargs)
    add_parser.add_argument(
        *default_args.force_args,
        **default_args.force_kwargs,
        help="Force overwriting of files."
    )
    add_parser.add_argument(
        *default_args.interactive_args,
        **default_args.interactive_kwargs,
        help="Interactively add files to the dotfiles repo, and then sync it."
    )
    add_parser.add_argument(
        "-F",
        "--files",
        dest="files",
        help="Add one or more files to the dotfiles repo, then sync it.",
        nargs="+",
    )
    return add_parser
