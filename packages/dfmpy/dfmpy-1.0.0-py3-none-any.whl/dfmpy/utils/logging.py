import logging
import sys


class NonColoredFormatter(logging.Formatter):

    @staticmethod
    def dependencies_met():
        # TODO unit test
        return True

    def format(self, record):
        # TODO unit test
        record.levelname = "[" + record.levelname[0] + "]"
        formatted_msg = super().format(record)
        return formatted_msg


class TermcolorFormatter(NonColoredFormatter):
    """
    Wrapper for https://pypi.org/project/termcolor/
    """

    # Sub-dict args should match colored() args
    _COLORS = {
        "CRITICAL": {"color": "white", "on_color": "on_red", "attrs": tuple(["bold"])},
        "FATAL": {"color": "white", "on_color": "on_red", "attrs": tuple(["bold"])},
        "ERROR": {"color": "red"},
        "WARNING": {"color": "yellow"},
        "INFO": {"color": "cyan"},
        "DEBUG": {},
    }

    @staticmethod
    def dependencies_met():
        # TODO unit test

        # Must be a TTY for colored output.
        if not sys.stdout.isatty():
            return False

        # This module depends on termcolor.
        try:
            # pylint: disable=import-outside-toplevel
            # pylint: disable=unused-import
            import termcolor
        except ModuleNotFoundError:
            return False

        return True

    def format(self, record):
        # TODO unit test
        # pylint: disable=import-outside-toplevel
        import termcolor

        colors = TermcolorFormatter._COLORS[record.levelname]
        formatted_msg = super().format(record)
        colored_msg = termcolor.colored(formatted_msg, **colors)
        return colored_msg


class ColoramaFormatter(logging.Formatter):
    """
    Wrapper for https://pypi.org/project/colorama/
    """

    @staticmethod
    def dependencies_met():
        # TODO unit test

        # Must be a TTY for colored output.
        if not sys.stdout.isatty():
            return False

        # This module depends on termcolor.
        try:
            # pylint: disable=import-outside-toplevel
            # pylint: disable=unused-import
            import colorama
        except ModuleNotFoundError:
            return False

        # return True
        return False  # b/c we did not yet implement format().

    def format(self, record):
        # TODO unit test
        raise NotImplementedError


def get_formatter(*args, **kwargs):
    # TODO unit test
    formatters = [ColoramaFormatter, TermcolorFormatter, NonColoredFormatter]
    formatters = [f for f in formatters if f.dependencies_met()]
    formatter = next(iter(formatters), NonColoredFormatter)
    return formatter(*args, **kwargs)
