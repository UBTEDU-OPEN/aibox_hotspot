#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: default_config.py
# Created: 2021-05-12 15:07:55
# Author: ChenglongXiong (chenglong.xiong@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# -----
# Description:配置
###
import os

class DeFaultConfig:
    #热点配置文件名
    hotspot_file = 'UbtHotSpot'
    #热点名
    hotspot_passwd = '12341234'

    #设备id可执行文件
    ubtsn_exe='/usr/local/UBTTools/ubtsn'

    #热点ini配置
    hotspot_ini = '/home/oneai/.config/hotspot/hotspot.ini'

    #弹框显示时长(s)
    display_timeout = 3

    #连接数超时查询(ms)
    connects_timeout = 5000

    #密码长度
    passwd_max = 50
    passwd_min = 8

    # 返回码
    ok = 0  # 成功
    timeout_error = -1  # 超时
    permissions_error = -2  # 权限错误
    file_error = -3  # 文件操作错误
    check_error = -4  # 校验错误
    params_error = -5  # 参数错误
    notfound_error = -6  # 未找到
    unknow_error = -50  # 未知错误 一般指python捕获的异常错误

    #wifi列表刷新状态文件路径
    wifis_status_path = '/proc/net/rtl88x2ce/wlan0/ap_sta_scan_ok'

    #wifi列表刷新周期(s)
    wifis_refresh_time = 13

    # 日志
    log_conf = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                # 格式
                'format': '%(asctime)s %(levelname)s %(name)s %(filename)s[line:%(lineno)d]: %(message)s'
            },
        },
        'handlers': {
            'file': {
                # 级别
                'level': 'DEBUG',
                # 日志文件轮转类
                'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
                'formatter': 'default',
                # 日志文件名
                'filename': 'test.log',
                # 日志文件大小
                'maxBytes': 50 * 1024 * 1024,
                # 日志文件个数
                'backupCount': 10,
                'delay': True
            }
        },
        'root': {
            'handlers': ['file'],
            'level': 'DEBUG',
        }
    }

    #配置目录
    conf_dir = '/home/oneai/.config/hotspot'