# import logging
# import os
# from abc import ABC, abstractmethod
# from logging.handlers import RotatingFileHandler


def hello() -> str:
    return "Hello from gisboys-library!"


# class ILogHelper(ABC):
#     @abstractmethod
#     def debug(self, tekst: str):
#         pass

#     @abstractmethod
#     def info(self, tekst: str):
#         pass

#     @abstractmethod
#     def warning(self, tekst: str):
#         pass

#     @abstractmethod
#     def error(self, tekst: str, ex: Exception):
#         pass

#     @abstractmethod
#     def critical(self, tekst: str, ex: Exception):
#         pass


# class LogHelper(ILogHelper):
#     _Logfile = None
#     _Format = "%(asctime)s %(levelname)s %(message)s"
#     _Logger = None
#     _LogfileLevel = None
#     _ConsoleLogLevel = None
#     _handler = None
#     _Filesize = None
#     _Filecount = None
#     _ConsoleHandler = None

#     def __init__(
#         self,
#         logfile,
#         logfilelevel="info",
#         consoleloglevel="info",
#         filesize=5242880,
#         filecount=5,
#     ):
#         self._Logfile = logfile
#         self._LogfileLevel = logfilelevel
#         self._ConsoleLogLevel = consoleloglevel
#         self._Filesize = filesize
#         self._Filecount = filecount

#         if not os.path.exists(os.path.dirname(logfile)):
#             os.makedirs(os.path.dirname(logfile))

#         log_formatter = logging.Formatter(self._Format)
#         self._handler = RotatingFileHandler(
#             self._Logfile,
#             mode="a",
#             maxBytes=self._Filesize,
#             backupCount=self._Filecount,
#             encoding=None,
#             delay=0,
#         )
#         self._handler.setFormatter(log_formatter)
#         self._ConsoleHandler = logging.StreamHandler()
#         self._ConsoleHandler.setFormatter(log_formatter)

#         self._Logger = logging.getLogger("root")
#         self._Logger.setLevel(logging.DEBUG)

#         level = None
#         if self._LogfileLevel == "debug":
#             level = logging.DEBUG
#         elif self._LogfileLevel == "info":
#             level = logging.INFO
#         elif self._LogfileLevel == "warning":
#             level = logging.WARNING
#         elif self._LogfileLevel == "error":
#             level = logging.ERROR
#         elif self._LogfileLevel == "critical":
#             level = logging.CRITICAL

#         levelC = None
#         if self._ConsoleLogLevel == "debug":
#             levelC = logging.DEBUG
#         elif self._ConsoleLogLevel == "info":
#             levelC = logging.INFO
#         elif self._ConsoleLogLevel == "warning":
#             levelC = logging.WARNING
#         elif self._ConsoleLogLevel == "error":
#             levelC = logging.ERROR
#         elif self._ConsoleLogLevel == "critical":
#             levelC = logging.CRITICAL

#         self._handler.setLevel(level)
#         self._ConsoleHandler.setLevel(levelC)

#         self._Logger.addHandler(self._handler)
#         self._Logger.addHandler(self._ConsoleHandler)

#     def debug(self, tekst):
#         self._Logger.debug(tekst)

#     def info(self, tekst):
#         self._Logger.info(tekst)

#     def warning(self, tekst):
#         self._Logger.warning(tekst)

#     def error(self, tekst, ex):
#         self._Logger.error(tekst, exc_info=ex)

#     def critical(self, tekst, ex):
#         self._Logger.critical(tekst, exc_info=ex)
