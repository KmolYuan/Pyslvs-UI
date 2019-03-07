# -*- coding: utf-8 -*-

"""Following script can output stdout and stderr to Qt text browser."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Optional
import sys
import os
from logging import (
    DEBUG,
    INFO,
    basicConfig,
    getLogger,
    Handler,
    StreamHandler,
)
from .info import ARGUMENTS
from core.QtModules import QObject, Signal


class _QtHandler(Handler):

    """Logging handle."""

    def __init__(self):
        super(_QtHandler, self).__init__()

    def emit(self, record: str):
        """Output to the other side."""
        record = self.format(record)
        if record:
            XStream.stdout().write(record + '\n')


_SYS_STDOUT = sys.stdout
_SYS_STDERR = sys.stderr
_log_file_name = "./pyslvs.log"

basicConfig(
    level=DEBUG if ARGUMENTS.debug_mode else INFO,
    filename=_log_file_name,
    format="[%(asctime)s] [%(funcName)s]:%(levelname)s: %(message)s",
)
logger = getLogger()
logger.addHandler(_QtHandler())
logger.setLevel(DEBUG)
_std_handler = StreamHandler(_SYS_STDOUT)
logger.addHandler(_std_handler)


class XStream(QObject):

    """Stream object to imitate Python output."""

    _stdout: Optional[XStream] = None
    _stderr: Optional[XStream] = None
    message_written = Signal(str)

    @staticmethod
    def flush():
        """Remove log file if exit."""
        os.remove(_log_file_name)

    def write(self, msg: str):
        """Output the message."""
        if not self.signalsBlocked():
            self.message_written.emit(msg)

    @staticmethod
    def stdout() -> XStream:
        """Replace stdout."""
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
            logger.removeHandler(_std_handler)
        return XStream._stdout

    @staticmethod
    def back():
        """Disconnect from Qt widget."""
        sys.stdout = _SYS_STDOUT
        sys.stderr = _SYS_STDERR
        XStream._stdout = None
        XStream._stderr = None
        logger.addHandler(_std_handler)
