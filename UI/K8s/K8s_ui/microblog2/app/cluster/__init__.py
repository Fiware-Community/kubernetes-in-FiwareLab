from flask import Blueprint

bp = Blueprint('cluster', __name__)

from app.cluster import routes