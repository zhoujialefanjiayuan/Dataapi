from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as basesqlalchemy
from flask_migrate import Migrate
from flask_redis import FlaskRedis



class SQLAlchemy(basesqlalchemy):
    # 利用contextmanager管理器,对try/except语句封装，使用的时候必须和with结合！！！
    @contextmanager
    def auto_commit_db(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            # 加入数据库commit提交失败，必须回滚！！！
            self.session.rollback()


db = SQLAlchemy()
migrate = Migrate()
redis_store = FlaskRedis()


def init_ext(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    redis_store.init_app(app)

