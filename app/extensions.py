# 导入相关库
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


# 创建相关对象
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
login_manager = LoginManager()


# 初始化
def config_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
    # login_manager.init_app(app)