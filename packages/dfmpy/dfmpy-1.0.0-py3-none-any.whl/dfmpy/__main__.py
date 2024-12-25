#!/usr/bin/env python3

# pylint: disable=wrong-import-position

import platform

# TODO unit test
__PYTHON_MAJOR_VERSION = int(platform.python_version_tuple()[0])
if __PYTHON_MAJOR_VERSION < 3:
    raise SystemError("dfmpy requires Python 3.6+, not " + platform.python_version())

# TODO unit test
__PYTHON_MIN_VERSION = int(platform.python_version_tuple()[1])
if __PYTHON_MIN_VERSION < 6:
    raise SystemError("dfmpy requires Python 3.6+, not " + platform.python_version())

import argparse
import dataclasses
import importlib.metadata
import logging
import sys

import dfmpy.commands.add
import dfmpy.commands.initialize
import dfmpy.commands.ls
import dfmpy.commands.uninstall
import dfmpy.commands.sync
import dfmpy.utils.interactive
import dfmpy.utils.logging

LOG = logging.getLogger(__file__)

_LOG_LEVELS = tuple(
    [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]
)


def _get_version_str():
    # TODO unit test
    return "%(prog)s " + importlib.metadata.version("dfmpy")


def _setup_logger(verbosity_index=None):
    # TODO unit test
    if not verbosity_index:
        verbosity_index = 1
    verbosity_index = max(0, min(len(_LOG_LEVELS) - 1, verbosity_index))
    log_level = _LOG_LEVELS[verbosity_index]
    # formatter = Formatter('%(asctime)s %(levelname)s %(message)s')
    formatter = dfmpy.utils.logging.get_formatter("%(levelname)s %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(log_level)
    logger.addHandler(handler)
    logger.debug("Using formatter: %s", formatter.__class__.__name__)


@dataclasses.dataclass(frozen=True)
class DefaultArgs:
    verbose_args: tuple
    verbose_kwargs: dict  # TODO how to make it a frozen dict?
    force_args: tuple
    force_kwargs: dict  # TODO how to make it a frozen dict?
    interactive_args: tuple
    interactive_kwargs: dict  # TODO how to make it a frozen dict?


def _parse_arguments():
    # TODO unit test
    # TODO go through all "help" docs and make sure they are consistent.
    # TODO move subparser initialization to each of the command modules.

    default_args = DefaultArgs(
        verbose_args=tuple(["-v", "--verbose"]),
        verbose_kwargs={
            "action": "count",
            "default": 1,
            "dest": "verbosity",
            "help": "Set verbosity level, multiple flags increase the level.",
        },
        force_args=tuple(["-f", "--force"]),
        force_kwargs={
            "action": "store_true",
            "default": False,
            "dest": "force",
        },
        interactive_args=tuple(["-i", "--interactive"]),
        interactive_kwargs={
            "action": "store_true",
            "default": False,
            "dest": "interactive",
        },
    )

    parser = argparse.ArgumentParser(prog="dfmpy")
    main_verbose_kwargs = default_args.verbose_kwargs.copy()
    del main_verbose_kwargs["dest"]
    parser.add_argument(
        *default_args.verbose_args, **main_verbose_kwargs, dest="main_verbosity"
    )
    parser.add_argument("-V", "--version", action="version", version=_get_version_str())
    subparsers = parser.add_subparsers(help="sub-command help")

    dfmpy.commands.add.setup_subparser(subparsers, default_args)
    dfmpy.commands.initialize.setup_subparser(subparsers, default_args)
    dfmpy.commands.ls.setup_subparser(subparsers, default_args)
    dfmpy.commands.sync.setup_subparser(subparsers, default_args)
    dfmpy.commands.uninstall.setup_subparser(subparsers, default_args)

    args = parser.parse_args()
    if not hasattr(args, "main"):
        parser.print_help()
        parser.exit()

    # Since a argument cannot exist on both the main parser as well as a
    # sub-parser we need to normalize here.  They technically can both exist,
    # but the sub-parser overwrites any value calculated from parsing the main
    # arguments.
    if "main_verbosity" in args:
        args.verbosity += args.main_verbosity - 1

    return args


def main():
    # TODO unit test?
    args = _parse_arguments()
    _setup_logger(args.verbosity)
    try:
        LOG.debug("Arguments: %s", args)

        if (
            "interactive" in args
            and args.interactive
            and not dfmpy.utils.interactive.check_for_interactivity()
        ):
            raise RuntimeError("Cannot run interactively while not attached to a TTY.")

        args.main(args)

    except KeyboardInterrupt:
        print("")
        LOG.warning("Leaving dfmpy prematurely.")

    # except Exception as e:
    #     LOG.critical(e)
    #     LOG.exception(e)

    except BaseException as exception:  # pylint: disable=broad-except
        # LOG.critical(exception)
        LOG.exception(exception)


if __name__ == "__main__":
    main()
