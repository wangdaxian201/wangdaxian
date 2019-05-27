class Config(object):
    """项目的配置类"""

    SECRET_KEY = '123456'

    # 数据库相关配置
    # ...


class DevelopmentConfig(Config):
    """开发环境中的配置类"""
    # DEBUG = True  # 打开测试

    # 设置数据库的链接地址
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@localhost:3306/flask_test1?charset=utf8'

    # 关闭追踪数据库的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 下面是SMTP服务器配置：
    # 电子邮件服务器的主机名或IP地址
    MAIL_SERVER = 'smtp.qq.com'

    # 电子邮件服务器的端口
    MAIL_PORT = 25

    # 启动传输层的安全
    MAIL_USE_TLS = True

    # 你的邮箱用户名
    MAIL_USERNAME = '2313901135@qq.com'

    # 邮箱账户的密码，这个密码是指的授权码！
    MAIL_PASSWORD = 'fpiknnlolepldhif'


class ProductionConfig(Config):
    """生产环境(线上)中配置类"""
    DEBUG = False  # 关闭测试


APPCONFIG = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
