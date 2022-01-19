from flask import render_template, flash, redirect, url_for, request
from app import db
from app.openstack_node.forms import OpenstackNodeCreationForm
from flask_login import login_required
from app.openstack_node import bp
from app.models import Openstack_node
from app.models import Cluster
from flask_login import current_user
from flask_table import Table, Col
from werkzeug.utils import secure_filename
import os
from config import Config

@bp.route('/openstack_node', methods=['GET', 'POST'])
@login_required
def openstack_node():
    cluster_id = request.args.get('id')
    form = OpenstackNodeCreationForm()
    finalpath_key = ""
    if form.key_path.data:
        f =form.key_path.data
        filename = f.filename.split(".")
        docname = secure_filename(filename[0]+"_"+form.node_name.data+"."+filename[1])
        finalpath_key = Config.basedir+"/media/"+docname
        path1=os.path.join(Config.basedir+"/media",docname)
        if os.path.exists(path1) and os.path.isfile(path1):
            print "file already exist"
        else:
            f.save(path1)
            os.chmod(path1, 0o400)

    if form.validate_on_submit():
        openstack_node_data = Openstack_node(node_name=form.node_name.data,
                                             flavor_name=form.flavor_name.data,
                                             image_name=form.image_name.data,
                                             security_group_name=form.security_group_name.data,
                                             keypair_name=form.keypair_name.data,
                                             key_path=finalpath_key,
                                             private_network_name=form.private_network_name.data,
                                             external_network_name=form.external_network_name.data,
                                             cluster_id=cluster_id,
                                             auth_url=form.auth_url.data,
                                             username=form.username.data,
                                             password=form.password.data,
                                             project_name=form.project_name.data,
                                             user_domain_name=form.user_domain_name.data,
                                             project_domain_name=form.project_domain_name.data,
                                             region_name=form.region_name.data)
        db.session.add(openstack_node_data)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('openstack_node.openstack_nodes',cluster_id=cluster_id))
    return render_template('openstack_node/openstack_node.html', title='openstack_node', form=form)

@bp.route('/openstack_nodes/<int:cluster_id>', methods=['GET', 'POST'])
@login_required
def openstack_nodes(cluster_id):
    cluster_list = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=cluster_id).all()
    items = Openstack_node.query.filter_by(cluster_id=cluster_id).all()
    class ItemTable2(Table):
        classes = ['table']
        auth_url = Col('Auth URL')
        username = Col('User Name')
        password = Col('Password')
        project_name = Col('Project Name')
        user_domain_name = Col('User Domain Name')
        project_domain_name = Col('Project Domain Name')
        region_name = Col('Region Name')
    table2 = ItemTable2(items)
    table2.border = True

    class ItemTable(Table):
        classes = ['table']
        id = Col('ID')
        node_name = Col('NodeName')
        flavor_name = Col('FlavorName')
        image_name = Col('ImageName')
        security_group_name = Col('SecurityGroup')
        private_network_name = Col('PrivateNetwork')
        external_network_name = Col('ExternalNetwork')
        status = Col('Status')
        created_at = Col('CreatedAt')
        cluster_id = Col('ClusterID')
    table = ItemTable(items)
    table.border = True
    return render_template('openstack_node/openstack_nodes.html',
                           title='openstack_nodes',
                           cluster_list=cluster_list,
                           table=table,
                           table2=table2,items=items)