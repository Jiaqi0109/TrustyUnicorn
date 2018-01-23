from flask import Flask
from flask_classy import FlaskView

from config import config
from .extensions import config_extensions


def create_app(config_name='production'):
    app = Flask(__name__)
    # 初始化配置
    app.config.from_object(config[config_name])
    # 配置扩展
    config_extensions(app)
    # 配置View
    configure_views(app)
    return app


# 注册Flask View
def configure_views(flask_app):
    from app.api import UserView
    for view in locals().values():
        if type(view) == type and issubclass(view, FlaskView):
            view.register(flask_app)