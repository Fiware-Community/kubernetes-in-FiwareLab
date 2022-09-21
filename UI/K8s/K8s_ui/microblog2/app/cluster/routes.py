import os

from flask import render_template, flash, redirect, url_for, request, current_app, copy_current_request_context
from app import db
from app.cluster.forms import ClusterCreationForm
from flask_login import login_required
from app.cluster import bp
from app.models import Cluster, Openstack_node, Component, Deployment, Deployment_log, Vm_node, Aws_node
from flask_login import current_user
from flask_table import Table, Col, LinkCol, ButtonCol

from flask import jsonify
from threading import Thread

import ansible_runner
from config import Config
import pprint
import ipaddress

PRIVATE_DIR = Config.rootdir+"/demo"

@bp.route('/cluster', methods=['GET', 'POST'])
@login_required
def cluster():
    #print ("--------------- <=> ",Config.rootdir)
    form = ClusterCreationForm()
    if form.validate_on_submit():
        cluster = Cluster(cluster_name=form.cluster_name.data,
                          description=form.description.data,
                          cluster_type=form.cluster_type.data,
                          cluster_os=form.cluster_os.data,
                          status='Pending',
                          node_count=form.node_count.data,
                          user_id=current_user.id)
        db.session.add(cluster)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('cluster.clusters'))
    return render_template('cluster/cluster.html', title='cluster', form=form)

@bp.route('/clusters', methods=['GET'])
@login_required
def clusters():

    cluster_list = Cluster.query.filter_by(user_id=current_user.id).all()

    class ItemTable(Table):
        #id = Col('ID')
        classes = ['table' , 'table td, th' , 'table tr' , ' table th']
        id = LinkCol('Cluster ID', 'cluster.get_cluster', url_kwargs=dict(id='id'), attr='id')
        cluster_name = Col('Cluster Name')
        description = Col('Description')
        cluster_type = Col('Cluster Type')
        cluster_os = Col('OS Type')
        node_count = Col('Node Count')
        status = Col('Status')
        created_at = Col('Created At')

    items = Cluster.query.filter_by(user_id=current_user.id).all()
    table = ItemTable(items)
    return render_template('cluster/clusters.html', title='clusters', cluster_list=cluster_list, table=table)


