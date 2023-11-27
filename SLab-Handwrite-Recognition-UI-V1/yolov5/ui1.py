from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit
import sys
 
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QImage, QPixmap
import cv2
 
class Window(QWidget):
    def __init__(self):
        super().__init__()
 
        self.title = "PyQt5 Open File"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
 
        self.InitWindow()
 
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        vbox = QVBoxLayout()
 
        self.btn1 = QPushButton("Open Image")
        self.btn1.clicked.connect(self.getImage)
 
        vbox.addWidget(self.btn1)
 
        self.label_Origin = QLabel("Origin Image")
        self.label_Predicted = QLabel("Predicted Image")
        vbox.addWidget(self.label_Origin)
        vbox.addWidget(self.label_Predicted)
 
        self.setLayout(vbox)
 
 
    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        imagePath = fname[0]
        print(imagePath)
        pixmap = QPixmap(imagePath)
        img=cv2.imread(imagePath)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        h, w,r= img.shape
        #    print(img.shape)
        
        #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        ch = 3
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(
            img.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_BGR888,  # This is used to show the heatmap of the defect in output
        )
        # print("QPixmap.fromImage(convert_to_Qt_format)")
        # print(QPixmap.fromImage(convert_to_Qt_format))
        self.label_Origin.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
        self.label_Predicted.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
        ####self.label.setPixmap(QPixmap(pixmap))
        self.resize(pixmap.width(), pixmap.height())
 
App = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(App.exec_())