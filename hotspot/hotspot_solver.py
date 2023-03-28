#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: hotspot.py
# Created: 2021-05-12 15:07:55
# Author: ChenglongXiong (chenglong.xiong@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# -----
# Description:热点配置
###

import logging
import configparser
import sys
import os
import time
import threading
import gettext
import fcntl
from hotspot.ui.hotspot_widget import HotspotWidget
from hotspot.common.utils.common_utility import CommonUtil
from hotspot.common.config.default_config import DeFaultConfig
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, pyqtSignal

class NewWidget(QWidget):
    """widget
    """
    #关闭信号
    close_striger = pyqtSignal(int)
    def __init__(self):
        super(NewWidget, self).__init__()
        self.m_flag = False

    def closeEvent(self, event):
        """重载关闭事件
        """
        self.close_striger.emit(0)
        event.accept()
        #确保所有线程退出
        os._exit(0)
    
    def mousePressEvent(self, event):
        """重载鼠标点击
        """
        if event.button() == Qt.LeftButton:
            self.m_Position = event.globalPos() - self.pos()
            y = self.m_Position.y()
            if y < 60:
                self.m_flag = True
            else:
                self.m_flag = False
            event.accept()
        else:
            self.m_flag = False

    def mouseMoveEvent(self, QMouseEvent):
        """重载鼠标移动事件
        """
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

