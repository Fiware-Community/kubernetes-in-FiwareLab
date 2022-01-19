from flask import render_template, flash, redirect, url_for, request
from app import db
from app.pxe_server.forms import PxeServerCreationForm
from flask_login import login_required
from app.pxe_server import bp
from app.models import Pxe_server
from app.models import Cluster
from flask_login import current_user
from flask_table import Table, Col
from werkzeug.utils import secure_filename
import os
from config import Config

from flask import render_template, flash, redirect, url_for, request, current_app, copy_current_request_context
from app import db
#from app.models import Cluster, Openstack_node, Component, Deployment, Deployment_log, Vm_node, Aws_node
#from flask_table import Table, Col, LinkCol, ButtonCol

from flask import jsonify
from threading import Thread
import ansible_runner
import pprint
import ipaddress
PRIVATE_DIR = Config.rootdir+"/demo"

@bp.route('/pxe_server', methods=['GET', 'POST'])
@login_required
def pxe_server():
    #cluster_id = request.args.get('id')
    form = PxeServerCreationForm()
    if form.validate_on_submit():
        pxe_server_data = Pxe_server(dhcp_subnet_ip=form.dhcp_subnet_ip.data,
                                             dhcp_subnet_netmask=form.dhcp_subnet_netmask.data,
                                             dhcp_interface_name=form.dhcp_interface_name.data,
                                             pxe_internet_interface_name=form.pxe_internet_interface_name.data,
                                             dhcp_interface_ip=form.dhcp_interface_ip.data,
                                             #key_path=finalpath_key,
                                             dhcp_interface_netmask=form.dhcp_interface_netmask.data,
                                             dhcp_subnet_range_begin=form.dhcp_subnet_range_begin.data,
                                             dhcp_subnet_range_end=form.dhcp_subnet_range_end.data,
                                             dhcp_subnet_domain_name_servers=form.dhcp_subnet_domain_name_servers.data,
                                             #cluster_id=cluster_id,
                                             status='Pending')
        db.session.add(pxe_server_data)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('pxe_server.pxe_server_detail'))
                                #,cluster_id=cluster_id))
    return render_template('pxe_server/pxe_server.html', title='pxe_server', form=form)

@bp.route('/pxe_server_detail', methods=['GET', 'POST'])
          #<int:cluster_id>', methods=['GET', 'POST'])
@login_required
def pxe_server_detail():
                #(cluster_id):
    #cluster_list = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=cluster_id).all()
    pxe_server_detail = Pxe_server.query.first_or_404()
    return render_template('pxe_server/pxe_server_detail.html',
                           title='pxe_server_detail',
                           #cluster_list=cluster_list,
                           pxe_dl = pxe_server_detail)

@bp.route('/deploy', methods=['GET','POST'])
@login_required
def deploy_pxe_server():
    extra_varibales = dict()
    pxe_dl = Pxe_server.query.first_or_404()
    extra_varibales['dhcp_subnet_ip'] = pxe_dl.dhcp_subnet_ip.encode('ascii', 'ignore')
    extra_varibales['dhcp_subnet_netmask'] = pxe_dl.dhcp_subnet_netmask.encode('ascii', 'ignore')
    extra_varibales['dhcp_interface_name'] = pxe_dl.dhcp_interface_name.encode('ascii', 'ignore')
    extra_varibales['pxe_internet_interface_name'] = pxe_dl.pxe_internet_interface_name.encode('ascii', 'ignore')
    extra_varibales['dhcp_interface_ip'] = pxe_dl.dhcp_interface_ip.encode('ascii', 'ignore')
    extra_varibales['dhcp_interface_netmask'] = pxe_dl.dhcp_interface_netmask.encode('ascii', 'ignore')
    extra_varibales['dhcp_subnet_range_begin'] = pxe_dl.dhcp_subnet_range_begin.encode('ascii', 'ignore')
    extra_varibales['dhcp_subnet_range_end'] = pxe_dl.dhcp_subnet_range_end.encode('ascii', 'ignore')
    extra_varibales['dhcp_subnet_domain_name_servers'] = pxe_dl.dhcp_subnet_domain_name_servers.encode('ascii', 'ignore')
    playbook_path = Config.rootdir + "/pxe_ui.yml"
    @copy_current_request_context
    def threaded_task1(app):
        pxe_data = Pxe_server.query.first_or_404()
        pxe_data.status = "deploying"
        try:
            db.session.commit()
        except:
            db.session.rollback()
        r1 = ansible_runner.run(private_data_dir=PRIVATE_DIR, playbook=playbook_path, extravars=extra_varibales)
        runner_logs = r1
        with app.app_context():
            pxe_data = Pxe_server.query.first_or_404()
            if runner_logs.rc == 0 and runner_logs.status == 'successful':
                pxe_data.status = "deployed"
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
    thread = Thread(target=threaded_task1, args = (current_app._get_current_object(),))
    thread.daemon = True
    thread.start()
    print(jsonify({'thread_name': str(thread.name),
                    'started': True}))
    return redirect(url_for('pxe_server.pxe_server_detail'))