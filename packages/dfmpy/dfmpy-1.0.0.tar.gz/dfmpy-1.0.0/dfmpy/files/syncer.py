import logging

import dfmpy.files
import dfmpy.files.deleter
import dfmpy.utils.interactive

LOG = logging.getLogger(__file__)


def link_path(symlink_path, target_path, force, interactive):
    # TODO unit test
    if dfmpy.utils.interactive.ask_to(
        f"Overwrite to link file: {symlink_path}", force, interactive
    ):
        dfmpy.files.mkdir_parents(symlink_path)
        symlink_path.symlink_to(target_path)
        LOG.warning("Symlinked: %s -> %s", symlink_path, target_path)
    else:
        LOG.info("Simulated symlink: %s -> %s", symlink_path, target_path)


def sync_expected_paths(expected_paths, force, interactive):
    # TODO unit test
    LOG.info("Syncing files.")
    force_it_kwargs = {"force": True, "interactive": False}
    for symlink_path, target_path in expected_paths.items():

        if dfmpy.files.path_is_symlink(symlink_path):
            if symlink_path.resolve() == target_path:
                # The symlink exists and points to the correct target.
                LOG.debug("No need to sync: %s -> %s", symlink_path, target_path)
            else:
                # If the symlink exists, but it points to the wrong target!
                sync_prompt = f"Sync broken link: {symlink_path}"
                if dfmpy.utils.interactive.ask_to(sync_prompt, force, interactive):
                    dfmpy.files.deleter.unlink_path(symlink_path, **force_it_kwargs)
                    link_path(symlink_path, target_path, **force_it_kwargs)

        elif dfmpy.files.path_is_file(symlink_path):
            sync_prompt = f"Replace existing file: {symlink_path}"
            if dfmpy.utils.interactive.ask_to(sync_prompt, force, interactive):
                dfmpy.files.deleter.unlink_path(symlink_path, **force_it_kwargs)
                link_path(symlink_path, target_path, **force_it_kwargs)

        else:
            # The file/link does not exist, so create it.
            link_path(symlink_path, target_path, force, interactive)
