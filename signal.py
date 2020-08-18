# /***************************************************************
# Copyright © wkangk <wangkangchn@163.com>
# 文件名		: signal.py
# 作者	  	: wkangk <wangkangchn@163.com>
# 版本	   	: v1.0
# 描述	   	: 自定义信号
# 时间	   	: 2020-08-18 14:13
# ***************************************************************/
from PyQt5.QtCore import pyqtSignal, QObject

class CustomSignal(QObject):
    """ 自定义信号必须继承自QObject, 使用pyqtSignal()方法定义 """
    close_login = pyqtSignal()  # 关闭登录界面

global c
c = CustomSignal()