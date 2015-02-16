import os
import sys
sys.dont_write_bytecode=True
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

sys.path.append("/usr/lib/duck_launcher")
import Apps

class QColorButton(QPushButton):
    '''
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).    
    '''

    colorChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QColorButton, self).__init__(*args, **kwargs)
        self.setObjectName("niceButton")
        self._color = None
        self.setMaximumWidth(32)
        self.pressed.connect(self.onColorPicker)
    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit()

        if self._color:
            self.setStyleSheet("QPushButton#niceButton {height:30px;border-style:solid;border-width:1px;border-color:rgb(40,40,40);border-radius:1px;background-color: %s;}" % self._color)
        else:
            self.setStyleSheet("")

    def color(self):
        return self._color

    def onColorPicker(self):
        '''
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        '''
        dlg = QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QColor(self._color))

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.setColor(None)

        return super(QColorButton, self).mousePressEvent(e)


class PicButton(QPushButton):
    def __init__(self,parent, pixmap):
        QPushButton.__init__(self,parent)
        self.pixmap = pixmap
        self.setFlat(True)
        self.setIcon(QIcon(pixmap))
        self.setStyleSheet('''QPushButton {background-color: rgba(0,0,0,0);border:none;outline:none;}
                    QPushButton:hover {background-color: rgba(30,30,30,20)}
                    QPushButton:pressed {background-color: rgba(30,30,30,40)}''')
    def sizeHint(self):
        return QPixmap(self.pixmap).size()


class AppWidget(QWidget):
    def __init__(self,parent,app,item):
        QWidget.__init__(self,parent)
        self.parent=parent
        self.item=item
        #self.resize(self.parent.width(),40)
        self.app=app
        self.layout = QHBoxLayout(self)
        self.appIcon=PicButton(self,Apps.ico_from_name(app["icon"]) )
        self.appIcon.setIconSize(QSize(32,32))
        self.appIcon.setMaximumWidth(40)
        self.appIcon.setMinimumHeight(32)
        self.layout.addWidget(self.appIcon)
        self.label=QLabel(self)
        self.label.setText(app["name"])
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
class AddAppWindow(QListWidget):
    appChosen=pyqtSignal(dict)
    def __init__(self,parent,*args,**kwargs):
        QListWidget.__init__(self,parent)
        self.setWindowTitle("Add an application")
        self.setStyleSheet("""
            QListWidget:item {
                height:50px;
                selection-background-color:rgb(150,150,150);
            }

            """)
        self.resize(300,300)
        self.apps=Apps.info('')
        for s in self.apps:
            i = QListWidgetItem()
            w= AppWidget(self,s,i)
            self.addItem(i)
            self.setItemWidget(i,w)

        self.itemClicked.connect(self.appSelected)
    def appSelected(self,i):
        app = self.itemWidget(i).app
        self.appChosen.emit(app)
        self.close()