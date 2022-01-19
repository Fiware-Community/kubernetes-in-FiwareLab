from app.api import bp
from flask import jsonify
from app.models import User
from flask import request

@bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    #print(User.query.get_or_404(id))
    return jsonify(User.query.get_or_404(id).to_dict())
    #return User.query

@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)