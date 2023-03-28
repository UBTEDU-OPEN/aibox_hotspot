#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: common_utility.py
# Created: 2021-05-12 15:07:55
# Author: ChenglongXiong (chenglong.xiong@ubtrobot.com)
# Copyright 2020 - 2020 Ubtech Robotics Corp. All rights reserved.
# -----
# Description:工具接口
###
import subprocess
import logging
import PIL
from hotspot.common.config.default_config import DeFaultConfig
from PIL import Image, ImageQt

class CommonUtil():
    @classmethod
    def run_cmd(cls, cmd_str, timeout = None):
        """执行命令

        Args:
            cmd_str (string): 命令
            timeout (int, optional): 超时时间. 默认None.

        Returns:
            tuple: 执行成功与否,执行结果
        """
        child = subprocess.Popen(cmd_str, shell = True, stdout=subprocess.PIPE)
        ret = DeFaultConfig.ok
        result = {}
        try:
            #超时等待
            child.wait(timeout)
            ret = DeFaultConfig.ok if child.returncode == DeFaultConfig.ok else DeFaultConfig.unknow_error
        except Exception as e:
            #超时删除
            child.kill()
            logging.error('Error:{} {}'.format(e.__class__.__name__, e))
            ret = DeFaultConfig.timeout_error
        else:
            result = child.stdout.readlines()

        return ret, result

    @classmethod
    def has_chinese(cls, data):
        """执行命令

        Args:
            data (string): 待判断的数据

        Returns:
            bool: Trus,有中文字符
        """
        for ch in data:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True

        return False

    @classmethod
    def img_rotate(cls, img, val):
        """图片旋转

        Args:
            img (string):图片路径
            val (int):旋转角度

        Returns:
            ImageQt:旋转后的图片
        """
        pil_img = Image.open(img)
        pil_img = pil_img.rotate(val, resample = PIL.Image.BILINEAR)

        #PIL转QImage
        qt_img = ImageQt.ImageQt(pil_img)
        
        return qt_img
