# -*- coding: utf-8 -*-

"""Following script can output stdout and stderr to Qt text browser."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

import sys
import logging
from core.QtModules import QObject, pyqtSignal


class _QtHandler(logging.Handler):
    
    """Logging handle."""
    
    def __init__(self):
        logging.Handler.__init__(self)
    
    def emit(self, record: str):
        """Output to the other side."""
        record = self.format(record)
        if not record:
            return
        XStream.stdout().write('{}\n'.format(record))


_logger = logging.getLogger(__name__)
_handler = _QtHandler()
_handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
_logger.addHandler(_handler)

_SYS_STDOUT = sys.stdout
_SYS_STDERR = sys.stderr


class XStream(QObject):
    
    """Stream object to imitate Python output."""
    
    _stdout = None
    _stderr = None
    messageWritten = pyqtSignal(str)
    
    def flush(self):
        pass
    
    def fileno(self):
        return -1
    
    def write(self, msg: str):
        """Output the message."""
        if not self.signalsBlocked():
            self.messageWritten.emit(msg)
    
    @staticmethod
    def stdout():
        """Replace stdout."""
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout
    
    @staticmethod
    def stderr():
        """Replace stderr."""
        if not XStream._stderr:
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr
    
    def back():
        """Disconnect from Qt widget."""
        sys.stdout = _SYS_STDOUT
        sys.stderr = _SYS_STDERR
        XStream._stdout = None
        XStream._stderr = None