@bp.route('/cluster/<int:id>', methods=['GET', 'POST','DELETE'])
@login_required
def get_cluster(id):

    cluster_list = Cluster.query.filter_by(id=id).first_or_404()
    cl_name= cluster_list.cluster_name.encode('ascii', 'ignore')
    cl_status = cluster_list.status.encode('ascii', 'ignore')
    print('------------cl_status--------',cl_status)
    master_ip_file_path = Config.rootdir + "/imp_files/"+ cl_name + "_master_ip.txt"
    orion_ip_file_path= Config.rootdir + "/orion.txt"
    iotagent_ip_file_path= Config.rootdir + "/iotagent.txt"
    scorpio_ip_file_path= Config.rootdir + "/scorpio.txt"
    admin_token_file_path = Config.rootdir + "/imp_files/"+ cl_name + "_admin_token.txt"
    grafana_port_file_path = Config.rootdir + "/imp_files/"+ cl_name + "_grafana-port.txt"
    alertmanager_port_file_path = Config.rootdir + "/imp_files/"+ cl_name + "_alertmanager-port.txt"
    prometheus_port_file_path = Config.rootdir + "/imp_files/"+ cl_name + "_prometheus-port.txt"
    worker_ip_file_path = Config.rootdir + "/imp_files/" + cl_name + "_worker_ip.txt"
    if os.path.exists(master_ip_file_path):
        with open(master_ip_file_path) as f:
            kube_endpoint_ip = f.readline()
            print("===kube_endpoint_ip========",kube_endpoint_ip)
    else:
        kube_endpoint_ip= '< IP Not found >'
    if os.path.exists(admin_token_file_path):
        with open(admin_token_file_path) as f1:
            admin_token = f1.readline()
            print("===admin_token========",admin_token)
    else:
        admin_token= '< token not found >'
    if os.path.exists(worker_ip_file_path):
        with open(worker_ip_file_path) as f3:
            worker_ip = f3.readline()
            print("===worker_ip========",worker_ip)
    else:
        worker_ip = '< IP Not found >'
    if os.path.exists(orion_ip_file_path):
        with open(orion_ip_file_path) as f5:
            orion_ip = f5.readline()
            print("===orion_ip========",orion_ip)
    else:
        orion_ip = '<Orion IP Not found>'
    if os.path.exists(iotagent_ip_file_path):
        with open(iotagent_ip_file_path) as f6:
            iotagent_ip = f6.readline()
            print("===iotagent_ip========",iotagent_ip)
    else:
        iotagent_ip = '<iotagent IP Not found>'
    if os.path.exists(scorpio_ip_file_path):
        with open(scorpio_ip_file_path) as f6:
            scorpio_ip = f6.readline()
            print("===scorpio_ip========",scorpio_ip)
    else:
        scorpio_ip = '<scorpio IP Not found>'
    if os.path.exists(grafana_port_file_path) and os.path.exists(alertmanager_port_file_path) and os.path.exists(prometheus_port_file_path) :
        with open(grafana_port_file_path) as f:
            grafana_port = f.readline()
            print("===grafana_port========",grafana_port)
        with open(alertmanager_port_file_path) as f1:
            alertmanager_port = f1.readline()
            print("===alertmanager_port========",alertmanager_port)
        with open(prometheus_port_file_path) as f2:
            prometheus_port = f2.readline()
            print("===prometheus_port========",prometheus_port)
    else:
        grafana_port= 'Not found'
        alertmanager_port= 'Not found'
        prometheus_port = 'Not found'

    class ItemTable(Table):
        classes = ['table' , 'table td, th' , 'table tr' , ' table th']
        id = Col('ClusterID')
        cluster_name = Col('ClusterName')
        description = Col('Description')
        cluster_type = Col('ClusterType')
        cluster_os = Col('OSType')
        node_count = Col('NodeCount')
        status = Col('Status')
        created_at = Col('CreatedAt')
        node = LinkCol('NodeDetails', 'openstack_node.openstack_node', url_kwargs=dict(id='id'))
        node1 = LinkCol('ComponentsDetails', 'component.add_component', url_kwargs=dict(id='id'))
        deploy_cluster = ButtonCol('ClusterDeploy', "cluster.execute_playbook", url_kwargs=dict(id='id'))
        delete_cluster1 = ButtonCol('Delete', "cluster.delete_cluster", url_kwargs=dict(id='id'))
    cluster_items = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).all()
    table = ItemTable(cluster_items)
    table.border = True
    #return render_template('cluster/clusters.html', cluster_list=cluster_list, )
    return render_template('cluster/cluster_specs.html', title='cluster_specs',
                           cluster_list=cluster_list, table=table, cluster_items=cluster_list,
                           cluster_status=cl_status,
                           kube_endpoint_ip=kube_endpoint_ip,admin_token=admin_token,
                           orion_port='1026',sth_comet_port='8666',cygnus_sth_service_port='5050',
                           cygnus_sth_admin_port='8081',iotagent_north_port='4041',
                           iotagent_http_port='7896',quantumleap_port='8668',
                           draco_gui_port='9091',draco_notify_port='5051',
                           grafana_port=grafana_port,alertmanager_port=alertmanager_port,iotagent_ip=iotagent_ip,
                           orion_ip=orion_ip,scorpio_ip=scorpio_ip,prometheus_port=prometheus_port,
                           master_ip=kube_endpoint_ip,worker_ip=worker_ip)

