import dfmpy.resources.config


def suffixes():
    # TODO unit test
    # Order of precedence:
    #   file.txt##hostname--system
    #   file.txt##hostname
    #   file.txt##systemname
    #   file.txt
    marker = dfmpy.resources.config.get_config().marker
    delimiter = dfmpy.resources.config.get_config().delimiter
    hostname = dfmpy.resources.config.get_config().hostname
    system_type = dfmpy.resources.config.get_config().system
    return tuple(
        [
            marker + delimiter.join([hostname, system_type]),
            marker + hostname,
            marker + system_type,
        ]
    )
