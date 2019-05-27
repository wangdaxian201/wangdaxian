from flask import *
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from app.config import APPCONFIG

# 创建SQLAlchemy对象
db = SQLAlchemy()

# 创建邮箱对象
mail = Mail()


def create_app():

    app = Flask(__name__)

    # 配置session用的SECRET_KEY 相当于一个加密盐
    # 1.从配置对象中加载(常用)
    app.config.from_object(APPCONFIG['development'])

    from app.views.admin import admin_blu
    from app.views.index import index_blue

    # 把蓝图(蓝本)注册到app

    app.register_blueprint(index_blue, url_prefix='/index')  # 前台个人页面的蓝图
    app.register_blueprint(admin_blu, url_prefix='/admin')  # 后台管理的页面

    # @app.errorhandler(404)
    # def internal_server_error(e):
    #     return render_template('404')

    # 添加一个app对象
    db.init_app(app)

    # 邮箱对象和当前的flask对象进行关联
    mail.init_app(app)

    # 返回当前app对象
    return app


