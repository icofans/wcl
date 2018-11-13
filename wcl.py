#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author : Jiaqiang

import time
import os
import subprocess
import datetime
import schedule
from yeelight import Bulb
from yeelight import discover_bulbs

# python 运行终端脚本
# sudo arp-scan -l
# sudo arp-scan --interface=enp3s0 -l| grep -i 5C:F7:E6:CA:ED:E5

# 灯的IP
bulb_ip = "192.168.10.2"
# 服务的网络接口
network_interface = "enp3s0"
# 手机mac地址
phone_mac_address = "5C:F7:E6:CA:ED:E5"


# 执行命令
def exec_cmd(cmd):
    """Run shell command"""
    cmd_env = os.environ.copy()
    cmd_env['PATH'] = '/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin'
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         env=cmd_env,
                         shell=True
                         )

    log_content = p.communicate()[0]

    return p.returncode, log_content

# 检查是否连上wifi
def check_wifi_connect():
    # output = os.popen('sudo arp-scan --interface=en0 -l| grep -i 40:8d:5c:81:ed:6b')
    # print(output.read())
    commond = "sudo arp-scan --interface=" + network_interface + " -l| grep -i " + phone_mac_address
    cmd_code, cmd_log = exec_cmd(commond)
    print(cmd_code)
    print(cmd_log)
    if cmd_code == 0:
        # 检测到wifi已连接
        return True
    else:
        # 检测到wifi已断开
        return False

# 检查时间段
def check_date_time():
    # 时间范围
    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'18:00', '%Y-%m-%d%H:%M')
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'23:59', '%Y-%m-%d%H:%M')
    # 当前时间
    n_time = datetime.datetime.now()
    # 判断
    if n_time > start_time and n_time<end_time:
        return True
    else:
        return False

# 控制灯
def control_yeelight(status):
    # 当前局域网存在灯设备
    if len(discover_bulbs()):
        # 连接到yeelight
        bulb = Bulb(bulb_ip)
        dic = bulb.get_properties()
        # {'sat': '100', 'color_mode': '2', 'ct': '6500', 'delayoff': '0', 'power': 'on', 'rgb': '16711680', 'hue': '359', 'music_on': '0', 'bright': '82', 'name': None, 'flowing': '0'}
        if dic.has_key('power'):
        	power = dic.get('power')
			if bulb and status == True and power == 'off':
            	bulb.turn_on()
	    	else:
        		print("未找到灯")

def schedule_task():
    schedule.every(0.1).minutes.do(do_check)
    while True:
        schedule.run_pending()
        time.sleep(1)

def do_check():
    print("执行定时任务")
    # 检查时间范围
    if(check_date_time() == True):
        # 判断是否回家
        if (check_wifi_connect() == True):
            # 判断灯的状态
            control_yeelight(True)

schedule_task()