@bp.route('/cluster/<int:id>/deploy', methods=['GET','POST'])
@login_required
def execute_playbook(id):
    op_count = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404().node_count
    cluster_os = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404().cluster_os
    infra_type = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404().cluster_type
    cluster_name = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404().cluster_name

    enable_orion = Component.query.filter_by(cluster_id=id).first_or_404().enable_orion
    orion_version = Component.query.filter_by(cluster_id=id).first_or_404().orion_version
    mongodb_version = Component.query.filter_by(cluster_id=id).first_or_404().mongodb_version
    enable_sth_comet = Component.query.filter_by(cluster_id=id).first_or_404().enable_sth_comet
    sth_version = Component.query.filter_by(cluster_id=id).first_or_404().sth_version
    sth_mongo_version = Component.query.filter_by(cluster_id=id).first_or_404().sth_mongo_version
    enable_cygnus_sth = Component.query.filter_by(cluster_id=id).first_or_404().enable_cygnus_sth
    cygnus_sth_version = Component.query.filter_by(cluster_id=id).first_or_404().cygnus_sth_version
    enable_iotagent = Component.query.filter_by(cluster_id=id).first_or_404().enable_iotagent
    iot_version = Component.query.filter_by(cluster_id=id).first_or_404().iot_version
    enable_quantumleap = Component.query.filter_by(cluster_id=id).first_or_404().enable_quantumleap
    quantumleap_version = Component.query.filter_by(cluster_id=id).first_or_404().quantumleap_version
    crate_version = Component.query.filter_by(cluster_id=id).first_or_404().crate_version
    enable_draco = Component.query.filter_by(cluster_id=id).first_or_404().enable_draco
    draco_version = Component.query.filter_by(cluster_id=id).first_or_404().draco_version
    enable_ckan = Component.query.filter_by(cluster_id=id).first_or_404().enable_ckan
    extra_varibales = dict()
    extra_varibales['op_count'] = op_count
    extra_varibales['cluster_os'] = cluster_os.encode('ascii', 'ignore')
    extra_varibales['cluster_name'] = cluster_name.encode('ascii', 'ignore')
    extra_varibales['infra_type'] = infra_type.encode('ascii', 'ignore')
    extra_varibales['k8s_enable_kubernetes'] = 'yes'
    extra_varibales['k8s_flannel_cidr'] = '10.244.0.0/16'
    extra_varibales['k8s_namespace'] = 'default'

    extra_varibales['enable_orion'] = enable_orion
    extra_varibales['orion_version'] = orion_version.encode('ascii', 'ignore')
    extra_varibales['mongodb_version'] = mongodb_version.encode('ascii', 'ignore')
    extra_varibales['enable_sth_comet'] = enable_sth_comet
    extra_varibales['sth_version'] = sth_version.encode('ascii', 'ignore')
    extra_varibales['sth_mongo_version'] = sth_mongo_version.encode('ascii', 'ignore')
    extra_varibales['enable_cygnus_sth'] = enable_cygnus_sth
    extra_varibales['cygnus_sth_version'] = cygnus_sth_version.encode('ascii', 'ignore')
    extra_varibales['enable_iotagent'] = enable_iotagent
    extra_varibales['iot_version'] = iot_version.encode('ascii', 'ignore')
    extra_varibales['enable_quantumleap'] = enable_quantumleap
    extra_varibales['quantumleap_version'] = quantumleap_version.encode('ascii', 'ignore')
    extra_varibales['crate_version'] = crate_version.encode('ascii', 'ignore')
    extra_varibales['enable_draco'] = enable_draco
    extra_varibales['draco_version'] = draco_version.encode('ascii', 'ignore')
    extra_varibales['enable_ckan'] = enable_ckan

    if extra_varibales['infra_type'] == 'openstack':
        op_OS_AUTH_URL = Openstack_node.query.filter_by(cluster_id=id).first_or_404().auth_url
        op_OS_USERNAME = Openstack_node.query.filter_by(cluster_id=id).first_or_404().username
        op_OS_PASSWORD = Openstack_node.query.filter_by(cluster_id=id).first_or_404().password
        op_OS_PROJECT_NAME = Openstack_node.query.filter_by(cluster_id=id).first_or_404().project_name
        op_OS_USER_DOMAIN_NAME = Openstack_node.query.filter_by(cluster_id=id).first_or_404().user_domain_name
        op_OS_PROJECT_DOMAIN_NAME = Openstack_node.query.filter_by(cluster_id=id).first_or_404().project_domain_name
        op_OS_REGION_NAME = Openstack_node.query.filter_by(cluster_id=id).first_or_404().region_name

        op_vm_name_prefix = Openstack_node.query.filter_by(cluster_id=id).first_or_404().node_name
        op_flavor = Openstack_node.query.filter_by(cluster_id=id).first_or_404().flavor_name
        op_image = Openstack_node.query.filter_by(cluster_id=id).first_or_404().image_name
        op_security_groups = Openstack_node.query.filter_by(cluster_id=id).first_or_404().security_group_name
        op_key_name = Openstack_node.query.filter_by(cluster_id=id).first_or_404().keypair_name
        op_key_path = Openstack_node.query.filter_by(cluster_id=id).first_or_404().key_path
        op_private_network = Openstack_node.query.filter_by(cluster_id=id).first_or_404().private_network_name
        op_external_network = Openstack_node.query.filter_by(cluster_id=id).first_or_404().external_network_name

        extra_varibales['op_OS_AUTH_URL'] = op_OS_AUTH_URL.encode('ascii', 'ignore')
        extra_varibales['op_OS_USERNAME'] = op_OS_USERNAME.encode('ascii', 'ignore')
        extra_varibales['op_OS_PASSWORD'] = op_OS_PASSWORD.encode('ascii', 'ignore')
        extra_varibales['op_OS_PROJECT_NAME'] = op_OS_PROJECT_NAME.encode('ascii', 'ignore')
        extra_varibales['op_OS_USER_DOMAIN_NAME'] = op_OS_USER_DOMAIN_NAME.encode('ascii', 'ignore')
        extra_varibales['op_OS_PROJECT_DOMAIN_NAME'] = op_OS_PROJECT_DOMAIN_NAME.encode('ascii', 'ignore')
        #extra_varibales['op_OS_REGION_NAME'] = op_OS_REGION_NAME

        extra_varibales['op_vm_name_prefix'] = op_vm_name_prefix.encode('ascii', 'ignore')
        extra_varibales['op_flavor'] = op_flavor.encode('ascii', 'ignore')
        extra_varibales['op_image'] = op_image.encode('ascii', 'ignore')
        extra_varibales['op_security_groups'] = op_security_groups.encode('ascii', 'ignore')
        extra_varibales['op_key_name'] = op_key_name.encode('ascii', 'ignore')
        extra_varibales['op_key_path'] = op_key_path.encode('ascii', 'ignore')
        extra_varibales['op_private_network'] = op_private_network.encode('ascii', 'ignore')
        extra_varibales['op_external_network'] = op_external_network.encode('ascii', 'ignore')
    else:
        extra_varibales['op_OS_AUTH_URL'] = ''
        extra_varibales['op_OS_USERNAME'] = ''
        extra_varibales['op_OS_PASSWORD'] = ''
        extra_varibales['op_OS_PROJECT_NAME'] = ''
        extra_varibales['op_OS_USER_DOMAIN_NAME'] = ''
        extra_varibales['op_OS_PROJECT_DOMAIN_NAME'] = ''
    if extra_varibales['infra_type'] == 'AWS':
        ACCESS_KEY_ID = Aws_node.query.filter_by(cluster_id=id).first_or_404().ACCESS_KEY_ID
        SECRET_ACCESS_KEY = Aws_node.query.filter_by(cluster_id=id).first_or_404().SECRET_ACCESS_KEY
        REGION = Aws_node.query.filter_by(cluster_id=id).first_or_404().REGION
        aws_node_name = Aws_node.query.filter_by(cluster_id=id).first_or_404().name
        aws_instance_type = Aws_node.query.filter_by(cluster_id=id).first_or_404().instance_type
        aws_image_name = Aws_node.query.filter_by(cluster_id=id).first_or_404().image_name
        aws_security_group_name = Aws_node.query.filter_by(cluster_id=id).first_or_404().security_group_name
        aws_vpc_subnet_id = Aws_node.query.filter_by(cluster_id=id).first_or_404().vpc_subnet_id
        aws_key_path = Aws_node.query.filter_by(cluster_id=id).first_or_404().key_path
        aws_key_name = Aws_node.query.filter_by(cluster_id=id).first_or_404().keypair_name
        aws_node_count = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404().node_count
        extra_varibales['ACCESS_KEY_ID'] = ACCESS_KEY_ID.encode('ascii', 'ignore')
        extra_varibales['SECRET_ACCESS_KEY'] = SECRET_ACCESS_KEY.encode('ascii', 'ignore')
        extra_varibales['REGION'] = REGION.encode('ascii', 'ignore')
        extra_varibales['aws_name'] = aws_node_name.encode('ascii', 'ignore')
        extra_varibales['aws_count'] = aws_node_count
        extra_varibales['aws_instance_type'] = aws_instance_type.encode('ascii', 'ignore')
        extra_varibales['aws_image'] = aws_image_name.encode('ascii', 'ignore')
        extra_varibales['aws_security_group'] = aws_security_group_name.encode('ascii', 'ignore')
        extra_varibales['aws_vpc_subnet_id'] = aws_vpc_subnet_id.encode('ascii', 'ignore')
        extra_varibales['aws_key_path'] = aws_key_path.encode('ascii', 'ignore')
        extra_varibales['aws_key_name'] = aws_key_name.encode('ascii', 'ignore')
    else:
        extra_varibales['ACCESS_KEY_ID'] = ""
        extra_varibales['SECRET_ACCESS_KEY'] = ""
        extra_varibales['REGION'] = ""
    def ip_range(start_ip,end_ip):
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        ipaddress_list = [start.exploded.encode('ascii', 'ignore')]
        temp = start
        while temp != end:
            temp += 1
            ipaddress_list.append(temp.exploded.encode('ascii', 'ignore'))
        return ipaddress_list
    if extra_varibales['infra_type'] == 'VM':
        vm_data = Vm_node.query.filter_by(cluster_id=id).first_or_404()
        #extra_varibales['bm_node_prefix'] = vm_data.vm_name_prefix.encode('ascii', 'ignore')
        #extra_varibales['bm_node_username'] = vm_data.vm_username.encode('ascii', 'ignore')
        #extra_varibales['bm_node_password'] = vm_data.vm_password.encode('ascii', 'ignore')
        #extra_varibales['bm_key_path'] = vm_data.vm_key_path.encode('ascii', 'ignore')
        #extra_varibales['bm_key_based_auth'] = vm_data.vm_key_based_auth
        vm_ip_string = vm_data.vm_ip
        def ip_string_to_list(vm_ip_string):
            final_vm_ip_list= []
            range_list = vm_ip_string.split('\r\n')
            for range in range_list:
                final_vm_ip_list.append(range.encode('ascii', 'ignore'))
            return final_vm_ip_list

        #listToStr = ','.join(map(str, ip_string_to_list(vm_ip_string)))
        extra_varibales['bm_nodeIPs'] = ip_string_to_list(vm_ip_string)
        #extra_varibales['bm_nodeIPs'] = listToStr
        #extra_varibales['bm_node_count'] = len(extra_varibales['bm_nodeIPs'])
    else:
        extra_varibales['bm_nodeIPs'] = ['192.168.122.1','192.168.122.2']
    pprint.pprint(extra_varibales)
    #playbook_path = "/home/necuser/sandbox/site_ui.yaml"
    playbook_path = Config.rootdir+"/site_ui.yaml"
    cfg_path=Config.rootdir+"/ansible.cfg"
    env = {}
    env["ANSIBLE_CONFIG"] = cfg_path
    r1 = ansible_runner.run_async(private_data_dir=PRIVATE_DIR, playbook=playbook_path, envvars=env, extravars=extra_varibales)
    deployment_data = Deployment(name='deployment_name',cluster_id=id)
    db.session.add(deployment_data)
    try:
        db.session.commit()
    except:
        db.session.rollback()
    cluster_data = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404()
    cluster_data.status = "started"
    try:
        db.session.commit()
    except:
        db.session.rollback()
    runner_logs = r1
    deployment_id = Deployment.query.filter_by(cluster_id=id).all()[-1]
    #print('========with_deployment_id====', deployment_id)
    #print("=======g.runner_logs=========_cluster=======", runner_logs)
    @copy_current_request_context
    def threaded_task(app):
        task_list = []
        #print("inside in thread------===========")
        with app.app_context():
            deployment_id = Deployment.query.filter_by(cluster_id=id).all()[-1]
            #print('========with_deployment_id====',deployment_id)
            #time.sleep(5)
            #for each_data in runner_logs.events:
            gen = runner_logs.events
            while True:
                try:
                    each_data = next(gen)
                    if 'event' in each_data:
                        if 'stdout' in each_data:
                            each_data_stdout = each_data['stdout'].encode('ascii', 'ignore')
                            #print('=====each_data===dir====', dir(each_data),'======each_data===type==', type(each_data))
                            if (not each_data_stdout):
                                print('======skip when stdout is null========')
                            else:
                                if 'skip' not in each_data['event']:
                                    if 'playbook' not in each_data['event']:
				        ansible_runner.run_async(private_data_dir=PRIVATE_DIR, playbook=playbook_path, envvars=env, extravars=extra_varibales)                                   
                                        if 'event_data' in each_data:
                                            yy1 = each_data['event_data']
                                            if 'runner_on_failed' in each_data['event'] and 'ignore_errors' in yy1 and yy1['ignore_errors']==None:
                                                if 'stdout' in each_data:
                                                    yy2= each_data['stdout'].encode('ascii', 'ignore')
                                                    print('=======res==yy2======', yy2, "===type==",type(yy2))
                                                    deployment_task_data = Deployment_log(task=yy2, log_type='ERROR',
                                                                                          deployment_id=deployment_id.id)
                                                    db.session.add(deployment_task_data)
                                                    try:
                                                        db.session.commit()
                                                    except:
                                                        db.session.rollback()
                                            else:
                                                if 'event_data' in each_data:
                                                    yy1 = each_data['event_data']
                                                    if 'task' in yy1:
                                                        yy2= yy1['task']
                                                        print('=========yy2======',yy2)
                                                        yy3 = yy2.encode('ascii', 'ignore')
                                                        dep_all_tasks = Deployment_log.query.filter_by(deployment_id=deployment_id.id).all()
                                                        empty_list = []
                                                        for each_task in dep_all_tasks:
                                                            if yy3 == each_task.task.encode('ascii', 'ignore'):
                                                                empty_list.append('found')
                                                        if 'found' not in empty_list:
                                                            deployment_task_data = Deployment_log(task=yy3, log_type='INFO', deployment_id= deployment_id.id)
                                                            db.session.add(deployment_task_data)
                                                            try:
                                                                db.session.commit()
                                                            except:
                                                                db.session.rollback()
                                                            cluster_data = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404()
                                                            cluster_data.status = runner_logs.status
                                                            try:
                                                                db.session.commit()
                                                            except:
                                                                db.session.rollback()
                except StopIteration:
                    cluster_data = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404()
                    cluster_data.status = runner_logs.status
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                    print('========break=====')
                    print task_list
                    break
    thread = Thread(target=threaded_task, args = (current_app._get_current_object(),))
    thread.daemon = True
    thread.start()
    print(jsonify({'thread_name': str(thread.name),
                    'started': True}))
    return redirect(url_for('deployment.deployment_log',deployment_id=deployment_id.id))
    #return render_template('cluster/deploy_cluster.html', title='deploy_cluster', table=table)

