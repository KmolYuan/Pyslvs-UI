# -*- coding: utf-8 -*-

"""Following script can output stdout and stderr to Qt text browser."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import QObject, pyqtSignal
import sys
import logging

class QtHandler(logging.Handler):
    
    """Logging handle."""
    
    def __init__(self):
        logging.Handler.__init__(self)
    
    def emit(self, record: str):
        """Output to the other side."""
        record = self.format(record)
        if not record:
            return
        XStream.stdout().write('{}\n'.format(record))

logger = logging.getLogger(__name__)
handler = QtHandler()
handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
logger.addHandler(handler)

SYS_STDOUT = sys.stdout
SYS_STDERR = sys.stderr

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
        sys.stdout = SYS_STDOUT
        sys.stderr = SYS_STDERR
        XStream._stdout = None
        XStream._stderr = None
