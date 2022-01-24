from flask import Blueprint

bp = Blueprint('vm_node', __name__)

from app.vm_node import routes