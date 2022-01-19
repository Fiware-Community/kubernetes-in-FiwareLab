from flask import Blueprint

bp = Blueprint('openstack_node', __name__)

from app.openstack_node import routes