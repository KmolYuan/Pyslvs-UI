# -*- coding: utf-8 -*-
from ..QtModules import *
import sys, logging

class QtHandler(logging.Handler):
    def __init__(self):
        logging.Handler.__init__(self)
    def emit(self, record):
        record = self.format(record)
        if record: XStream.stdout().write('{}\n'.format(record))

logger = logging.getLogger(__name__)
handler = QtHandler()
handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))
logger.addHandler(handler)

SYS_STDOUT = sys.stdout
SYS_STDERR = sys.stderr

class XStream(QObject):
    _stdout = None
    _stderr = None
    messageWritten = pyqtSignal(str)
    def flush(self): pass
    def fileno(self): return -1
    def write(self, msg):
        if not self.signalsBlocked(): self.messageWritten.emit(msg)
    @staticmethod
    def stdout():
        if not XStream._stdout:
            XStream._stdout = XStream()
            sys.stdout = XStream._stdout
        return XStream._stdout
    @staticmethod
    def stderr():
        if not XStream._stderr:
            XStream._stderr = XStream()
            sys.stderr = XStream._stderr
        return XStream._stderr
    def back():
        sys.stdout = SYS_STDOUT
        sys.stderr = SYS_STDERR
        XStream._stdout = None
        XStream._stderr = None
