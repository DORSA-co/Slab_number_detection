import sys
import cv2
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
from pathlib import Path
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2
from yolov5.detect2 import run

class Ui(QtWidgets.QMainWindow):

    """this class is used to build class for mainwindow to load GUI application

    :param QtWidgets: _description_
    """

    def __init__(self):
        """this function is used to laod ui file and build GUI application"""

        super(Ui, self).__init__()
        uic.loadUi("main_UI.ui", self)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))
        self.activate_()
        self.button_connector()

    def activate_(self):
        """main butoons connect -- exit , minize , maximize, help --"""
        self.close_btn.clicked.connect(self.close_win)
        self.minimize_btn.clicked.connect(self.minimize)
        self.maximize_btn.clicked.connect(self.maxmize_minimize)

    def minimize(self):
        """Minimize winodw"""
        self.showMinimized()

    def close_win(self):
        """Close window"""
        self.close()
        sys.exit()

    def maxmize_minimize(self):
        """Maximize or Minimize window"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def button_connector(self):
        self.live.clicked.connect(self.start_selection)

    def start_selection(self):
        self.show_farme()

    def show_image(self, frame, labelshow):  # show the frame
        img = frame
        h, w, r = img.shape
        ch = 3
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(
            img.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_BGR888,  
        )
        
        labelshow.setPixmap(QPixmap.fromImage(convert_to_Qt_format))

    def open_dir_dialog(self):

        dir_name = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "All Files (*);;Python Files (*.py);;Text Files (*.txt)",
        )
        if dir_name:
            path = Path(dir_name)
            self.dir_name_edit.setText(str(path))

    def show_farme(self):  # main algorithm

        self.Message_LB.setText("")

        ######   Read the original image
        fname = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "All Files (*);;Python Files (*.py);;Text Files (*.txt)",
        )
        imagePath = fname[0]
        img = cv2.imread(imagePath)       
        cv2.imwrite("yolov5\\data\\slab\\slab\\1.jpg", img)
        img = cv2.resize(img, (1000, 300), interpolation=cv2.INTER_AREA)
        self.show_image(img,self.Showlive)
        
        #####  Detection the number 
        im, Final_list_cls = run()
        strings = [str(int(x)) for x in Final_list_cls]    # Extract the predicted number in txt format
        strings = "".join(strings)
        im = cv2.resize(im, (1000, 300), interpolation=cv2.INTER_AREA)
        self.show_image(im,self.Showlive2)
        self.Message_LB.setText(strings)
      
    def set_message(self, label_name, text, level=1):
        """Show warning with time delay 2 second , all labels for show warning has been set here"""
        if text != None:
            if level == 1:
                label_name.setText(" " + text + " ")
                label_name.setStyleSheet(
                    "background-color:rgb(140, 140, 140);border-radius:2px;color:black"
                )

            QTimer.singleShot(10000, lambda: self.set_message(label_name, None))

        else:
            label_name.setText("")
            label_name.setStyleSheet("")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()
