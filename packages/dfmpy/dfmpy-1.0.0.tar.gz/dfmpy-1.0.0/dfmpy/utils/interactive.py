import logging
import sys

LOG = logging.getLogger(__file__)


def check_for_interactivity():
    # TODO unit test
    # Cannot be interactive if there is no terminal to read from or write to!
    return sys.stdout.isatty() and sys.stdin.isatty()


def _prompt_user(message):
    # TODO docs - does not actually check "no" responses, just for a "yes."
    # TODO unit test
    response = input(f"{message} [y/N]: ").strip().lower()
    response = response and response[0] == "y"
    if response:
        LOG.debug("User accepted the prompt: %s", message)
    else:
        LOG.debug("User DID NOT accepted the prompt: %s", message)
    return response


def ask_to(message, force=False, interactive=True):
    # TODO unit test

    if force:
        # If "force" is true, then allow the operation.
        return True

    if not interactive:
        # If "force" is not true, and we do not want to ask the user, then for
        # safety do not allow the operation.
        return False

    # If "force" is not true, and we want to prompt the user, then ask them
    # what to do.
    return _prompt_user(message)
