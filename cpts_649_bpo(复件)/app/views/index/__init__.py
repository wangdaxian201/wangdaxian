from flask import Blueprint

# 创建一个蓝图,用来管理多个函数
index_blue = Blueprint("index", __name__)

# 添加导入 否则和views没有了关联, views里面的视图也不会生成
from . import views
