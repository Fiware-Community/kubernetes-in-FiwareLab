from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from app.main import bp

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
 return redirect(url_for('cluster.clusters'))

@bp.route('/about')
@login_required
def about():
    return render_template('main/about.html', title='About', current_user=current_user)
