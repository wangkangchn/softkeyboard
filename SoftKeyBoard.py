import sys
import datetime
from dateutil.parser import parse

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication
from UI.Ui_SoftKeyBoard import Ui_SoftKeyBoard

if __name__ == '__main__':
    from utils import logger
    global log
    log = logger.setup_logger('logging.log')
else:
    log = None

# 数字到特殊字符的映射关系
shift_map_num = {
'1': '!',
'2': '@',
'3': '#',
'4': '$',
'5': '%',
'6': '^',
'7': '&',
'8': '*',
'9': '(',
'0': ')',}

shift_map_punctuation = {
'dec': ['-', '_'],
'add': ['=', '+'],
'left_bracket': ['[', '{'],
'right_bracket': [']', '}'],
'semicolon': [';', ':'],
'quota': ['\'', '"'],
'comma': [',', '<'],
'dot': ['.', '>'],
'backslash': ['/', '?'],
'slash': ['\\', '|'],}

func_keys = ['backspace', 'enter', 'shift', 'capslock', 'space',
            'clear', 'up', 'down', 'left', 'right']

class SoftKeyBoard(QWidget, Ui_SoftKeyBoard):

    signal_send_text = QtCore.pyqtSignal(str)

    def __init__(self):
        super(SoftKeyBoard, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('SoftBoard')

        # 上一次点击大写键的时间
        self.last_click_caps_time = parse('1996-03-04 23:43:10.123')

        self.double_Caps = False
        self.Caps = False
        self.Shift = False
        self.data = None

        self.set_log(log)

        # 数字键连接到槽函数
        for i in range(10):
            exec("""self.num_{0}_.clicked.connect(
                    self.btn_num_{0}_clicked)""".format(i))

        # 字母键连接到槽函数
        for i in range(97, 123):
            exec("""self.char_{0}_.clicked.connect(
                    self.btn_char_{0}_clicked)""".format(chr(i)))

        # 功能键连接到槽函数
        for i in func_keys:
            exec("""self.btn_{0}_.clicked.connect(
                    self.btn_{0}_clicked)""".format(i))

        # 标点键连接到槽函数
        for i in shift_map_punctuation.keys():
            exec("""self.btn_{0}_.clicked.connect(
                    self.btn_{0}_clicked)""".format(i))

    # 双击大写键连接到槽函数
    def mouseDoubleClickEvent(self, e):
        log.debug('双击了！{}'.format(e.button()))

    def set_log(self, logger):
        self.log = logger

    def get_key_symbol(self, name, num=False):
        """ 获取函数名对应的按键 """
        i = 9
        if num:
            i = 8
        symbol = name.strip()[i]
        return symbol

    def num2symbol(self, num):
        """ 获取数字键上字符 """
        symbol = shift_map_num[num]
        return symbol

    def get_func_key_name(self, name):
        """ 获取功能键名字 """
        right = name.rfind('_', 0)
        left = name.find('_', 0)
        return name[left+1:right]

    def get_punctuation(self, key_name, shift):
        """ 键名转换为标点符号 """
        punctuations = shift_map_punctuation[key_name]
        if shift:
            return punctuations[1]
        return punctuations[0]

    def change_caps_style(self):
        """ 修改大写键风格, 单击时, 在下一次单击前保持绿色, 双击持续绿色 """
        if self.Caps or self.double_Caps:
            self.btn_capslock_.setStyleSheet("background-color:green")
        else:
            self.btn_capslock_.setStyleSheet("background-color:rgb(67,63,59)");

    def change_shift_style(self):
        """ 修改shift风格, 单击时, 在下一次单击前保持绿色, 双击持续绿色 """
        if self.Shift:
            self.btn_shift_.setStyleSheet("background-color:green")
        else:
            self.btn_shift_.setStyleSheet("background-color:rgb(67,63,59)");

    def send_func_key(self, key_name, punctuation=False):
        """ 设置功能键标志 """
        # 标点
        if punctuation:
            self.data = self.get_punctuation(key_name, self.Shift)
            if self.Shift:
                self.Shift = False
                self.change_shift_style()
        # 功能键
        else:
            if key_name == 'shift':
                self.Shift = True
                self.data = None
                self.change_shift_style()

            elif key_name == 'capslock':
                t = datetime.datetime.now()
                diff = (t - self.last_click_caps_time).total_seconds()
                self.last_click_caps_time = t

                # 两次点击时间间隔小于 0.6s 就认为是双击
                if diff < 0.6:
                    self.log.debug('双击 CapsLock')
                    self.double_Caps = True
                    self.Caps = False

                # 单击
                else:
                    self.log.debug('单击 CapsLock')
                    # 之前双击时, 关闭双击, 保持小写
                    if self.double_Caps:
                        self.double_Caps = not self.double_Caps    # 单击后关闭双击
                    else:
                        self.Caps = True

                self.change_caps_style()
                self.data = None

            elif key_name == 'space':
                self.data = ' '

            else:
                self.data = key_name

    def send_data(self):
        if self.data is not None:
            self.signal_send_text.emit(self.data)

    # 数字键槽函数
    for i in range(10):
        exec("""
def btn_num_{}_clicked(self):
    name = sys._getframe().f_code.co_name
    num = self.get_key_symbol(name, True)
    if self.Shift:
        num = self.num2symbol(num)
        self.Shift = False    # 一次一按
        self.change_shift_style()

    self.data = num
    self.send_data()
    msg = name + ' 按下 ' + num + ' 发送: ' + self.data
    self.log.debug(msg)
    if self.Caps:
        self.Caps = False    # 一次一按
        self.change_caps_style()
        """.format(i))

    # 字母键槽函数
    for i in range(97, 123):
        exec("""
def btn_char_{}_clicked(self):
    name = sys._getframe().f_code.co_name
    char = self.get_key_symbol(name)

    if self.Caps or self.double_Caps:
        char = char.upper()
        self.Caps = False    # 一次一按
        self.change_caps_style()

    self.data = char
    self.send_data()
    msg = name + ' 按下 ' + char + ' 发送: ' + self.data
    self.log.debug(msg)
        """.format(chr(i)))

    # 功能键槽函数
    for i in func_keys:
        exec("""
def btn_{}_clicked(self):
    name = sys._getframe().f_code.co_name
    key_name = self.get_func_key_name(name)
    self.send_func_key(key_name)
    self.send_data()
    msg1 = self.data if self.data is not None else 'None'
    msg = name + ' 按下 ' + key_name + ' 发送: ' + msg1
    self.log.debug(msg)
        """.format(i))

    # 标点键槽函数
    for i in shift_map_punctuation.keys():
        exec("""
def btn_{}_clicked(self):
    name = sys._getframe().f_code.co_name
    key_name = self.get_func_key_name(name)
    self.send_func_key(key_name, True)
    self.send_data()
    msg1 = self.data if self.data is not None else 'None'
    msg = name + ' 按下 ' + key_name + ' 发送: ' + msg1
    self.log.debug(msg)
        """.format(i))

    def btn_capslock_doubleClicked(self):
        """ 双击大写键槽函数 """
        log.debug("双击大写键")
        self.double_Caps = True

    def resizeEvent(self, event):
        """调整窗口尺寸时，该方法被持续调用。event参数包含QResizeEvent类的实例，
        通过该类的下列方法获得窗口信息"""
        w, h = event.size().width(), event.size().height()
        # ~ self.log.debug("w = {0}; h = {1}".format(w, h))
        # 以窗口尺寸, 调整字符的大小

        if h >= 360:
            self.setStyleSheet(self.set_style())

        elif 340 <= h < 360: # 小于 360 用15号字
            self.setStyleSheet(self.set_style(15))

        elif 320 <= h < 340: # 小于 360 用15号字
            self.setStyleSheet(self.set_style(12))

        elif h < 320: # 小于 360 用15号字
            self.setStyleSheet(self.set_style(10))

        QtWidgets.QWidget.resizeEvent(self, event)# 让默认函数处理其他功能


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    mainWindow = SoftKeyBoard()
    mainWindow.show()
    sys.exit(app.exec_())
