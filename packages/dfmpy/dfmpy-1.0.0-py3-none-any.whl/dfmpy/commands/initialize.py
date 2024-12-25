import datetime
import importlib
import importlib.resources
import logging
import pathlib
import shutil

import xdgenvpy

LOG = logging.getLogger(__file__)

# TODO consider renaming this to a "config" command, where it can be initialized
#  or "edit" the configs, or list the config.

_XDG = xdgenvpy.xdgenv.XDGPedanticPackage("dfm")

_BACKUP_SUFFIX = datetime.datetime.now().strftime(".%Y%m%d_%H%M%S.dfmpy.backup")


def _install_file(resource_name, overwrite=False):
    # TODO unit test
    ref = importlib.resources.files("dfmpy.resources") / resource_name
    with importlib.resources.as_file(ref) as base_resource:
        LOG.debug("Found: %s", base_resource)

        installed_file = pathlib.Path(_XDG.XDG_CONFIG_HOME).joinpath(resource_name)
        if installed_file.exists() and not overwrite:
            LOG.error("Not overwriting: %s", installed_file)

        elif installed_file.exists() and overwrite:
            # TODO create a backup of the existing file!!
            # TODO make a checksum to see if overwriting is really necessary!
            backup_file = str(installed_file) + _BACKUP_SUFFIX
            shutil.move(installed_file, backup_file)
            LOG.warning("Backed up: %s", backup_file)
            shutil.copyfile(base_resource, installed_file)
            LOG.warning("Overwrote: %s", installed_file)

        else:
            shutil.copyfile(base_resource, installed_file)
            LOG.info("Installed: %s", installed_file)


def initialize(force=False, interactive=False):
    # TODO do not overwrite existing files
    # TODO unit test
    # TODO implement interactive
    if interactive:
        raise NotImplementedError("Interactive not yet implemented.")
    _install_file("config.ini", overwrite=force)
    _install_file("ignore.globs", overwrite=force)


def _initialize_main(cli):
    # TODO unit test
    initialize(cli.force, cli.interactive)


def setup_subparser(subparsers, default_args):
    # TODO unit test
    init_parser = subparsers.add_parser("init")
    init_parser.set_defaults(main=_initialize_main)
    init_parser.add_argument(*default_args.verbose_args, **default_args.verbose_kwargs)
    init_parser.add_argument(
        *default_args.force_args,
        **default_args.force_kwargs,
        help="Force overwriting of config files."
    )
    init_parser.add_argument(
        *default_args.interactive_args,
        **default_args.interactive_kwargs,
        help="Interactively overwrite files if there are conflicts."
    )
    return init_parser
