# softkeyboard
PyQt5实现的软键盘  
Author: wkangk <wangkangchn@163.com>  

Created Time: 2020-08-18 21:28 中国标准时间  
Version: SoftKeyBoard v1.3  

1. 添加背景  
    添加背景的方法:  
        (1) 将需要添加的背景图片放到 pic 目录下, 而后使用 QtDesigner 或 QtCreater  
        将图片添加进资源, 而后修改样式加入背景即可  
        (2) 使用命令 pyrcc5 -o pic_rc.py pic.qrc 生成 pic_rc.py 文件将其 
        放入主目录即可

========================================================================  

Created Time: 2020-05-13 20:48:02 中国标准时间  
Version: SoftKeyBoard v1.2

优化:
1. 对输入框进行优化, 增加一次删除所有选择文本
2. 消除输入位置不正确bug

========================================================================  
Created Time: 2020-05-12 23:17:26 中国标准时间  
Version: SoftKeyBoard v1.1  

新增:
1. 随窗口尺寸的改变, 缩小放大按键字母, 优化体验
2. 双击CapsLock键, 锁定大写输出, 可输出大写期间CapsLock保持绿色
3. 单击shift时, 风格改为绿色

========================================================================  
Created Time: 2020-05-12 20:37:19 中国标准时间  
Version: SoftKeyBoard v1.0  

pyqt5实现英文输入软键盘, 支持:
1. Shift 切换字符
2. 每单击一次 CapsLock, 下一次输出大写字母