@bp.route('/cluster/<int:id>/delete', methods=['GET','POST'])
@login_required
def delete_cluster(id):
    extra_varibales = dict()
    cluster_os = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404().cluster_os
    extra_varibales['cluster_os'] = cluster_os.encode('ascii', 'ignore')
    infra_type = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404().cluster_type
    extra_varibales['infra_type'] = infra_type.encode('ascii', 'ignore')
    if extra_varibales['infra_type'] == 'openstack':
        op_OS_AUTH_URL = Openstack_node.query.filter_by(cluster_id=id).first_or_404().auth_url
        op_OS_USERNAME = Openstack_node.query.filter_by(cluster_id=id).first_or_404().username
        op_OS_PASSWORD = Openstack_node.query.filter_by(cluster_id=id).first_or_404().password
        op_OS_PROJECT_NAME = Openstack_node.query.filter_by(cluster_id=id).first_or_404().project_name
        op_OS_USER_DOMAIN_NAME = Openstack_node.query.filter_by(cluster_id=id).first_or_404().user_domain_name
        op_OS_PROJECT_DOMAIN_NAME = Openstack_node.query.filter_by(cluster_id=id).first_or_404().project_domain_name
        op_OS_REGION_NAME = Openstack_node.query.filter_by(cluster_id=id).first_or_404().region_name
        op_vm_name_prefix = Openstack_node.query.filter_by(cluster_id=id).first_or_404().node_name
        op_count = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404().node_count
        extra_varibales['op_count'] = op_count
        extra_varibales['op_OS_AUTH_URL'] = op_OS_AUTH_URL.encode('ascii', 'ignore')
        extra_varibales['op_OS_USERNAME'] = op_OS_USERNAME.encode('ascii', 'ignore')
        extra_varibales['op_OS_PASSWORD'] = op_OS_PASSWORD.encode('ascii', 'ignore')
        extra_varibales['op_OS_PROJECT_NAME'] = op_OS_PROJECT_NAME.encode('ascii', 'ignore')
        extra_varibales['op_OS_USER_DOMAIN_NAME'] = op_OS_USER_DOMAIN_NAME.encode('ascii', 'ignore')
        extra_varibales['op_OS_PROJECT_DOMAIN_NAME'] = op_OS_PROJECT_DOMAIN_NAME.encode('ascii', 'ignore')
        # extra_varibales['op_OS_REGION_NAME'] = op_OS_REGION_NAME
        extra_varibales['op_vm_name_prefix'] = op_vm_name_prefix.encode('ascii', 'ignore')
        playbook_path = Config.rootdir + "/destroy_vm_with_vm_name.yaml"

    def ip_range(start_ip, end_ip):
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        ipaddress_list = [start.exploded.encode('ascii', 'ignore')]
        temp = start
        while temp != end:
            temp += 1
            ipaddress_list.append(temp.exploded.encode('ascii', 'ignore'))
        return ipaddress_list

    if extra_varibales['infra_type'] == 'baremetal':
        vm_data = Vm_node.query.filter_by(cluster_id=id).first_or_404()
        extra_varibales['bm_node_prefix'] = vm_data.vm_name_prefix.encode('ascii', 'ignore')
        extra_varibales['bm_node_username'] = vm_data.vm_username.encode('ascii', 'ignore')
        extra_varibales['bm_node_password'] = vm_data.vm_password.encode('ascii', 'ignore')
        extra_varibales['bm_key_path'] = vm_data.vm_key_path.encode('ascii', 'ignore')
        extra_varibales['bm_key_based_auth'] = vm_data.vm_key_based_auth
        vm_ip_string = vm_data.vm_ip
        def ip_string_to_list(vm_ip_string):
            final_vm_ip_list = []
            range_list = vm_ip_string.split('\r\n')
            for range in range_list:
                final_vm_ip_list.append(range.encode('ascii', 'ignore'))
            return final_vm_ip_list

        extra_varibales['bm_nodeIPs'] = ip_string_to_list(vm_ip_string)
        extra_varibales['k8s_enable_kubernetes'] = 'yes'
        playbook_path = Config.rootdir + "/destroy_baremetal_vm_with_vm_ips.yaml"
    if extra_varibales['infra_type'] == 'AWS':
        ACCESS_KEY_ID = Aws_node.query.filter_by(cluster_id=id).first_or_404().ACCESS_KEY_ID
        SECRET_ACCESS_KEY = Aws_node.query.filter_by(cluster_id=id).first_or_404().SECRET_ACCESS_KEY
        REGION = Aws_node.query.filter_by(cluster_id=id).first_or_404().REGION
        aws_node_name = Aws_node.query.filter_by(cluster_id=id).first_or_404().name
        extra_varibales['ACCESS_KEY_ID'] = ACCESS_KEY_ID.encode('ascii', 'ignore')
        extra_varibales['SECRET_ACCESS_KEY'] = SECRET_ACCESS_KEY.encode('ascii', 'ignore')
        extra_varibales['REGION'] = REGION.encode('ascii', 'ignore')
        extra_varibales['aws_name'] = aws_node_name.encode('ascii', 'ignore')
        extra_varibales['k8s_enable_kubernetes'] = 'yes'
        playbook_path = Config.rootdir + "/destroy_aws_vm_with_vm_name.yaml"
    @copy_current_request_context
    def threaded_task1(app):
        cluster_data = Cluster.query.filter_by(id=id).first_or_404()
        cluster_data.status = "deleting"
        try:
            db.session.commit()
        except:
            db.session.rollback()
	cfg_path=Config.rootdir+"/ansible.cfg"
        env = {}
        env["ANSIBLE_CONFIG"] = cfg_path
        playbook_path = Config.rootdir + "/destroy_baremetal_vm_with_vm_ips.yaml"
        r1 = ansible_runner.run(private_data_dir=PRIVATE_DIR, playbook=playbook_path,envvars=env, extravars=extra_varibales)        
        runner_logs = r1
        with app.app_context():
            cluster_data = Cluster.query.filter_by(user_id=current_user.id).filter_by(id=id).first_or_404()
            if runner_logs.rc == 0 and runner_logs.status == 'successful':
                cluster_data.status = "deleted"
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
    thread = Thread(target=threaded_task1, args = (current_app._get_current_object(),))
    thread.daemon = True
    thread.start()
    print(jsonify({'thread_name': str(thread.name),
                    'started': True}))
    return redirect(url_for('cluster.clusters'))
