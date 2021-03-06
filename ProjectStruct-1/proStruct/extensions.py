# -*- coding: utf-8 -*-
# @Time : 2020/9/26
# @Author : Benny Jane
# @Email : 暂无
# @File : errors.py
# @Project : Flask-Demo
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from proStruct.utils.redis_lib import RedisManager

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
redis_manager = RedisManager()


def register_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    redis_manager.init_app(app)
