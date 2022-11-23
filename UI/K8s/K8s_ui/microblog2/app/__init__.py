from flask import Flask
# , request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
#from flask_mysqldb import MySQL
from flask_login import LoginManager
from config import Config

# ...
db = SQLAlchemy()
#db = MySQL(app)
# db: SQLAlchemy = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.userLogin_auth'
#global runner_logs

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.cluster import bp as cluster_bp
    app.register_blueprint(cluster_bp, url_prefix='/cluster')

    from app.openstack_node import bp as openstack_node_bp
    app.register_blueprint(openstack_node_bp, url_prefix='/openstack_node')

    from app.aws_node import bp as aws_node_bp
    app.register_blueprint(aws_node_bp, url_prefix='/aws_node')

    from app.vm_node import bp as vm_node_bp
    app.register_blueprint(vm_node_bp, url_prefix='/vm_node')

    from app.component import bp as component_bp
    app.register_blueprint(component_bp, url_prefix='/component')

    from app.deployment import bp as deployment_bp
    app.register_blueprint(deployment_bp, url_prefix='/deployment')

    from app.pxe_server import bp as pxe_server_bp
    app.register_blueprint(pxe_server_bp, url_prefix='/pxe_server')

    return app

from app import models
