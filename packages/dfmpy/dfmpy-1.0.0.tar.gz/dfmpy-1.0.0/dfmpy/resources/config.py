import configparser
import functools
import logging
import os.path
import pathlib
import platform
import socket

import xdgenvpy.xdgenv

LOG = logging.getLogger(__file__)

_XDG_ENV = xdgenvpy.xdgenv.XDGPackage("dfm")

# TODO add all defaults in here so that the config files are not required.
_CONFIG_DEFAULTS = {
    "delimiter": "--",
    "hostname": socket.gethostname(),
    "marker": "##",
    "system": platform.system(),
}


class DfmpyConfig:  # pylint: disable=too-few-public-methods

    def __init__(self, config):
        # TODO unit test
        self._config = config
        LOG.debug("Config: %s", dict(self._config))

    def __getattr__(self, attribute):
        # TODO unit test
        # TODO check CLI args for an override before checking the file
        value = str(self._config.get(attribute, None)).strip()

        # Normalize paths, if it looks like a path.
        if value:
            value = pathlib.Path(value).expanduser()
            value = str(value)

        # Normalize variables, if it hasit.
        if value:
            value = os.path.expandvars(value)

        return value


def _remove_comments(line):
    # TODO unit test
    try:
        return line[: line.index("#")]
    except ValueError:
        return line


@functools.lru_cache(maxsize=1)
def get_config():
    # TODO unit test
    # TODO supply a default set of args that was written to a default config file.
    config = configparser.ConfigParser(defaults=_CONFIG_DEFAULTS.copy())

    config_file = pathlib.Path(_XDG_ENV.XDG_CONFIG_HOME).joinpath("config.ini")
    if config_file.exists():
        LOG.debug("Reading config file: %s", config_file)
        config.read(config_file)

    valid_sections = ("dfmpy",)
    section = configparser.DEFAULTSECT
    for section_name in valid_sections:
        if config.has_section(section_name):
            section = section_name
    if not section:
        raise configparser.NoSectionError(
            f"Config {config_file}" f" must include a valid section: {valid_sections}"
        )
    LOG.debug("Using section %s from %s", section, config_file)
    try:
        return DfmpyConfig(config[section])
    except configparser.NoSectionError as exception:
        exception.message = f"{exception.message} in {config_file}"
        raise exception


def get_globs(file_path):
    # TODO unit test
    file_path = pathlib.Path(file_path)
    globs = []
    if file_path.exists():
        globs = file_path.read_text(encoding="UTF-8").splitlines()
        globs = [_remove_comments(line) for line in globs]
        globs = [line.strip() for line in globs]
        globs = [line for line in globs if line]
    return tuple(globs)


@functools.lru_cache(maxsize=1)
def get_ignore_globs():
    # TODO unit test
    ignore_file = pathlib.Path(_XDG_ENV.XDG_CONFIG_HOME).joinpath("ignore.globs")
    globs = get_globs(ignore_file)
    return tuple(globs)
