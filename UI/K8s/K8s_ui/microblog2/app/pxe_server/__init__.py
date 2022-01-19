from flask import Blueprint

bp = Blueprint('pxe_server', __name__)

from app.pxe_server import routes