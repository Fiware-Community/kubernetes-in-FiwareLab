from flask import Blueprint

bp = Blueprint('aws_node', __name__)

from app.aws_node import routes