""" 配置日志文件 """
import logging
import os
# 1. 可以通过设置不同的日志等级，在release版本中只输出重要信息，而不必显示大量
# 的调试信息；
# 2. print将所有信息都输出到标准输出中，严重影响开发者从标准输出中查看其
# 它数据；logging则可以由开发者决定将信#息输出到什么地方，以及怎么输出；

def setup_logger(filepath):
    """ 日志文件 """
    # 当前时间 模块的文件名
    file_formatter = logging.Formatter(
        "[%(asctime)s %(filename)s %(lineno)s] %(levelname)-6s %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logger = logging.getLogger('example')
    handler = logging.StreamHandler()   # 输出到显示器
    handler.setFormatter(file_formatter)
    logger.addHandler(handler)

    file_handle_name = "file"
    if file_handle_name in [h.name for h in logger.handlers]:
        return
    if os.path.dirname(filepath) is not '':
        if not os.path.isdir(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
    # 日志文件
    file_handle = logging.FileHandler(filename=filepath, mode="a")
    file_handle.set_name(file_handle_name)
    file_handle.setFormatter(file_formatter)
    logger.addHandler(file_handle)
    logger.setLevel(logging.DEBUG) # 文件中只显示debug信息
    return logger
