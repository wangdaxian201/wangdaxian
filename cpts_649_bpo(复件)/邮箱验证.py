from flask import Flask
from flask_mail import Mail, Message


app = Flask(__name__)
# 下面是SMTP服务器配置
app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 电子邮件服务器的主机名或IP地址
app.config['MAIL_PORT'] = 25  # 电子邮件服务器的端口
app.config['MAIL_USE_TLS'] = True  # 启用传输层安全
# 注意这里启用的是TLS协议(transport layer security)，而不是SSL协议所以用的是25号端口
app.config['MAIL_USERNAME'] = 'wangyuhao0315@qq.com'  # 你的邮件账户用户名
app.config['MAIL_PASSWORD'] = 'fpiknnlolepldhif'  # 邮件账户的密码,这个密码是指的授权码!授权码!授权码!

mail = Mail(app)


@app.route('/')
def index():
    msg = Message('你好', sender='wangyuhao0315@qq.com', recipients=['2313901135@qq.com'])
    # 这里的sender是发信人，写上你发信人的名字，比如张三。
    # recipients是收信人，用一个列表去表示。
    msg.body = '你好'
    msg.html = '<b>hello LiSihui</b>'
    mail.send(msg)
    return '<h1>邮件发送成功</h1>'


if __name__ == '__main__':
    app.run()