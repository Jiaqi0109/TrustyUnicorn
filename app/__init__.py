from flask import Flask, render_template
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
    # 配置错误处理
    # configure_errorhandler(app)
    return app


# 注册Flask View
def configure_views(flask_app):
    from app.api import PositionView, HomeView, AdminView, CityView, UserView, WESView, ResultView, CompanyView
    for view in locals().values():
        if type(view) == type and issubclass(view, FlaskView):
            view.register(flask_app)


# 错误处理
def configure_errorhandler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html')

    @app.errorhandler(500)
    def page_not_found(e):
        return render_template('errors/500.html')
