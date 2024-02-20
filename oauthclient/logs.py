# todo: remove
# import copy
# import os
# import sys
# from logging.handlers import RotatingFileHandler
# from pathlib import Path
#
# from decouple import config
# from loguru import logger
#
#
# def get_loguru(file_name: str = "logurulog", log_to_file: bool = True) -> logger:
#     """Returns a loguru Logger instance with 2 handlers (file logger and console logger)
#     Separate instances with deepcopy
#     https://loguru.readthedocs.io/en/stable/resources/recipes.html#creating-independent-loggers-with-separate-set-of-handlers  # noqa
#     """
#     # remove the default since it isn't serializable and errors during deepcopy
#     logger.remove()
#     logger_ = copy.deepcopy(logger)
#     # Optionally disable logging output (disabled for the CI test runner)
#     if config("DISABLE_LOGGING", cast=bool, default=False):
#         logger.info("disabling logger")
#         logger.remove()
#         return logger_
#     else:
#         logger.info("logging not disabled")
#     # this creates the file logger
#     if log_to_file:
#         # create the PosixPath
#
#         log_path = Path(f"{settings.ROOT_DIR}") / "logs"
#         # make the directory if it doesn't already exist
#         log_path.mkdir(parents=True, exist_ok=True)
#         # append the filename to the PosixPath
#         log_file = log_path / f"{file_name}.log"
#         # add the group rotating handler to prevent duplicate log file renaming
#         group_handler = GroupWriteRotatingFileHandler(
#             # must convert the PosixPath type to string
#             str(log_file),
#             maxBytes=5120 * 1024,
#             backupCount=300,
#             encoding="utf-8",
#         )
#         logger_.configure(
#             handlers=[
#                 dict(sink=group_handler, level=config("LOG_LEVEL", default="INFO")),
#             ]
#         )
#     # add the default back.
#     # need to add formatting here to customize instead of inside configure since this is a new sink
#     # this adds the console logger
#     logger_.add(
#         sys.stderr,
#         format="{time:MM-DD-YY HH:mm:ss}|<level>{level}|{name}|{function}:{line}|{message}</level>",
#         level=config("LOG_LEVEL", default="INFO"),
#     )
#     return logger_
#
#
# class GroupWriteRotatingFileHandler(RotatingFileHandler):
#     def _open(self):
#         """
#         Override base class method to make the new log file group writable.
#         source:
#         https://stackoverflow.com/questions/1407474/does-python-logging-handlers-rotatingfilehandler-allow-creation-of-a-group-writa
#         :return:
#         :testing: utils.tests.test_general
#         """
#         prevumask = os.umask(0o002)
#         rtv = RotatingFileHandler._open(self)
#         os.umask(prevumask)
#         return rtv
