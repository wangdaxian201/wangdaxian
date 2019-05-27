import hashlib
import os
import traceback
import uuid
import flask
from flask import *
from sqlalchemy import *
from sqlalchemy.orm import *
from flask_mail import Message
from app import db, mail
from app.models.models import User
from app.views.commons.commons import login_user_data
from . import index_blue


@index_blue.route("/profile_v7/")
@login_user_data
def profile7():
    """登录验证"""

    # 从g里面 获取到用户信息 在login_user_data装饰器里面已经查询好了
    user = g.user

    if user:
        # 模板渲染
        return render_template("index/profile.html",
                               user_name=user.user_name,
                               head_img=user.head_img,
                               short_desc=user.short_description)
    else:
        return '去<a href="http://127.0.0.1:5000/index/login.html">登录</a>'


@index_blue.route('/login.html')
def login():
    """显示登录页面"""
    return render_template('index/login.html')  # 获取返回的数据


@index_blue.route('/login', methods=['POST', 'GET'])
def login_vf():
    """处理登录验证"""

    print('get----', request.args)
    print('post----', request.form)
    if request.method == 'POST':

        # 获取用户名和密码
        username = request.form.get('username')
        password = request.form.get('password')

        # 业务逻辑 登录用户

        try:

            # 查询数据
            user = db.session.query(User).filter(and_(User.user_name == username, User.password == password)).one()

        except:
            # 查询失败则登录失败
            ret = {
                "status": 1,
                "msg": "用户名或密码错误，请重新输入"
            }
            response = make_response(flask.jsonify(ret))

            # 设置cookie
            # response.set_cookie('login_flag', 'fail')
            # 设置session
            session['login_flag'] = 'fail'

        else:

            # 登录成功 redirect返回的是一个response对象，可以设置cookie
            ret = {
                "status": 0,
                "msg": "登录成功"
            }
            response = make_response(flask.jsonify(ret))

            # response.set_cookie('login_flag', 'success')
            # response.set_cookie('user_id', username)
            # 设置session
            session['login_flag'] = 'success'
            session['user_id'] = username

        finally:

            # 关闭会话对象
            db.session.close()

        # 验证通过重定向去用户页面
        return response


@index_blue.route('/logout')
def logout():
    """退出登录"""

    # 获取response响应对象
    response = redirect(url_for('index.login'))

    # 把cookie登录相关的信息清除
    response.delete_cookie('login_flag')

    return response


@index_blue.route("/register", methods=["GET", "POST"])
def register():
    """显示注册页面"""

    if request.method == 'POST':

        # 获取post请求的参数
        email = request.form.get('email')  # 获取邮箱

        password = request.form.get('password')  # 获取密码

        username = request.form.get('username')  # 获取用户名

        captcha = request.form.get('captcha')  # 获取图片验证码

        # 只要缺少一个需要的数据，就返回错误
        if not (email and username and password and captcha):
            # 返回post请求的参数
            ret = {
                "status": 2,
                "msg": "输入数据错误，请重新输入"
            }
            return flask.jsonify(ret)
        # 从session中去除图片验证码
        session_captcha = session.get('captcha')

        # 判断验证码是否正确
        if session_captcha.lower() != captcha.lower():
            # 返回post请求的参数
            ret = {
                "status": 3,
                "msg": "验证码输入错误"
            }
            return flask.jsonify(ret)

        # 业务处理,判断是否注册

        # 1.业务处理

        # 数据查询
        user_ret = db.session.query(User).filter(or_(User.user_name == username, User.email == email)).first()

        if user_ret:

            ret = {
                "status": 1,
                "msg": "邮箱或用户名已存在,请修改"
            }
            return flask.jsonify(ret)
        else:
            activekey = str(uuid.uuid1())  # 获取激活码

            activekey = activekey.replace('-', '')

            # request.host_url http://127.0.0.1:5000/
            active__addr = request.host_url + 'index/active?user_id={}&activekey={}'.format(username, activekey)

            # 发送激活码的功能
            # sender到时候换成公司要求的邮箱 recipients是接受人的邮箱
            msg = Message('你好', sender='2313901135@qq.com', recipients=[email])
            msg.body = '激活邮件'
            msg.html = '<a href="{}">点击验证</a>,完成账户激活，如果有问题请联王大仙,电话17661480714'.format(active__addr)

            # 发送
            mail.send(msg)

            # -------------------------------------------------------------------------------------
            # 未注册进行注册
            new_user = User(email=email, user_id=username, user_name=username, password=password, activekey=activekey)
            # 添加提交
            db.session.add(new_user)
            db.session.commit()

            # 返回对应的信息
            ret = {
                "status": 0,
                "msg": "注册成功"
            }

            return flask.jsonify(ret)

    elif request.method == 'GET':
        print(1112222222222)
        # 如果是GET请求 就是请求页面
        return render_template("index/register.html")