class HotSpot(HotspotWidget):
    """热点配置
    """
    def __init__(self):
        """热点配置
        """
        super(HotSpot, self).__init__()
        self.hotspot_conf = DeFaultConfig.hotspot_ini  #热点配置
        self.hotspot_file = None                       #热点文件名
        self.hotspot_passwd = None                     #热点密码
        self.hotspot_ssid = ''                         #热点名
        self.hotspot_bootup = False                    #热点自启动
        self.hotspot_onoff = False                     #热点开关
        self.current_wifiname = None                   #当前连接的wifi名
        self.current_wifistatus = False                #当前wifi状态
        self.wifiname_lasttime = None                  #上次连接wifi名
        self.wifistatus_lasttime = False               #上次wifi连接状态
        self.hotspot_file_dir = '/etc/NetworkManager/system-connections/'
        self.hotspot_switch_timeout = 10

        #语言环境
        locale_dir = DeFaultConfig.conf_dir + '/locale/'
        ret = gettext.find("hotspot_locale", locale_dir)
        gettext.translation("hotspot_locale", localedir = locale_dir, languages = ['en'] if ret is None else None).install()

    def start(self):
        """启动界面
        """
        app = QApplication(sys.argv)
        self.mainwindow = NewWidget()
        self.mainwindow.close_striger.connect(self.save_hotspot_conf)
        self.setupUi(self.mainwindow)

        #获取热点配置
        ret = self.__get_hotspot_conf()

        # 获取wifi状态信息
        ret, self.current_wifistatus, self.current_wifiname = self.__get_wifi_status()
        if ret != DeFaultConfig.ok:
            logging.error('fail to get the status of wifi')
            return ret
        
        #热点状态更新
        if self.current_wifistatus:
            if self.current_wifiname == self.hotspot_file:
                self.hotspot_onoff = True
                self.wifistatus_lasttime = False
                self.current_wifistatus = False
            else:#更新wifi信息
                self.wifiname_lasttime = self.current_wifiname
                self.wifistatus_lasttime = self.current_wifistatus
                self.hotspot_onoff = False
        else:
            self.wifistatus_lasttime = False
            self.wifiname_lasttime = None
            self.hotspot_onoff = False
        
        logging.debug('wifi:{} {} hotspot:{} file:{}'.format(self.current_wifistatus, self.current_wifiname, self.hotspot_ssid, self.hotspot_file))
        logging.debug('last wifi:{} {} hotspot:{}'.format(self.wifistatus_lasttime, self.wifiname_lasttime, self.hotspot_ssid))
        #界面初始化
        ret = self.ui_init()

        #启动界面
        self.mainwindow.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.mainwindow.setAttribute(Qt.WA_TranslucentBackground)
        self.mainwindow.show()
        sys.exit(app.exec_())

    def get_hotspot_file(self):
        """获取热点文件名

        Returns:
            string:文件名
        """
        return self.hotspot_file

    def set_hotspot_file(self, name):
        """获取热点文件名

        Args:
            name (string): 文件名
        """
        self.hotspot_file = name

    def get_hotspot_passwd(self):
        """获取热点密码

        Returns:
            string:密码
        """
        return self.hotspot_passwd

    def set_hotspot_passwd(self, passwd):
        """设置热点密码

        Args:
            passwd (string):密码
        """
        self.hotspot_passwd = passwd

    def get_hotspot_ssid(self):
        """获取热点名称

        Returns:
            string:热点名称
        """
        return self.hotspot_ssid

    def set_hotspot_ssid(self, ssid):
        """设置热点名称

        Args:
            ssid (string):热点名称
        """
        self.hotspot_ssid = ssid

    def get_hotspot_bootup(self):
        """获取热点自启动开关

        Returns:
            bool:热点自启动, True 自启动
        """
        return self.hotspot_bootup

    def set_hotspot_bootup(self, bootup):
        """设置热点自启动开关

        Args:
            bootup (bool):热点自启动, True 自启动
        """
        self.hotspot_bootup = bootup

    def get_hotspot_onoff(self):
        """获取热点开关

        Returns:
            bool:热点开关, True 开
        """
        return self.hotspot_onoff

    def set_hotspot_onoff(self, onoff):
        """设置热点开关

        Args:
            onoff (bool):热点开关, True 开
        """
        self.hotspot_onoff = onoff

    def get_current_wifiname(self):
        """获取当前连接的wifi名

        Returns:
            string:wifi名,无wifi连接，则返回None
        """
        return self.current_wifiname

    def get_current_wifistatus(self):
        """获取当前wifi状态

        Returns:
            bool:wifi状态,true已连接wifi，false wifi断开
        """
        return self.current_wifistatus


    def __get_device_id(self):
        """获取设备id
        """
        # 执行获取设备sn命令
        ret, result_lines = CommonUtil.run_cmd(''.join((DeFaultConfig.ubtsn_exe, ' -r')), timeout = 5)
        
        # 获取失败
        if not len(result_lines):
            logging.error('fail to get sn:not found')
            return DeFaultConfig.notfound_error
        
        data = str(result_lines[0], encoding='utf-8').strip()
        vals = data.split('=')
        
        # 格式不对
        if len(vals) < 2:
            logging.error('fail to get sn:Wrong format')
            return DeFaultConfig.notfound_error, None

        return ret, vals[1]

    def __get_hotspot_conf(self):
        """获取热点配置信息

        Returns:
            int:成功返回DeFaultConfig.ok
        """
        # 读取热点配置文件
        try:
            hotspot_ini = configparser.ConfigParser()
            logging.debug('hotspot ini:{}'.format(self.hotspot_conf))
            hotspot_ini.read(self.hotspot_conf)
            self.hotspot_ssid = hotspot_ini['hotspot']['hotspot_ssid']
            self.hotspot_passwd = hotspot_ini['hotspot']['hotspot_passwd']
            self.hotspot_file = hotspot_ini['hotspot']['hotspot_file']
            self.hotspot_bootup = hotspot_ini.getboolean('hotspot', 'hotspot_bootup')
            self.hotspot_onoff = hotspot_ini.getboolean('hotspot', 'hotspot_onoff')
            self.wifiname_lasttime = hotspot_ini['wifi']['wifi_name_lasttime']
            self.wifistatus_lasttime = hotspot_ini['wifi']['wifi_status_lasttime']
            self.current_wifiname = self.hotspot_ssid
        except Exception as e:
            logging.error('{} {}'.format(e.__class__.__name__, e))
            return DeFaultConfig.unknow_error

        #更新配置
        path = self.hotspot_file_dir + '/' + self.hotspot_file
        if os.path.exists(path):
            try:
                network_hotspot = configparser.ConfigParser()
                network_hotspot.read(path)
                if network_hotspot.has_option('wifi', 'ssid'):
                    self.hotspot_ssid = network_hotspot['wifi']['ssid']
                if network_hotspot.has_option('wifi-security', 'psk'):
                    self.hotspot_passwd = network_hotspot['wifi-security']['psk']
                if network_hotspot.has_option('connection', 'autoconnect'):
                    self.hotspot_bootup = False
                else:
                    self.hotspot_bootup = True
            except Exception as e:
                logging.error('{} {}'.format(e.__class__.__name__, e))
                return DeFaultConfig.unknow_error
        
        ret = DeFaultConfig.ok
        if len(self.hotspot_ssid) == 0:
            ret, self.hotspot_ssid = self.__get_device_id()
            logging.debug('hotspot ssid:{}'.format(self.hotspot_ssid))

        return ret

    def __get_wifi_status(self):
        """获取当前wifi状态信息

        Returns:
            int, bool, string:成功返回DeFaultConfig.ok, true or false连接状态，wifi名
        """
        #执行获取wifi状态信息指令
        ret, results = CommonUtil.run_cmd('nmcli device show wlan0|awk \'NR==5,NR==6\'', timeout = 5)
        if ret != DeFaultConfig.ok:
            logging.error('fail to run cmd')
            return ret, False, None
        
        #判断获取数据是否正确
        if len(results) < 2:
            logging.error('wrong wifi status:{}'.format(results))
            return DeFaultConfig.unknow_error, False, None
        
        #获取状态信息
        datas = str(results[0], encoding='utf-8').strip()[40:]
        wifi_status = True if int(datas.strip().split(' ')[0]) == 100 else False
        
        # 获取wifi名
        wifi_name = None
        if wifi_status:
            logging.debug('wifi item:{}'.format(results[1]))
            datas = str(results[1], encoding='utf-8').strip('\n')[40:]
            wifi_name = datas
        
        return DeFaultConfig.ok, wifi_status, wifi_name

    def system_hotspot_onoff(self, onoff):
        """热点启动

        Args:
            onoff (boot):True打开，False关闭

        Returns:
            int:成功返回DeFaultConfig.ok
        """

        # 获取wifi状态信息
        ret, self.current_wifistatus, self.current_wifiname = self.__get_wifi_status()
        if ret != DeFaultConfig.ok:
            logging.error('fail to get the status of wifi')
            return ret
        
        #热点状态更新
        if self.current_wifistatus:
            if self.current_wifiname == self.hotspot_file:
                self.hotspot_onoff = True
                self.wifistatus_lasttime = False
                self.current_wifistatus = False
            else:#更新wifi信息
                self.wifiname_lasttime = self.current_wifiname
                self.wifistatus_lasttime = self.current_wifistatus
                self.hotspot_onoff = False
        else:
            self.wifistatus_lasttime = False
            self.wifiname_lasttime = None
            self.hotspot_onoff = False

        cmd_str = ''
        if onoff and not self.hotspot_onoff:
            #wifi连接先断开wifi
            if self.current_wifistatus and not self.hotspot_onoff:
                cmd_str = ''.join(('nmcli connection down \'', self.current_wifiname, '\''))
                logging.debug(cmd_str)
                ret, results = CommonUtil.run_cmd(cmd_str, timeout = self.hotspot_switch_timeout)
                if ret != DeFaultConfig.ok:
                    logging.error('fail to run cmd:{} cod:{}'.format(cmd_str, ret))
                    #return ret

            #热点不存在新建，存在则连接
            path = self.hotspot_file_dir + '/' + self.hotspot_file
            cmd_str = ''
            bootup_switch = False
            if os.path.exists(path):
                #先删除原配置
                cmd_str = ''.join(('nmcli connection del ',
                              self.hotspot_file))
                logging.debug(cmd_str)
                ret, results = CommonUtil.run_cmd(cmd_str, timeout=5)
                if ret != DeFaultConfig.ok:
                    cmd_str = ''.join(('rm -rf ',  self.hotspot_file))
                    logging.debug(cmd_str)
                    ret, results = CommonUtil.run_cmd(cmd_str, timeout=5)
            
            #启动
            cmd_str = ''.join(('nmcli device wifi hotspot ifname wlan0 con-name ',
                            self.hotspot_file, ' ssid ', self.hotspot_ssid,
                            ' password ', self.hotspot_passwd))
            if self.hotspot_bootup:
                bootup_switch = True

            logging.debug(cmd_str)

            ret = self.hotspot_switch_ready(timeout = 6)
            if ret != DeFaultConfig.ok:
                logging.error('hotspot switch not ready:{}'.format(ret))
                return ret

            ret, results = CommonUtil.run_cmd(cmd_str, timeout = self.hotspot_switch_timeout)
            if ret != DeFaultConfig.ok:
                logging.error('fail to run cmd:{} cod:{}'.format(cmd_str, ret))
                return ret
            
            if bootup_switch:
                self.system_hotspot_bootup(self.hotspot_bootup)
        elif not onoff and self.hotspot_onoff:
            #关闭
            cmd_str = ''.join(('nmcli connection down ', self.hotspot_file))
            logging.debug(cmd_str)
            
            ret = self.hotspot_switch_ready(timeout = 6)
            if ret != DeFaultConfig.ok:
                logging.error('hotspot switch not ready:{}'.format(ret))
                return ret
            
            ret, results = CommonUtil.run_cmd(cmd_str, timeout = self.hotspot_switch_timeout)
            if ret != DeFaultConfig.ok:
                logging.error('fail to run cmd:{} cod:{}'.format(cmd_str, ret))
                return ret
            
            #连接之前断开的wifi
            if self.wifistatus_lasttime:
                cmd_str = ''.join(('nmcli connection up \'', self.wifiname_lasttime, '\''))
                logging.debug(cmd_str)
                ret, results = CommonUtil.run_cmd(cmd_str, timeout = self.hotspot_switch_timeout)
                if ret != DeFaultConfig.ok:
                    logging.error('fail to run cmd:{} cod:{}'.format(cmd_str, ret))
                    self.wifistatus_lasttime = False
                    #return ret

        return DeFaultConfig.ok

    def system_hotspot_bootup(self, bootup):
        """热点自启动

        Args:
            bootup (boot):True打开，False关闭

        Returns:
            int:成功返回DeFaultConfig.ok
        """
        path = self.hotspot_file_dir + '/' + self.hotspot_file
        if os.path.exists(path):
            cmd_str = 'nmcli con modify ' + self.hotspot_file + ' connection.autoconnect ' + str('yes' if bootup else 'no')
            logging.debug('cmd:{}'.format(cmd_str))
            ret, results = CommonUtil.run_cmd(cmd_str, timeout=5)
            if ret != DeFaultConfig.ok:
                logging.error('fail to run cmd:{} cod:{}'.format(cmd_str, ret))
                return ret
        return DeFaultConfig.ok

    def system_hotspot_passwd(self, passwd):
        """热点密码修改

        Args:
            passwd (string):热点密码

        Returns:
            int:成功返回DeFaultConfig.ok
        """
        path = self.hotspot_file_dir + '/' + self.hotspot_file
        if os.path.exists(path):
            #密码修改
            cmd_str = 'nmcli con modify ' + self.hotspot_file + ' 802-11-wireless-security.psk ' + passwd
            logging.debug('cmd:{}'.format(cmd_str))
            ret, results = CommonUtil.run_cmd(cmd_str, timeout=5)
            if ret != DeFaultConfig.ok:
                logging.error('fail to run cmd:{} cod:{}'.format(cmd_str, ret))
                return ret

        return DeFaultConfig.ok

    def hotspot_devices_get(self):
        """获取热点连接设备数

        Returns:
            int:成功返回设备数量
        """
        results = []

        if self.hotspot_onoff:
            cmd_str = 'iw wlan0 station dump'
            logging.debug('cmd:{}'.format(cmd_str))
            ret, results = CommonUtil.run_cmd(cmd_str, timeout=5)
            if ret != DeFaultConfig.ok:
                logging.error('fail to run cmd:{} cod:{}'.format(cmd_str, ret))
                return -1
        
        return int(len(results)/3)

    def save_hotspot_conf(self):
        """保存热点配置

        Returns:
            int:成功返回DeFaultConfig.ok
        """
        try:
            hotspot_ini = configparser.ConfigParser()
            hotspot_ini.read(self.hotspot_conf)
            hotspot_ini.set('hotspot', 'hotspot_ssid', self.hotspot_ssid)
            hotspot_ini.set('hotspot', 'hotspot_passwd', self.hotspot_passwd)
            hotspot_ini.set('hotspot', 'hotspot_file', self.hotspot_file)
            hotspot_ini.set('hotspot', 'hotspot_bootup', 'True' if self.hotspot_bootup else 'False')
            hotspot_ini.set('hotspot', 'hotspot_onoff', 'True' if self.hotspot_onoff else 'False')
            hotspot_ini.set('wifi', 'wifi_status_lasttime', 'True' if self.wifistatus_lasttime else 'False')
            hotspot_ini.set('wifi', 'wifi_name_lasttime', '' if self.wifiname_lasttime is None else self.wifiname_lasttime)
        except Exception as e:
            logging.error('{} {}'.format(e.__class__.__name__, e))
            return  DeFaultConfig.unknow_error

        #写配置文件
        ret = DeFaultConfig.ok
        try:
            fp = open(self.hotspot_conf, "w+")
            fcntl.flock(fp.fileno(), fcntl.LOCK_EX)
            hotspot_ini.write(fp)
        except Exception as e:
            logging.error('{} {}'.format(e.__class__.__name__, e))
            ret = DeFaultConfig.unknow_error
        finally:
            fcntl.flock(fp.fileno(), fcntl.LOCK_UN)
            fp.close()

        return ret

    def window_close(self):
        """关闭窗口
        """
        self.mainwindow.close()

    def window_mini(self):
        """窗口最小化
        """
        self.mainwindow.setWindowState(Qt.WindowMinimized)

    def __wifis_refreshed_status(self, timeout = 0):
        """获取wifi列表状态

        Returns:
            bool: True已经刷新完，False正在刷新
        """
        
        nums = timeout * 10

        while True:
            if timeout:
                if nums > 0:
                    nums = nums - 1
                else:
                    return False
            time.sleep(0.1)
            #获取状态
            ret, results = CommonUtil.run_cmd(''.join(('cat ', DeFaultConfig.wifis_status_path)))
            if ret != DeFaultConfig.ok or len(results) <= 0:
                logging.error('Fail to get status:{} {}'.format(ret, len(results)))
                continue

            data = str(results[0], encoding='utf-8').strip()
            status_str = data.split( )
            logging.debug('refresh status:{}'.format(status_str))
            #刷新完退出
            if status_str[0] == '1':
               break
        
        return True

    def hotspot_switch_ready(self, timeout = 0):
        """网卡是否就绪
        通过判断底层wifi列表是否刷新完来返回网卡是否就绪标志

        Args:
            timeout (int, optional)：超时时间，默认0，一直阻塞
        Returns:
            int：DeFaultConfig.ok已就绪
        """
        #刷新wifi列表
        cmd_str = 'nmcli dev wifi rescan'
        ret, results = CommonUtil.run_cmd(cmd_str, timeout = 10)
        if ret != DeFaultConfig.ok:
            logging.debug('fail to refresh wifis:{}'.format(ret))
        time.sleep(1)
        ret = self.__wifis_refreshed_status(timeout)

        return DeFaultConfig.ok if ret else DeFaultConfig.unknow_error