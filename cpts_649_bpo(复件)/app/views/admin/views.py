import flask
from flask import *
from sqlalchemy import *
from sqlalchemy.orm import *

from app import db
from app.models.models import User

# .就代表当前模块 会去模块的init.py找admin_blu
from commons.commons import login_user_data
from . import admin_blu


@admin_blu.route('/')
def index1():
    return render_template('admin/login.html')


@admin_blu.route('/index.html')
def index2():
    return render_template('admin/index.html')


# 上一版本，不必改动
# @admin_blu.route('/tables.html')
# def user_info():
#     """显示页面信息"""
#     # 获取session标记
#     login_flag = flask.session.get('login_flag', 'fail')
#
#     if login_flag == 'success':
#         # 获取db_session对象
#         # db_session = sessionmaker(bind=engine)()
#
#         # 查询全部数据
#         all_user_info = db.session.query(User).all()
#         print(all_user_info)
#
#         # 关闭session
#         db.session.close()
#
#         # 模板渲染
#         return render_template('admin/tables.html', user_infos=all_user_info)


@admin_blu.route('/tables.html')
def table():
    """显示页面信息"""
    # # 获取session标记
    # login_flag = flask.session.get('login_flag', 'fail')
    print(1111111111111)
    # if login_flag == 'success':
    per_page = 5  # 要分页的每页数量
    # 当前第几页是浏览器发过来的请求参数 默认第一页 注意
    page_index = int(request.args.get('page', 1))

    # 查询分页的数据
    pagination = User.query.paginate(page=page_index, per_page=per_page, error_out=False)

    # 查询分页的全部数据
    all_user_info = pagination.items

    # print(all_user_info)
    # 关闭session
    db.session.close()

    # 模板渲染
    return render_template('admin/tables.html', user_infos=all_user_info, pagination=pagination)


@admin_blu.route('/login.html')
def login():
    """显示登录页面"""
    print('login111111111111')

    return render_template('admin/login.html')


@admin_blu.route('/login', methods=['GET', 'POST'])
@login_user_data
def login_vf():
    """登录验证"""
    print(11111111)
    if request.method == 'POST':
        # 获取post请求的参数
        # print('post', request.form)

        # 获取邮箱和密码
        email = request.form.get('email')
        password = request.form.get('password')

        # 业务逻辑 用户登录

        # # 得到会话对象
        # db_session = sessionmaker(bind=engine)()

        try:
            user = db.session.query(User).filter(and_(User.email == email, User.password == password)).one()

        except:
            # 设置状态数据
            ret = {
                'status': 1,
                'msg': '邮箱或密码错误'
            }
            response = make_response(flask.jsonify(ret))

            # 设置session
            session['login_flag'] = 'fail'
        else:
            # 设置状态数据
            ret = {
                'status': 0,
                'msg': '登录成功'
            }
            response = make_response(flask.jsonify(ret))

            # 设置session
            session['login_flag'] = 'success'

        finally:
            # 关闭会话对象
            db.session.close()

        # 返回ajax数据 和session
        return response
