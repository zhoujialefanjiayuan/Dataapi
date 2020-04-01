# 在app/__init__.py中注册
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
import logging

from app.ext import init_ext
from app.middleware import load_middleware
from app.views import init_blue

# 设置日志的记录等级
logging.basicConfig(level=logging.DEBUG) # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler(".\log.txt", maxBytes=1024*1024*100, backupCount=10)
# 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s:%(lineno)d-%(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日志记录器
logging.getLogger(__name__).addHandler(file_log_handler)


app = Flask(__name__)
env = os.environ.get('env','dep')

def createapp():
    app.config.from_pyfile('../%sconfig.ini'%env)
    load_middleware(app=app)
    init_ext(app)
    init_blue(app)
    return app