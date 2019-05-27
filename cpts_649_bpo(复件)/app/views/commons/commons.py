import traceback
import functools
from flask import session, g
from sqlalchemy.orm import sessionmaker

from app import db
from app.models.models import User


def login_user_data(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):

        # 尝试从session中获取user_id
        user_id = session.get('user_id')  # 获取不到,返回None

        user = None
        if user_id:
            # 用户已登录
            try:

                # 根据user_id 查询用户数据
                user = db.session.query(User).filter(User.user_id == user_id).first()
            except Exception as e:
                print("登录查询用户信息, 产生异常...")
                traceback.print_exc()

        g.user = user
        return view_func(*args, ** kwargs)

    return wrapper
