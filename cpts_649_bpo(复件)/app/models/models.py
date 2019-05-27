from app import db


# 模型类 model
class User(db.Model):
    """模型类"""

    __tablename__ = 'user'

    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    # user_id
    user_id = db.Column(db.String(50), nullable=False)

    # user_name
    user_name = db.Column(db.String(50), nullable=False)

    # email
    email = db.Column(db.String(100))

    # password
    password = db.Column(db.String(50), nullable=False)

    # img
    head_img = db.Column(db.String(200), nullable=True)

    # 个人简介
    short_description = db.Column(db.String(300), nullable=True)

    # 激活状态码
    status = db.Column(db.Boolean, default=False)

    # 激活码
    activekey = db.Column(db.String(50), nullable=True)
