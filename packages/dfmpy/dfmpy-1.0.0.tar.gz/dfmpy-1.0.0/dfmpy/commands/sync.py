import logging

import dfmpy.resources.config
import dfmpy.files.deleter
import dfmpy.files.finder
import dfmpy.files.syncer

LOG = logging.getLogger(__file__)


# pylint: disable=duplicate-code
def sync(force=False, interactive=False):
    # TODO unit test

    install_dir = dfmpy.resources.config.get_config().install_dir
    repository_dir = dfmpy.resources.config.get_config().repository_dir

    expected_paths = dfmpy.files.finder.get_expected_paths(install_dir, repository_dir)
    installed_paths = dfmpy.files.finder.get_installed_paths(
        install_dir, repository_dir
    )

    if not force:
        LOG.error("Must use '-f' to force overwriting of symlinked dotfiles.")

    dfmpy.files.syncer.sync_expected_paths(expected_paths, force, interactive)
    dfmpy.files.deleter.remove_broken_files(installed_paths, force, interactive)


def _sync_main(cli):
    # TODO unit test
    sync(cli.force, cli.interactive)


def setup_subparser(subparsers, default_args):
    # TODO unit test
    sync_parser = subparsers.add_parser("sync")
    sync_parser.set_defaults(main=_sync_main)
    sync_parser.add_argument(*default_args.verbose_args, **default_args.verbose_kwargs)
    sync_parser.add_argument(
        *default_args.force_args,
        **default_args.force_kwargs,
        help="Overwrite files if there are conflicts."
    )
    sync_parser.add_argument(
        *default_args.interactive_args,
        **default_args.interactive_kwargs,
        help="Interactively overwrite files if there are conflicts."
    )
    return sync_parser
