import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Form(QWidget):

    def __init__(self, parent = None):
    
        QWidget.__init__(self, parent)
        
        self.undoStack = QUndoStack()
        
        undoAction = self.undoStack.createUndoAction(self, self.tr("&Undo"))
        undoAction.setShortcuts(QKeySequence.Undo)
        redoAction = self.undoStack.createRedoAction(self, self.tr("&Redo"))
        redoAction.setShortcuts(QKeySequence.Redo)
        
        nameEdit = QLineEdit()
        addressEdit = QLineEdit()
        
        undoButton = QToolButton()
        undoButton.setDefaultAction(undoAction)
        redoButton = QToolButton()
        redoButton.setDefaultAction(redoAction)
        
        nameEdit.editingFinished.connect(self.storeFieldText)
        addressEdit.editingFinished.connect(self.storeFieldText)
        
        formLayout = QFormLayout()
        formLayout.addRow(self.tr("&Name"), nameEdit)
        formLayout.addRow(self.tr("&Address"), addressEdit)
        
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(undoButton)
        buttonLayout.addWidget(redoButton)
        
        layout = QHBoxLayout(self)
        layout.addLayout(formLayout)
        layout.addLayout(buttonLayout)
        
        self.setWindowTitle(self.tr("Undo Example"))
    
    def storeFieldText(self):
    
        command = StoreCommand(self.sender())
        self.undoStack.push(command)


class StoreCommand(QUndoCommand):

    def __init__(self, field):
    
        QUndoCommand.__init__(self)
        
        # Record the field that has changed.
        self.field = field
        
        # Record the text at the time the command was created.
        self.text = field.text()

    def undo(self):
    
        # Remove the text from the file and set it in the field.
        # ...
        self.field.setText(self.text)
    
    def redo(self):
    
        # Store the text in the file and set it in the field.
        # ...
        self.field.setText(self.text)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
