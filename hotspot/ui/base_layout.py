# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'base_layout.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPainter, QPainterPath, QImage, QPixmap

class UserLable(QtWidgets.QLabel):
    """label

    Args:
        QtWidgets.QLabel (object): QLabel
    """
    # 鼠标信号 0单击
    mouse_trigger = pyqtSignal(int)
    def __init__(self, form):
        super(UserLable, self).__init__(form)
        self.left_clicked = False

    def mousePressEvent(self, QMouseEvent):
        """重载鼠标单击事件

        Args:
            QMouseEvent (object): QMouseEvent
        """
        if QMouseEvent.buttons() == QtCore.Qt.LeftButton:
            self.left_clicked = True
        else:
            self.left_clicked = False
                
    def mouseReleaseEvent(self, QMouseEvent):
        """重载鼠标释放事件

        Args:
            QMouseEvent (object): QMouseEvent
        """
        if self.left_clicked:
            self.mouse_trigger.emit(0)

class Ui_main_widget(object):
    def setupUi(self, main_widget):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        main_widget.setObjectName("main_widget")
        main_widget.resize(700, 480)
        self.main_frame = QtWidgets.QFrame(main_widget)
        self.main_frame.setGeometry(QtCore.QRect(0, 0, 700, 480))
        self.main_frame.setStyleSheet("#main_frame{background: #FFFFFF;\n"
"border: 1px solid #9EB2C0;\n"
"border-radius: 10px;\n"
"border-radius: 10px;}")
        self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_frame.setObjectName("main_frame")
        self.title_label = QtWidgets.QLabel(self.main_frame)
        self.title_label.setGeometry(QtCore.QRect(0, 0, 700, 60))
        self.title_label.setStyleSheet("#title_label{background: #E9EEF4;\n"
"border-top: 1px solid #9EB2C0;\n"
"border-left: 1px solid #9EB2C0;\n"
"border-right: 1px solid #9EB2C0;\n"
"border-top-left-radius: 10px;\n"
"border-top-right-radius: 10px;\n"
"border-bottom-left-radius: 0px;\n"
"border-bottom-right-radius: 0px;}")
        self.title_label.setText("")
        self.title_label.setObjectName("title_label")
        
        pix_old = QtGui.QPixmap(current_dir + "/../assets/ic_hotlink.svg")
        pix_new = QtGui.QPixmap(26, 26)
        pix_new.fill(Qt.transparent)
        pat = QPainter()
        pat.begin(pix_new)
        pat.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        path = QPainterPath()
        path.addRoundedRect(0, 0, 26, 26, 3, 3)
        pat.setClipPath(path)
        pat.drawPixmap(0, 0, 26, 26, pix_old)
        pat.end()

        self.title_icon_label = QtWidgets.QLabel(self.main_frame)
        self.title_icon_label.setGeometry(QtCore.QRect(20, 15, 30, 30))
        self.title_icon_label.setText("")
        self.title_icon_label.setPixmap(pix_new)
        self.title_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_icon_label.setObjectName("title_icon_label")
        self.title_info_label = QtWidgets.QLabel(self.main_frame)
        self.title_info_label.setGeometry(QtCore.QRect(62, 15, 150, 30))
        self.title_info_label.setStyleSheet("#title_info_label{\n"
"font-family: SourceHanSansCN-Normal;\n"
"font-size: 16px;\n"
"color: #4C545B;\n"
"text-align: center;}")
        self.title_info_label.setAlignment(QtCore.Qt.AlignVCenter)
        self.title_info_label.setObjectName("title_info_label")
        self.onoff_info_label1 = QtWidgets.QLabel(self.main_frame)
        self.onoff_info_label1.setGeometry(QtCore.QRect(50, 105, 200, 20))
        self.onoff_info_label1.setStyleSheet("#onoff_info_label1{\n"
"font-family: SourceHanSansCN-Medium;\n"
"font-weight: 500;\n"
"font-size: 16px;\n"
"color: #4C545B;}")
        self.onoff_info_label1.setObjectName("onoff_info_label1")
        self.onoff_info_label2 = QtWidgets.QLabel(self.main_frame)
        self.onoff_info_label2.setGeometry(QtCore.QRect(50, 131, 393, 80))
        self.onoff_info_label2.setStyleSheet("#onoff_info_label2{\n"
"font-family: SourceHanSansCN-Regular;\n"
"font-size: 13px;\n"
"color: #4C545B;\n"
"line-height: 20px;\n"
"}")
        self.onoff_info_label2.setWordWrap(True)
        self.onoff_info_label2.setObjectName("onoff_info_label2")
        self.hotspot_name_label = QtWidgets.QLabel(self.main_frame)
        self.hotspot_name_label.setGeometry(QtCore.QRect(50, 238, 56, 14))
        self.hotspot_name_label.setStyleSheet("#hotspot_name_label{\n"
"font-family: SourceHanSansCN-Medium;\n"
"font-weight: 500;\n"
"font-size: 14px;\n"
"color: #4C545B;}")
        self.hotspot_name_label.setObjectName("hotspot_name_label")
        self.hotspot_passwd_label = QtWidgets.QLabel(self.main_frame)
        self.hotspot_passwd_label.setGeometry(QtCore.QRect(50, 298, 68, 14))
        self.hotspot_passwd_label.setStyleSheet("#hotspot_passwd_label{\n"
"font-family: SourceHanSansCN-Medium;\n"
"font-weight: 500;\n"
"font-size: 14px;\n"
"color: #4C545B;}")
        self.hotspot_passwd_label.setObjectName("hotspot_passwd_label")
        self.bootup_into_label1 = QtWidgets.QLabel(self.main_frame)
        self.bootup_into_label1.setGeometry(QtCore.QRect(80, 369, 170, 18))
        #QtCore.QRect(156, 370, 25, 19)
        self.bootup_into_label1.setStyleSheet("#bootup_into_label1{\n"
"font-family: SourceHanSansCN-Medium;\n"
"font-weight: 500;\n"
"font-size: 16px;\n"
"color: #4C545B;}")
        self.bootup_into_label1.setObjectName("bootup_into_label1")
        self.bootup_into_label2 = QtWidgets.QLabel(self.main_frame)
        self.bootup_into_label2.setGeometry(QtCore.QRect(50, 398, 266, 50))
        self.bootup_into_label2.setStyleSheet("#bootup_into_label2{\n"
"font-family: SourceHanSansCN-Regular;\n"
"font-size: 13px;\n"
"color: #4C545B;}")
        self.bootup_into_label2.setWordWrap(True)
        self.bootup_into_label2.setObjectName("bootup_into_label2")
        self.hotspot_name_input = QtWidgets.QLineEdit(self.main_frame)
        self.hotspot_name_input.setGeometry(QtCore.QRect(128, 225, 400, 40))
        self.hotspot_name_input.setStyleSheet("#hotspot_name_input{\n"
"background: #E9EEF4;\n"
"border-radius: 6px;\n"
"font-family: SourceHanSansCN-Medium;\n"
"font-size: 14px;\n"
"color: #4C545B;\n"
"padding-left: 12px;}")
        self.hotspot_name_input.setReadOnly(True)
        self.hotspot_name_input.setObjectName("hotspot_name_input")
        self.hotspot_passwd_input = QtWidgets.QLineEdit(self.main_frame)
        self.hotspot_passwd_input.setGeometry(QtCore.QRect(128, 285, 400, 40))
        self.hotspot_passwd_input.setStyleSheet("#hotspot_passwd_input{\n"
"background: #E9EEF4;\n"
"border-radius: 6px;\n"
"font-family: SourceHanSansCN-Medium;\n"
"font-size: 14px;\n"
"color: #4C545B;\n"
"padding-left: 12px;}")
        self.hotspot_passwd_input.setReadOnly(True)
        self.hotspot_passwd_input.setObjectName("hotspot_passwd_input")
        
        self.hotspot_passwd_edit = UserLable(self.main_frame)
        self.hotspot_passwd_edit.setGeometry(QtCore.QRect(548, 294, 28, 22))
        self.hotspot_passwd_edit.setText("")
        self.hotspot_passwd_edit.setObjectName("bootup_check")
        self.hotspot_passwd_edit.setPixmap(QtGui.QPixmap(current_dir + "/../assets/ic_edit_disable.svg"))

        self.bootup_check = UserLable(self.main_frame)
        self.bootup_check.setGeometry(QtCore.QRect(50, 370, 25, 19))
        self.bootup_check.setText("")
        self.bootup_check.setObjectName("bootup_check")

        self.title_close_label = QtWidgets.QPushButton(self.main_frame)
        self.title_close_label.setGeometry(QtCore.QRect(666, 15, 24, 24))
        #self.title_close_label.setStyleSheet("#title_close_label{background: transparent;}")
        self.title_close_label.setFlat(True)
        self.title_close_label.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(current_dir + "/../assets/ic_pop_close.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.title_close_label.setIcon(icon2)
        self.title_close_label.setIconSize(QtCore.QSize(24, 24))
        self.title_close_label.setObjectName("title_close_label")
        self.title_mini_label = QtWidgets.QPushButton(self.main_frame)
        self.title_mini_label.setGeometry(QtCore.QRect(637, 15, 24, 24))
        #self.title_mini_label.setStyleSheet("#title_mini_label{background: transparent;}")
        self.title_mini_label.setFlat(True)
        self.title_mini_label.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(current_dir + "/../assets/ic_pop_minimize.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.title_mini_label.setIcon(icon3)
        self.title_mini_label.setIconSize(QtCore.QSize(24, 24))
        self.title_mini_label.setObjectName("title_mini_label")
        self.dialog_main_frame = QtWidgets.QFrame(self.main_frame)
        self.dialog_main_frame.setGeometry(QtCore.QRect(0, 0, 700, 480))
        self.dialog_main_frame.setStyleSheet("#dialog_main_frame{\n"
"background: rgba(39,51,123,0.30);\n"
"border-radius: 10px;\n"
"border-radius: 10px;}")
        self.dialog_main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dialog_main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dialog_main_frame.setObjectName("dialog_main_frame")
        self.hotpot_frame = QtWidgets.QFrame(self.dialog_main_frame)
        self.hotpot_frame.setGeometry(QtCore.QRect(98, 135, 500, 260))
        self.hotpot_frame.setStyleSheet("#hotpot_frame{\n"
"opacity: 0.3;\n"
"background: #FFFFFF;\n"
"border-radius: 10px;\n"
"border-radius: 10px;}")
        self.hotpot_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.hotpot_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hotpot_frame.setObjectName("hotpot_frame")
        self.name_info_frame = QtWidgets.QLabel(self.hotpot_frame)
        self.name_info_frame.setGeometry(QtCore.QRect(46, 54, 70, 14))
        self.name_info_frame.setStyleSheet("#name_info_frame{\n"
"font-family: SourceHanSansCN-Normal;\n"
"font-size: 14px;\n"
"color: #4C545B;}")
        self.name_info_frame.setObjectName("name_info_frame")
        self.passwd_info_frame = QtWidgets.QLabel(self.hotpot_frame)
        self.passwd_info_frame.setGeometry(QtCore.QRect(46, 114, 70, 14))
        self.passwd_info_frame.setStyleSheet("#passwd_info_frame{\n"
"font-family: SourceHanSansCN-Normal;\n"
"font-size: 14px;\n"
"color: #4C545B;}")
        self.passwd_info_frame.setObjectName("passwd_info_frame")
        self.info_frame = QtWidgets.QLabel(self.hotpot_frame)
        self.info_frame.setGeometry(QtCore.QRect(128, 156, 310, 30))
        self.info_frame.setStyleSheet("#info_frame{\n"
"font-family: SourceHanSansCN-Regular;\n"
"font-size: 12px;\n"
"color: #4C545B;\n"
"line-height: 14px;}")
        self.info_frame.setWordWrap(True)
        self.info_frame.setObjectName("info_frame")
        self.name_input_frame = QtWidgets.QLineEdit(self.hotpot_frame)
        self.name_input_frame.setGeometry(QtCore.QRect(124, 41, 300, 40))
        self.name_input_frame.setStyleSheet("#name_input_frame{\n"
"background: #E9EEF4;\n"
"border-radius: 6px;\n"
"border-radius: 6px;\n"
"padding-left: 12px;\n"
"font-family: SourceHanSansCN-Medium;\n"
"font-size: 14px;\n"
"color: #4C545B;}")
        self.name_input_frame.setObjectName("name_input_frame")
        self.passwd_input_frame = QtWidgets.QLineEdit(self.hotpot_frame)
        self.passwd_input_frame.setGeometry(QtCore.QRect(124, 101, 300, 40))
        self.passwd_input_frame.setStyleSheet("#passwd_input_frame{\n"
"border: 1px solid #389FF1;\n"
"border-radius: 6px;\n"
"border-radius: 6px;\n"
"padding-left: 12px;\n"
"font-family: SourceHanSansCN-Medium;\n"
"font-size: 14px;\n"
"color: #4C545B;}")
        self.passwd_input_frame.setObjectName("passwd_input_frame")
        self.cancel_frame = QtWidgets.QPushButton(self.hotpot_frame)
        self.cancel_frame.setGeometry(QtCore.QRect(140, 197, 100, 34))
        self.cancel_frame.setStyleSheet("#cancel_frame{\n"
"background: #9EB2C0;\n"
"border-radius: 5px;\n"
"border-radius: 5px;}")
        self.cancel_frame.setText("")
        self.cancel_frame.setObjectName("cancel_frame")
        self.save_frame = QtWidgets.QPushButton(self.hotpot_frame)
        self.save_frame.setGeometry(QtCore.QRect(260, 197, 100, 34))
        self.save_frame.setStyleSheet("#save_frame{\n"
"background: #9EB2C0;\n"
"border-radius: 5px;\n"
"border-radius: 5px;}")
        self.save_frame.setText("")
        self.save_frame.setObjectName("save_frame")
        self.cancel_info_frame = UserLable(self.hotpot_frame)
        self.cancel_info_frame.setGeometry(QtCore.QRect(140, 197, 100, 34))
        self.cancel_info_frame.setStyleSheet("#cancel_info_frame{\n"
"font-family: SourceHanSansCN-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"text-align: center;}")
        self.cancel_info_frame.setAlignment(Qt.AlignCenter)
        self.cancel_info_frame.setObjectName("cancel_info_frame")
        self.save_info_frame = UserLable(self.hotpot_frame)
        self.save_info_frame.setGeometry(QtCore.QRect(260, 197, 100, 34))
        self.save_info_frame.setStyleSheet("#save_info_frame{\n"
"opacity: 0.3;\n"
"font-family: SourceHanSansCN-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"text-align: center;}")
        self.save_info_frame.setAlignment(Qt.AlignCenter)
        self.save_info_frame.setObjectName("save_info_frame")

        self.save_fail_frame = QtWidgets.QFrame(self.main_frame)
        self.save_fail_frame.setGeometry(QtCore.QRect(230, 220, 240, 40))
        self.save_fail_frame.setStyleSheet("#save_fail_frame{\n"
                                              "opacity: 0.7;\n"
                                              "background: #171E2B;\n"
                                              "border-radius: 7px;\n"
                                              "border-radius: 7px;}")
        self.save_fail_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.save_fail_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.save_fail_frame.setObjectName("save_fail_frame")
        self.save_fail_info = QtWidgets.QLabel(self.save_fail_frame)
        self.save_fail_info.setGeometry(QtCore.QRect(0, 0, 240, 40))
        self.save_fail_info.setStyleSheet("#save_fail_info{\n"
                                             "font-family: SourceHanSansCN-Regular;\n"
                                             "font-size: 14px;\n"
                                             "color: #FFFFFF;\n"
                                             "letter-spacing: 0;\n"
                                             "text-align: center;\n"
                                             "line-height: 14px;}")
        self.save_fail_info.setAlignment(Qt.AlignCenter)
        self.save_fail_info.setWordWrap(True)
        self.save_fail_info.setObjectName("save_fail_info")

        self.save_success_frame = QtWidgets.QFrame(self.main_frame)
        self.save_success_frame.setGeometry(QtCore.QRect(250, 220, 200, 40))
        self.save_success_frame.setStyleSheet("#save_success_frame{\n"
"opacity: 0.7;\n"
"background: #171E2B;\n"
"border-radius: 7px;\n"
"border-radius: 7px;}")
        self.save_success_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.save_success_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.save_success_frame.setObjectName("save_success_frame")
        self.save_success_info = QtWidgets.QLabel(self.save_success_frame)
        self.save_success_info.setGeometry(QtCore.QRect(0, 0, 200, 40))
        self.save_success_info.setStyleSheet("#save_success_info{\n"
"font-family: SourceHanSansCN-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"letter-spacing: 0;\n"
"text-align: center;\n"
"line-height: 14px;}")
        self.save_success_info.setAlignment(Qt.AlignCenter)
        self.save_success_info.setObjectName("save_success_info")

        #self.onoff_button_lable = QtWidgets.QLabel(self.main_frame)
        self.onoff_button_lable = UserLable(self.main_frame)
        self.onoff_button_lable.setGeometry(QtCore.QRect(512, 134, 65, 36))
        self.onoff_button_lable.setText("")
        self.onoff_button_lable.setObjectName("onoff_button_lable")

        self.onoff_button_info = QtWidgets.QLabel(self.main_frame)
        self.onoff_button_info.setGeometry(QtCore.QRect(583, 134, 80, 36))
        self.onoff_button_info.setStyleSheet("#onoff_button_info{\n"
                                             "font-family: SourceHanSansCN-Regular;\n"
                                             "font-size: 14px;\n"
                                             "color: #4C545B;}")
        self.onoff_button_info.setObjectName("onoff_button_info")
        self.onoff_button_info.setAlignment(Qt.AlignVCenter)

        self.connects_label = QtWidgets.QLabel(self.main_frame)
        self.connects_label.setGeometry(QtCore.QRect(460, 390, 180, 20))
        self.connects_label.setStyleSheet("#connects_label{\n"
"font-family: SourceHanSansCN-Medium;\n"
"font-size: 16px;\n"
"color: #4C545B;\n"
"line-height: 14px;}")
        self.connects_label.setObjectName("connects_label")
        self.connects_label.setText('')

        self.loading_frame = QtWidgets.QFrame(self.main_frame)
        self.loading_frame.setGeometry(QtCore.QRect(260, 150, 180, 180))
        self.loading_frame.setStyleSheet("#loading_frame{\n"
                                         "opacity: 0.6;\n"
                                         "background: #171E2B;\n"
                                         "border-radius: 9.47px;\n"
                                         "border-radius: 9.47px;}")
        self.loading_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.loading_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.loading_frame.setObjectName("loading_frame")
        self.loading_img = QtWidgets.QLabel(self.loading_frame)
        self.loading_img.setGeometry(QtCore.QRect(65, 65, 60, 60))
        self.loading_img.setScaledContents(True)
        self.loading_img.setObjectName("loading_img")
        image = QImage()
        image.load(self.current_dir + "/../assets/ic_loading.png")
        self.loading_img.setPixmap(QPixmap.fromImage(image))

        self.onoff_frame = QtWidgets.QFrame(self.main_frame)
        self.onoff_frame.setGeometry(QtCore.QRect(250, 220, 200, 40))
        self.onoff_frame.setStyleSheet("#onoff_frame{\n"
                                              "opacity: 0.7;\n"
                                              "background: #171E2B;\n"
                                              "border-radius: 7px;\n"
                                              "border-radius: 7px;}")
        self.onoff_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.onoff_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.onoff_frame.setObjectName("onoff_frame")
        self.onoff_info = QtWidgets.QLabel(self.onoff_frame)
        self.onoff_info.setGeometry(QtCore.QRect(51, 6, 98, 28))
        self.onoff_info.setStyleSheet("#onoff_info{\n"
                                             "font-family: SourceHanSansCN-Regular;\n"
                                             "font-size: 14px;\n"
                                             "color: #FFFFFF;\n"
                                             "letter-spacing: 0;\n"
                                             "text-align: center;\n"
                                             "line-height: 14px;}")
        self.onoff_info.setObjectName("onoff_info")

        self.dialog_main_frame.raise_()
        self.title_label.raise_()
        self.title_icon_label.raise_()
        self.title_info_label.raise_()
        self.onoff_info_label1.raise_()
        self.onoff_info_label2.raise_()
        self.hotspot_name_label.raise_()
        self.hotspot_passwd_label.raise_()
        self.bootup_into_label1.raise_()
        self.bootup_into_label2.raise_()
        self.hotspot_name_input.raise_()
        self.hotspot_passwd_input.raise_()
        self.hotspot_passwd_edit.raise_()
        self.loading_frame.raise_()
        self.onoff_frame.raise_()
        self.bootup_check.raise_()
        self.title_close_label.raise_()
        self.title_mini_label.raise_()
        self.save_success_frame.raise_()
        self.onoff_button_lable.raise_()
        self.onoff_button_info.raise_()
        self.connects_label.raise_()

        main_widget.setWindowTitle(_("ubt_hotspot_set"))
        main_widget.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(current_dir + "/../assets/ic_hotlink.svg")))
        self.retranslateUi(main_widget)
        QtCore.QMetaObject.connectSlotsByName(main_widget)

    def retranslateUi(self, main_widget):
        _translate = QtCore.QCoreApplication.translate
        self.title_info_label.setText(_translate("main_widget", _("ubt_hotspot_set")))
        self.onoff_info_label1.setText(_translate("main_widget", _("ubt_hotspot_connect")))
        self.onoff_info_label2.setText(_translate("main_widget", _("ubt_hotspot_info1") + "\n" +
_("ubt_hotspot_info2")))
        self.hotspot_name_label.setText(_translate("main_widget", _("ubt_hotspot_ssid")))
        self.hotspot_passwd_label.setText(_translate("main_widget", _("ubt_hotspot_pssd")))
        self.bootup_into_label1.setText(_translate("main_widget", _("ubt_hotspot_auto_on")))
        self.bootup_into_label2.setText(_translate("main_widget", _("ubt_hotspot_auto_info")))
        self.name_info_frame.setText(_translate("main_widget", _("ubt_hotspot_ssid")))
        self.passwd_info_frame.setText(_translate("main_widget", _("ubt_hotspot_pssd")))
        self.info_frame.setText(_translate("main_widget", _("ubt_hotspot_pssd_set_info")))
        self.cancel_info_frame.setText(_translate("main_widget", _("ubt_hotspot_cancel")))
        self.save_info_frame.setText(_translate("main_widget", _("ubt_hotspot_save")))
        self.save_success_info.setText(_translate("main_widget", _("ubt_hotspot_passwd_ok")))
        self.save_fail_info.setText(_translate("main_widget", _("ubt_hotspot_pssd_error_info")))

