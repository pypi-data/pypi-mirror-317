import os.path
import pathlib

import dfmpy.resources.config
import dfmpy.files.constants


def normalize_for_phantom_files(file_paths):
    # TODO docs - explain this shit!  explain why it's needed when determining
    #  expected files when there only exists a markered file (and not the
    #  equivalent non-marked file).
    # TODO use this with EXTREME caution, since it's a hack it causes too many
    #  side-effects in other places -- causing misleading bugs.
    # TODO optimize this? so it does not iterate over the list many times! (eg
    #  use of "in" keyword).
    # TODO unit test
    file_paths = list(file_paths)
    marker = dfmpy.resources.config.get_config().marker
    for file_path in file_paths:
        file_name = str(file_path)
        if marker in file_name:
            marker_index = file_name.find(marker)
            phantom_file_name = file_name[:marker_index]
            phantom_file_path = pathlib.Path(phantom_file_name)
            if phantom_file_path not in file_paths:
                file_paths.append(phantom_file_path)
    file_paths.sort()
    return tuple(file_paths)


def normalize_repo_path(file_path):
    # TODO unit test
    file_name = str(file_path)
    for suffix in dfmpy.files.constants.suffixes():
        file_with_suffix = file_name + suffix
        if pathlib.Path(file_with_suffix).exists():
            return pathlib.Path(file_with_suffix)
    return pathlib.Path(file_path)


def normalize_file_names(files):
    # TODO unit test
    if not files:
        files = []
    files = [os.path.expandvars(f) for f in files]
    paths = [pathlib.Path(f) for f in files]
    paths = [p.expanduser() for p in paths]
    paths = [p.absolute() for p in paths]
    return tuple(paths)
