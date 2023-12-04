import sys
import cv2
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtWidgets import *
from functools import partial
import time
import os
from pathlib import Path

# from utils.move_on_list import moveOnList, moveOnImagrList

import numpy as np
import pickle

# from backend import date_module
from PyQt5.QtGui import QImage, QPixmap


from PyQt5.QtCore import QTimer
import cv2, random
import time
from backend.database2 import dataBase

from PyQt5 import QtCore, QtWidgets, uic
from yolov5.detect2 import run

from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
from datetime import date
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


# Import open3d as o3d
class Ui(QtWidgets.QMainWindow):

    """this class is used to build class for mainwindow to load GUI application

    :param QtWidgets: _description_
    """

    def __init__(self):
        """this function is used to laod ui file and build GUI application"""

        super(Ui, self).__init__()

        # load ui file
        #########uic.loadUi("slab.ui", self)
        uic.loadUi("main_UI.ui", self)

        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint))
        # button connector
        self.activate_()
        self.button_connector()
        self.Total_string = ""

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
        # self.GetCurrent.clicked.connect(self.connect1)  # Show the current defect
        self.live.clicked.connect(self.start_selection2)

    def start_selection(self):
        self.picktimer = QTimer()
        self.picktimer.timeout.connect(self.main)
        self.picktimer.start()

    def start_selection2(self):
        # self.picktimer2 = QTimer()
        # self.picktimer2.timeout.connect(self.show_farme)
        self.show_farme()
        # self.open_dir_dialog
        # self.picktimer2.start()

    def show_image(self, frame, labelshow):  # show the frame
        img = frame
        # print()
        img = cv2.resize(
            img,
            (1000, 280),  # this is relative to the camera
            interpolation=cv2.INTER_AREA,
        )

        try:
            h, w, ch = img.shape
            # print(img.shape)
        except:
            h, w = img.shape
            # print(img.shape)
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
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

        labelshow.setPixmap(QPixmap.fromImage(convert_to_Qt_format))

        # labelshow.setPixmap(
        #     QPixmap.fromImage(convert_to_Qt_format).transformed(
        #        QtGui.QTransform().rotate(90)
        #    )
        # )                 ########## This is used for rotate the image

    def open_dir_dialog(self):
        # dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        # dir_name = QtGui.QFileDialog.getExistingDirectory(
        #    self, "Open a folder", "/home/my_user_name/", QtGui.QFileDialog.ShowDirsOnly
        # )
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
        # fname = QFileDialog.getOpenFileName(self, "Open file")
        # dir_name = QFileDialog.getExistingDirectory(self, "Select a Directory")
        # for fname in os.listdir
        # if dir_name:
        # path = Path(dir_name)
        ##print("path")
        #  print(path)
        # self.dir_name_edit.setText(str(path))
        self.Message_LB.setText("")
        fname = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "All Files (*);;Python Files (*.py);;Text Files (*.txt)",
        )
        imagePath = fname[0]
        # print(imagePath)
        pixmap = QPixmap(imagePath)
        img = cv2.imread(imagePath)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imwrite("yolov5\\data\\slab\\slab\\1.jpg", img)
        # img = cv2.resize(img, (1000, 700), interpolation=cv2.INTER_AREA)
        # self.resize(pixmap.width(), pixmap.height())
        # self.resize(1200, h)
        # self.Showlive.resize(400, 400)
        self.Total_string = ""
        lay = QVBoxLayout(self.frame_27)
        title_label = QLabel()
        # title_label.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
        ####lay.addWidget(title_label)
        im, Final_list_cls, Final_img_detect_bounding_box = run()
        Index_y = [
            Final_img_detect_bounding_box[i][3]
            for i in range(0, len(Final_img_detect_bounding_box))
        ]
        Sort_Index_y = np.argsort(Index_y)  # I add it  to sort the the list value
        Final_list_cls_sorted = [Final_list_cls[i] for i in Sort_Index_y]
        Final_img_detect_bounding_box_0 = [
            Final_img_detect_bounding_box[i][0] for i in Sort_Index_y
        ]
        Final_img_detect_bounding_box_1 = [
            Final_img_detect_bounding_box[i][1] for i in Sort_Index_y
        ]
        Final_img_detect_bounding_box_2 = [
            Final_img_detect_bounding_box[i][2] for i in Sort_Index_y
        ]
        Final_img_detect_bounding_box_3 = [
            Final_img_detect_bounding_box[i][3] for i in Sort_Index_y
        ]

        for i in range(len(Final_list_cls_sorted)):
            bb0 = Final_img_detect_bounding_box_0[i]
            bb1 = Final_img_detect_bounding_box_1[i]
            bb2 = Final_img_detect_bounding_box_2[i]
            bb3 = Final_img_detect_bounding_box_3[i]
            cv2.rectangle(
                img,
                (bb0, bb2),
                (bb1, bb3),
                (0, 0, 255),
                3,
            )
            # uncomment to show label index
            cv2.putText(
                img,
                str(i + 1),
                (bb0, bb2 + 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                4,
                cv2.LINE_AA,
            )
            strings = [str(int(x)) for x in Final_list_cls_sorted[i]]
            strings = "".join(strings)
            self.Total_string = (
                self.Total_string
                + "\n"
                + str("Slab_")
                + str(i + 1)
                + str("=")
                + strings
            )
            ###########title_label = QLabel()

            # imh = cv2.resize(im[i], (1000, 700), interpolation=cv2.INTER_AREA)
            ##########imh = im[i]
            ##########h, w, r = imh.shape
            ##########ch = 3
            ##########bytes_per_line = ch * w
            ##########convert_to_Qt_format = QImage(
            ##########    imh.data,
            #######    w,
            ########    h,
            ########    bytes_per_line,
            ########    QImage.Format_BGR888,  # This is used to show the heatmap of the defect in output
        ####### )
        ########title_label.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
        ######lay.addWidget(title_label)
        img = cv2.resize(img, (1000, 700), interpolation=cv2.INTER_AREA)
        h, w, r = img.shape

        # print(h, w)
        # img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
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
        self.Showlive.setPixmap(QPixmap.fromImage(convert_to_Qt_format))  # remove it
        ##im = run()
        # Final_list_cls = []
        #########print(Final_list_cls)
        # print(strings)
        # self.label = QLabel("This is label", self.frame_27)
        # self.Showlive2.resize(400, 400)
        # print(im.shape)
        # label = QLabel(self.frame_27)
        # pixmap = QPixmap("cat.jpg")
        # label.setPixmap(pixmap)
        ##########self.Message_LB.setText(strings)
        self.Message_LB.setText(self.Total_string)
        self.setLayout(lay)
        ######self.label_Predicted.setPixmap(QPixmap.fromImage(convert_to_Qt_format))
        ####self.label.setPixmap(QPixmap(pixmap))

    def set_message(self, label_name, text, level=1):
        """Show warning with time delay 2 second , all labels for show warning has been set here"""

        # print('set_warning')
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
