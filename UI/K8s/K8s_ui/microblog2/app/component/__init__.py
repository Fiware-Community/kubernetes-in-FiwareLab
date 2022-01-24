from flask import Blueprint

bp = Blueprint('component', __name__)

from app.component import routes