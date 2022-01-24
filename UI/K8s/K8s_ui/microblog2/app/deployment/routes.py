from flask import render_template
from flask_login import login_required
from app.deployment import bp
from app.models import Cluster, Deployment, Deployment_log
from flask_login import current_user
from flask_table import Table, Col
import json
from sqlalchemy import desc

@bp.route('/deployment_log/<int:deployment_id>', methods=['GET','POST'])
@login_required
def deployment_log(deployment_id):
    cluster_list = []
    if (deployment_id == 0):
        cluster_list = Cluster.query.filter_by(user_id=current_user.id).filter_by(user_id=current_user.id).all()
    return render_template('deployment/deployment_logs.html', title='Deployment Logs',  deployment_id=deployment_id,cluster_list=cluster_list)


@bp.route('/deployment_log_table/<int:deployment_id>', methods=['GET','POST'])
@login_required
def deployment_log_table(deployment_id):
    row_headers = ["id","deployment id","task","timestamp"]
    deployment_list = Deployment_log.query.filter_by(deployment_id=deployment_id)
    json_data=[]
    for result in deployment_list:
        json_data.append(row2dict(result))
    return json.dumps(json_data)

@bp.route('/deployment_log', methods=['GET','POST'])
@login_required
def deployment_log1(deployment_id):
    class ItemTable(Table):
        task = Col('Task Name')
        timestamp = Col('Created At')
    dep_all_tasks = Deployment_log.query.filter_by(deployment_id=deployment_id).all()
    table = ItemTable(dep_all_tasks)
    table.border = True
    return render_template('deployment/deployment_logs.html', title='Deployment Logs',  deployment_id=deployment_id)

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

@bp.route('/deployment_list_cluster_id/<int:cluster_id>', methods=['GET','POST'])
@login_required
def deployment_list_cluster_id(cluster_id):
    row_headers = ["id","name","cluster_id","timestamp"]
    deployment_list = Deployment.query.filter_by(cluster_id=cluster_id).order_by(desc(Deployment.id))
    json_data=[]
    for result in deployment_list:
        json_data.append(row2dict(result))
    return json.dumps(json_data)

@bp.route('/deployment_log_spec_id/<int:deployment_id>', methods=['GET','POST'])
@login_required
def deployment_log_spec_id(deployment_id):
    row_headers = ["id","deployment id","task","timestamp"]
    deployment_list = Deployment_log.query.filter_by(deployment_id=deployment_id).order_by(desc(Deployment_log.id))
    json_data=[]
    for result in deployment_list:
        json_data.append(row2dict(result))
    return json.dumps(json_data)
