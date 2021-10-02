# -*- coding: utf-8 -*-

"""Following script can output stdout and stderr to Qt text browser."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import cast, Optional, ClassVar
import sys
from os import remove
from os.path import join, expanduser
from platform import system
from logging import (
    DEBUG, INFO, ERROR, basicConfig, getLogger, Handler,
    StreamHandler, LogRecord,
)
from qtpy.QtCore import QObject, Signal
from .info import ARGUMENTS, SYS_INFO

logger = getLogger('matplotlib')
logger.setLevel(ERROR)
logger = getLogger()
_SYS_STDOUT = sys.stdout
_SYS_STDERR = sys.stderr
_std_handler = StreamHandler(_SYS_STDOUT)
_log_path = "pyslvs.log"
if system() not in {'Windows', 'Darwin'}:
    # Cause of AppImages can't use related path
    _log_path = join(expanduser("~"), _log_path)


def sign_in_logger() -> None:
    basicConfig(
        level=DEBUG if ARGUMENTS.debug_mode else INFO,
        filename=_log_path,
        format="[%(asctime)s] [%(funcName)s]:%(levelname)s: %(message)s",
    )
    logger.addHandler(_std_handler)
    for info_str in SYS_INFO:
        logger.info(info_str)
    logger.info('-' * 7)
    logger.addHandler(_QtHandler())


class _QtHandler(Handler):
    """Logging handle."""

    def __init__(self):
        super(_QtHandler, self).__init__()

    def emit(self, record: LogRecord) -> None:
        """Output to the other side."""
        msg = self.format(record)
        if msg and XStream.replaced():
            XStream.stdout().write(msg + '\n')

    def close(self) -> None:
        """Remove log file if exit."""
        super(_QtHandler, self).close()
        remove(_log_path)


class XStream(QObject):
    """Stream object to imitate Python output."""
    __stdout: ClassVar[Optional[XStream]] = None
    __stderr: ClassVar[Optional[XStream]] = None
    message_written = Signal(str)

    def write(self, msg: str) -> None:
        """Output the message."""
        if not self.signalsBlocked():
            self.message_written.emit(msg)

    @staticmethod
    def replaced() -> bool:
        return XStream.__stdout is not None

    @staticmethod
    def stdout() -> XStream:
        """Replace stdout."""
        if not XStream.replaced():
            XStream.__stdout = XStream()
            sys.stdout = XStream.__stdout
            logger.removeHandler(_std_handler)
        return cast(XStream, XStream.__stdout)

    @staticmethod
    def back() -> None:
        """Disconnect from Qt widget."""
        sys.stdout = _SYS_STDOUT
        sys.stderr = _SYS_STDERR
        XStream.__stdout = None
        XStream.__stderr = None
        logger.addHandler(_std_handler)
