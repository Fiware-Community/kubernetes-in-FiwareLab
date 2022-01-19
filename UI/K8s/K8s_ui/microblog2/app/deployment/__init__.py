from flask import Blueprint

bp = Blueprint('deployment', __name__)

from app.deployment import routes