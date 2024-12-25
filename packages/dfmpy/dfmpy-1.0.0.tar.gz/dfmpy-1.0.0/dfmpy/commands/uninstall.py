import logging

import dfmpy.resources.config
import dfmpy.files.deleter
import dfmpy.files.finder

LOG = logging.getLogger(__file__)


def uninstall(force=False, interactive=False):
    # TODO unit test

    install_dir = dfmpy.resources.config.get_config().install_dir
    repository_dir = dfmpy.resources.config.get_config().repository_dir

    installed_paths = dfmpy.files.finder.get_installed_paths(
        install_dir, repository_dir
    )

    if not force:
        LOG.error("Must use '-f' to force removal of dotfiles.")

    for file in installed_paths:
        dfmpy.files.deleter.unlink_path(
            file,
            force,
            interactive,
            tuple([install_dir, repository_dir]),
        )


def _uninstall_main(cli):
    # TODO unit test
    uninstall(cli.force, cli.interactive)


def setup_subparser(subparsers, default_args):
    # TODO unit test
    uninstall_parser = subparsers.add_parser("uninstall")
    uninstall_parser.set_defaults(main=_uninstall_main)
    uninstall_parser.add_argument(
        *default_args.verbose_args, **default_args.verbose_kwargs
    )
    uninstall_parser.add_argument(
        *default_args.force_args,
        **default_args.force_kwargs,
        help="Force removal of all files."
    )
    uninstall_parser.add_argument(
        *default_args.interactive_args,
        **default_args.interactive_kwargs,
        help="Interactively remove of files."
    )
    return uninstall_parser
