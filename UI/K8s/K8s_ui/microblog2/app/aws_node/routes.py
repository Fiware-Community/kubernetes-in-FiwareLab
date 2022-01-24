from flask import render_template, flash, redirect, url_for, request
from app import db
from app.aws_node.forms import AwsNodeCreationForm
from flask_login import login_required
from app.aws_node import bp
from app.models import Aws_node
from app.models import Cluster
from flask_login import current_user
from flask_table import Table, Col
from werkzeug.utils import secure_filename
import os
from config import Config

@bp.route('/aws_node', methods=['GET', 'POST'])
@login_required
def aws_node():
    cluster_id = request.args.get('id')
    form = AwsNodeCreationForm()
    finalpath_key = ""
    if form.key_path.data:
        f =form.key_path.data
        filename = f.filename.split(".")
        docname = secure_filename(filename[0]+"_"+form.name.data+"."+filename[1])
        finalpath_key = Config.basedir+"/media/"+docname
        path1=os.path.join(Config.basedir+"/media",docname)
        f.save(path1)
        os.chmod(path1, 0o400)

    if form.validate_on_submit():
        aws_node_data = Aws_node(name=form.name.data,
                                             instance_type=form.instance_type.data,
                                             image_name=form.image_name.data,
                                             security_group_name=form.security_group_name.data,
                                             keypair_name=form.keypair_name.data,
                                             key_path=finalpath_key,
                                             vpc_subnet_id=form.vpc_subnet_id.data,
                                             cluster_id=cluster_id,
                                             ACCESS_KEY_ID=form.ACCESS_KEY_ID.data,
                                             SECRET_ACCESS_KEY=form.SECRET_ACCESS_KEY.data,
                                             REGION=form.REGION.data)
        db.session.add(aws_node_data)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('aws_node.aws_nodes',cluster_id=cluster_id))
    return render_template('aws_node/aws_node.html', title='aws_node', form=form)

@bp.route('/aws_nodes/<int:cluster_id>', methods=['GET', 'POST'])
@login_required
def aws_nodes(cluster_id):
    cluster_list = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=cluster_id).all()
    items = Aws_node.query.filter_by(cluster_id=cluster_id).all()
    class ItemTable2(Table):
        classes = ['table']
        ACCESS_KEY_ID = Col('ACCESS KEY ID')
        REGION = Col('REGION')
    table2 = ItemTable2(items)
    table2.border = True

    class ItemTable(Table):
        classes = ['table']
        id = Col('ID')
        name = Col('Name')
        instance_type = Col('Instance Type')
        image_name = Col('Image Name')
        security_group_name = Col('Security Group Name')
        keypair_name = Col('Keypair Name')
        vpc_subnet_id = Col('VPC Subnet ID')
        status = Col('Status')
        created_at = Col('CreatedAt')
        cluster_id = Col('ClusterID')
    table = ItemTable(items)
    table.border = True
    return render_template('aws_node/aws_nodes.html',
                           title='aws_nodes',
                           cluster_list=cluster_list,
                           table=table,
                           table2=table2,items=items)