@index_blue.route('/active', methods=["POST", "GET"])
def active():
    """用来验证账户和激活码"""

    # 获取用户id
    user_id = request.args.get('user_id')
    # 获取激活码
    activekey = request.args.get('activekey')

    try:
        # 数据库查询和这个激活码相同的用户
        user = db.session.query(User).filter(and_(User.user_id == user_id, activekey == activekey)).one()

    except Exception as e:
        # 修改状态码
        print(e)
        traceback.print_exc()
        request_str = '激活失败， 请重新注册'
    else:
        # 修改状态码
        user.status = 1
        # 提交
        db.session.commit()

        request_str = '激活成功,点击<a href="{}">登录</a>'.format(url_for('.login'))

    return request_str


@index_blue.route("/forgot")
def forgot():
    """显示忘记密码"""
    return render_template('/index/forgot.html')


from app.utils.captcha.captcha import captcha


@index_blue.route("/captcha")
def generate_captcha():
    """图片验证码所对应的函数"""
    # # 1. 获取当前的图片编号id
    # captcha_id = request.args.get('id')
    # print(type(captcha_id), captcha_id)

    # 2.生成图片验证码
    # 返回保存的图片名字  验证码的值 图片二进制内容
    name, text, image = captcha.generate_captcha()

    # 3.将生成的图片验证值作为value, 存储到session中
    session['captcha'] = text

    # 返回响应内容
    resp = make_response(image)

    # 设置内容类型
    resp.headers['Content-Type'] = 'image/jpg'
    return resp


@index_blue.route('/edit', methods=["GET", "POST"])
@login_user_data
def edit():
    current_user = g.user
    # 判断账户是否存在
    if not current_user:
        # 没有存在就去登录
        return reditect(url_for(".login"))

    # 如果是GET请求就返回页面
    if request.method == "GET":
        return render_template("index/edit.html", user=g.user)

    elif request.method == "POST":
        # 获取用户名
        username = request.form.get("username")

        # 获取密码
        password = request.form.get("password")

        # 获取邮箱
        email = request.form.get('email')

        # 获取内容
        content = request.form.get("content")

        # 当前应用路径
        print(current_app.root_path)

        # 获取头像,注意：和获取文本信息方式不同
        f = request.files.get("image")

        # 判断文件是否存在
        if f:
            # 获取文件的后缀名
            image_type = f.filename[(f.filename.rfind(".")):]

            # 根据图片的二进制数据获取MD5加密的一个字符串最后保存的名字
            name_hash = hashlib.md5()
            uuidstr = str(uuid.uuid1())  # uuid 保证图片名字不一样 不会覆盖
            name_hash.update((f.filename + uuidstr).encode("utf-8"))
            image_file_name = name_hash.hexdigest()

            # 图片保存的名字 = MD5加密一个字符串 + 原后缀
            image_file = image_file_name + image_type

            # 图片在服务器里的路径 注意提前创建好/static/upload/images文件夹
            image_path = os.path.join('/static/upload/images', image_file)

            # 图片的绝对路径
            upload_path = os.path.join(current_app.root_path, 'static/upload/images', image_file)
            print(upload_path)
            # 保存图片到硬盘
            f.save(upload_path)
            # 保存图片路径到数据库
            current_user.head_img = image_path

        # 修改用户信息 为新的信息
        current_user.user_name = username
        current_user.password = password
        current_user.email = email
        current_user.short_desc = content

        # 提交数据
        db.session.commit()
        db.session.close()

        # 重新刷新编辑页面 显示新的信息
        return redirect(url_for(".edit"))
