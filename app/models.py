# !/usr/bin/env python
# -*- coding:utf-8 -*-
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:010771@localhost:3306/movie?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


# 用户
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    pwd = db.Column(db.String(16))
    email = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(11), unique=True)
    info = db.Column(db.Text)
    face = db.Column(db.String(255))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())
    uuid = db.Column(db.String(255), unique=True)
    userlogs = db.relationship("Userlog", backref="user")  # 外键关系关联
    comment = db.relationship("Comment", backref="user")  # 外键关系关联
    moviecols = db.relationship("Moviecol", backref="user")  # 外键关系关联

    def __repr__(self):
        return "<User %r>" % self.name


# 登录日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, default=datetime.now())
    movies = db.relationship("Movie", backref="tag")  # 外键关系关联

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    playnum = db.Column(db.BigInteger)
    info = db.Column(db.Text)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    area = db.Column(db.String(20))
    release_time = db.Column(db.DateTime, default=datetime.now())
    length = db.Column(db.String(100))
    add_time = db.Column(db.DateTime, default=datetime.now())
    comments = db.relationship("Comment", backref="movie")  # 外键关系关联
    moviecols = db.relationship("Moviecol", backref="movie")  # 外键关系关联

    def __repr__(self):
        return "<movie %r>" % self.title


# 电影上映
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<preview %r>" % self.title


# 电影评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    add_time = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<comment %r>" % self.id


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    add_time = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<moviecol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<Auth %r>" % self.id


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    auths = db.Column(db.String(500))
    add_time = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "< %r>" % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    pwd = db.Column(db.String(16))
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    add_time = db.Column(db.DateTime, default=datetime.now())
    adminlogs = db.relationship("Adminlog", backref="admin")  # 外键关系关联
    oplogs = db.relationship("Oplog", backref="admin")  # 外键关系关联

    def __repr__(self):
        return "<Admin %r>" % self.name


# 登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 管理日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(500))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())

    def __repr__(self):
        return "<Oplog %r>" % self.id

if __name__ == "__main__":
    db.create_all()