
import sys
import os
import logging
import logging.config
#调整模块搜索路径顺序
back = sys.path[1:]
back.append(sys.path[0])
sys.path = back

from hotspot.hotspot_solver import HotSpot
from hotspot.common.config.default_config import DeFaultConfig
from hotspot.common.utils.common_utility import CommonUtil
import fcntl

if __name__ == '__main__':
    #初始化日志
    log_path = os.path.expanduser("~") + "/.cache/hotspot/"
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_name = log_path + "HotSpot.log"
    DeFaultConfig.log_conf['handlers']['file']['filename'] = file_name
    logging.config.dictConfig(DeFaultConfig.log_conf)
    logging.debug('start')
    
    #防止多开
    fd = open(os.path.realpath(sys.argv[0]), "r")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except Exception as e:
        logging.debug('app is already running')
        exit(0)

    tHotSpot = HotSpot()
    tHotSpot.start()