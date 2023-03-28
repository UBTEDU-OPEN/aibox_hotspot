#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: hotspot_widget.py
# Created: 2021-05-12 15:07:55
# Author: ChenglongXiong (chenglong.xiong@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# -----
# Description:热点界面
###

import abc
import sys
import logging
import os
import time
import threading
import multiprocessing
from hotspot.ui.base_layout import Ui_main_widget
from hotspot.common.config.default_config import DeFaultConfig
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QObject, Qt
from hotspot.common.utils.common_utility import CommonUtil
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication

class HotspotWidget(Ui_main_widget):
    """热点界面
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        super(HotspotWidget, self).__init__()
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.rotate_val = 0          #loading角度
        self.data_pipe = multiprocessing.Pipe()

    def ui_init(self):
        """界面初始化
        """
        #输入框状态信息
        self.hotspot_passwd_input.setText(self.get_hotspot_passwd())
        self.hotspot_name_input.setText(self.get_hotspot_ssid())
        self.hotspot_name_input.setDisabled(True)
        self.hotspot_passwd_input.setDisabled(True)

        #弹框输入框状态信息
        self.name_input_frame.setText(self.get_hotspot_ssid())
        self.passwd_input_frame.setText(self.get_hotspot_passwd())
        self.name_input_frame.setDisabled(True)

        #状态更新
        self.__bootup_box_update(self.get_hotspot_bootup())
        self.__onoff_button_update(self.get_hotspot_onoff())

        #隐藏密码编辑弹框
        self.hide_level_set(self.dialog_main_frame, 0)

        #隐藏设置成功弹框
        self.hide_level_set(self.save_success_frame, 0)

        # 隐藏设置失败弹框
        self.hide_level_set(self.save_fail_frame, 0)
        
        #隐藏loading
        self.hide_level_set(self.loading_frame, 0)

        #隐藏热点开关toast
        self.hide_level_set(self.onoff_frame, 0)

        #信号与槽
        ##关闭
        self.title_close_label.clicked.connect(self.window_close)
        ##最小化
        self.title_mini_label.clicked.connect(self.window_mini)
        ##自启动
        self.bootup_check.mouse_trigger.connect(self.bootup_box_slot)
        ##开关
        self.onoff_button_lable.mouse_trigger.connect(self.onoff_button_slot)
        ##编辑
        self.hotspot_passwd_edit.mouse_trigger.connect(self.passwd_edit_slot)
        ##取消按钮
        self.cancel_frame.clicked.connect(self.cancel_frame_slot)
        self.cancel_info_frame.mouse_trigger.connect(self.cancel_frame_slot)
        ##保存按钮
        self.save_frame.clicked.connect(self.save_frame_slot)
        self.save_info_frame.mouse_trigger.connect(self.save_frame_slot)
        ##输入框
        self.passwd_input_frame.textEdited.connect(self.passwd_input_slot)
        ##实时显示连接数
        self.connects_label_timer = QTimer()
        self.connects_label_timer.timeout.connect(self.display_devices_connects)
        self.connects_label_timer.start(DeFaultConfig.connects_timeout)

    def display_devices_connects(self):
        """实时显示连接数
        """
        nums = self.hotspot_devices_get()
        display_str=''
        if nums > 0:
            display_str = _("ubt_hotspot_devices")
            display_str = display_str.replace('XX', str(nums))
        self.connects_label.setText(display_str)

    def passwd_input_slot(self):
        """密码输入框槽函数
        """
        input_text = self.passwd_input_frame.text()

        #去除空格
        self.passwd_input_frame.setText(input_text.strip())

        if len(input_text) < DeFaultConfig.passwd_min:
            self.save_info_frame.setDisabled(True)
            self.save_frame.setDisabled(True)
            self.save_frame.setStyleSheet("#save_frame{\n"
                                          "background: #9EB2C0;\n"
                                          "border-radius: 5px;\n"
                                          "border-radius: 5px;}")
        else:
            self.save_info_frame.setDisabled(False)
            self.save_frame.setDisabled(False)
            self.save_frame.setStyleSheet("#save_frame{\n"
                                          "background: #389FF1;\n"
                                          "border-radius: 5px;\n"
                                          "border-radius: 5px;}")

        if len(input_text) > DeFaultConfig.passwd_max:
            self.passwd_input_frame.setText(input_text[:len(input_text) - 1])

    def save_frame_slot(self):
        """保存按钮槽函数
        """
        passwd = self.passwd_input_frame.text()

        # 判断密码是否包含中文
        ch = CommonUtil.has_chinese(passwd)

        if not ch:#不包含中文
            self.__dialog_main_frame_lower(True)
            self.hide_level_set(self.dialog_main_frame, 0)

            #更新密码
            self.hotspot_passwd_input.setText(passwd)
            self.set_hotspot_passwd(passwd)

            self.system_hotspot_passwd(passwd)

            #显示设置成功
            timer = threading.Timer(DeFaultConfig.display_timeout, self.save_success_frame_timer)
            self.hide_level_set(self.save_success_frame, 0.7)
            timer.start()
        else:
            # 显示设置失败
            timer = threading.Timer(DeFaultConfig.display_timeout, self.save_fail_frame_timer)
            self.hide_level_set(self.save_fail_frame, 0.7)
            self.save_fail_frame.raise_()
            timer.start()

    def save_fail_frame_timer(self):
        self.hide_level_set(self.save_fail_frame, 0)
        self.save_fail_frame.lower()

    def save_success_frame_timer(self):
        self.hide_level_set(self.save_success_frame, 0)

    def cancel_frame_slot(self):
        """取消按钮槽函数
        """
        self.hide_level_set(self.save_fail_frame, 0)
        self.__dialog_main_frame_lower(True)
        self.hide_level_set(self.dialog_main_frame, 0)

    def passwd_edit_slot(self):
        """密码编辑按钮槽函数
        """
        self.__dialog_main_frame_lower(False)
        self.hide_level_set(self.dialog_main_frame, 1)

        #密码长度需要符合8-50
        passwd_len = len(self.passwd_input_frame.text())
        if passwd_len < DeFaultConfig.passwd_min or passwd_len > DeFaultConfig.passwd_max:
            self.save_info_frame.setDisabled(True)
            self.save_frame.setDisabled(True)
            self.save_frame.setStyleSheet("#save_frame{\n"
                                         "background: #9EB2C0;\n"
                                         "border-radius: 5px;\n"
                                         "border-radius: 5px;}")
        else:
            self.save_info_frame.setDisabled(False)
            self.save_frame.setDisabled(False)
            self.save_frame.setStyleSheet("#save_frame{\n"
                                          "background: #389FF1;\n"
                                          "border-radius: 5px;\n"
                                          "border-radius: 5px;}")

    def hide_level_set(self, target, level):
        """隐藏设置0透明，1不透明

        Args:
            level (int):透明度,0全透明，1不透明
            target (object):带设置的目标
        """
        op = QtWidgets.QGraphicsOpacityEffect()
        op.setOpacity(level)
        target.setGraphicsEffect(op)


    @abc.abstractmethod
    def window_close(self):
        pass

    @abc.abstractmethod
    def window_mini(self):
        pass

    def __dialog_main_frame_lower(self, lower):
        """隐藏设置0透明，1不透明

        Args:
            lower (bool):true底部，false顶部
        """
        self.dialog_main_frame.raise_()
        if lower:
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
            self.loading_frame.raise_()
            self.onoff_frame.raise_()
            self.hotspot_passwd_edit.raise_()
            self.bootup_check.raise_()
            self.title_close_label.raise_()
            self.title_mini_label.raise_()
            self.save_success_frame.raise_()
            self.onoff_button_lable.raise_()
            self.onoff_button_info.raise_()
            self.connects_label.raise_()
        # else:
        #     self.cancel_frame.raise_()
        #     self.cancel_info_frame.raise_()

    def onoff_button_slot(self):
        """热点开关槽函数
        """
        #toast状态，按钮禁止点击
        self.onoff_button_lable.setDisabled(True)
        onoff = not self.get_hotspot_onoff()
        logging.debug('hotspot onoff:{}'.format(onoff))
        if onoff:
            self.hotspot_passwd_edit.setDisabled(True)
            self.bootup_check.setDisabled(True)

        #打开loading
        self.hide_level_set(self.loading_frame, 0.7)
        #创建线程处理热点设置
        sub_thread = threading.Thread(target=self.onoff_system_threading, args=(onoff,))
        sub_thread.start()

        #动态loading
        while True:
            new_coming = self.data_pipe[0].poll(0.05)
            if new_coming:
                data = self.data_pipe[0].recv()
                break
            else:
                logging.debug('onoff_button_slot reflesh====')
                self.__update_loading_label()
        logging.debug('onoff_button_slot result :{}'.format(data))
        self.hide_level_set(self.loading_frame, 0)

        if data == DeFaultConfig.ok:
            self.onoff_button_lable.setDisabled(False)
            #设置指令
            self.set_hotspot_onoff(onoff)
            #更新ui
            self.__onoff_button_update(onoff)
        else:
            #失败提示
            self.onoff_info.setText(_('ubt_hotspot_set_failed'))
            self.onoff_info.setAlignment(Qt.AlignCenter)
            self.hide_level_set(self.onoff_frame, 0)
            timer = threading.Timer(DeFaultConfig.display_timeout, self.onoff_frame_timer)
            self.hide_level_set(self.onoff_frame, 0.7)
            timer.start()

    def bootup_box_slot(self):
        """热点自启动槽函数
        """
        #获取状态
        bootup = not self.get_hotspot_bootup()

        ret = self.system_hotspot_bootup(bootup)
        if ret != DeFaultConfig.ok:
            return
            
        #设置状态
        self.set_hotspot_bootup(bootup)
        #更新ui
        self.__bootup_box_update(bootup)

    def __bootup_box_update(self, bootup):
        icon1 = QtGui.QIcon()
        if not bootup:
            self.bootup_check.setPixmap(QtGui.QPixmap(self.current_dir + "/../assets/ic_checkbox.svg"))
        else:
            self.bootup_check.setPixmap(QtGui.QPixmap(self.current_dir + "/../assets/ic_checkbox_check.svg"))

    def __onoff_button_update(self, onoff):
        """热点开关状态更新

        Args:
            onoff (bool):热点开关，True打开，false关闭
        """
        if not onoff:
            self.onoff_button_info.setText(_('ubt_hotspot_off'))
            self.onoff_button_lable.setPixmap(QtGui.QPixmap(self.current_dir + "/../assets/ic_off.svg"))
        else:
            self.onoff_button_info.setText(_('ubt_hotspot_on'))
            self.onoff_button_lable.setPixmap(QtGui.QPixmap(self.current_dir + "/../assets/ic_on.svg"))

        if onoff:
            self.hotspot_passwd_edit.setPixmap(QtGui.QPixmap(self.current_dir + "/../assets/ic_edit_disable.svg"))
        else:
            self.hotspot_passwd_edit.setPixmap(QtGui.QPixmap(self.current_dir + "/../assets/ic_edit.svg"))

        #密码编辑按钮状态使能
        self.hotspot_passwd_edit.setDisabled(onoff)
        #自启动状态使能
        self.bootup_check.setDisabled(onoff)

    @abc.abstractmethod
    def get_hotspot_file(self):
        pass

    @abc.abstractmethod
    def set_hotspot_file(self, name):
        pass

    @abc.abstractmethod
    def get_hotspot_passwd(self):
        pass

    @abc.abstractmethod
    def set_hotspot_passwd(self, passwd):
        pass

    @abc.abstractmethod
    def get_hotspot_ssid(self):
        pass

    @abc.abstractmethod
    def set_hotspot_ssid(self, ssid):
        pass

    @abc.abstractmethod
    def get_hotspot_bootup(self):
        pass

    @abc.abstractmethod
    def set_hotspot_bootup(self, bootup):
        pass

    @abc.abstractmethod
    def get_hotspot_onoff(self):
        pass

    @abc.abstractmethod
    def set_hotspot_onoff(self, onoff):
        pass

    @abc.abstractmethod
    def get_current_wifiname(self):
        pass

    @abc.abstractmethod
    def get_current_wifistatus(self):
        pass

    @abc.abstractmethod
    def system_hotspot_onoff(self, onoff):
        pass

    @abc.abstractmethod
    def system_hotspot_bootup(self, bootup):
        pass

    @abc.abstractmethod
    def save_hotspot_conf(self):
        pass

    @abc.abstractmethod
    def system_hotspot_passwd(self, passwd):
        pass

    @abc.abstractmethod
    def hotspot_devices_get(self):
        pass

    def __update_loading_label(self):
        """更新loading

        """
        #旋转角度
        logging.debug('__update_loading_label ===========')
        self.rotate_val = self.rotate_val%360 + 10
        try:
            image = CommonUtil.img_rotate(self.current_dir + "/../assets/ic_loading.png", self.rotate_val)
        except Exception as e:
            logging.error('img_rotate:{} {}'.format(e.__class__.__name__, e))
            return
        self.loading_img.setPixmap(QPixmap.fromImage(image))
        QApplication.processEvents()
    
    def onoff_system_threading(self, onoff):
        """执行系统命令

        Args:
            onoff(boot):True打开，False关闭
        """
        #执行指令
        logging.debug('run system hostpot cmd:{}'.format(onoff))
        ret = self.system_hotspot_onoff(onoff)
        self.data_pipe[1].send(ret)

    def onoff_frame_timer(self):
        """隐藏label

        """
        self.hide_level_set(self.onoff_frame, 0)
        self.onoff_button_lable.setDisabled(False)