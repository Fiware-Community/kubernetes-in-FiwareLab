from flask import render_template, flash, redirect, url_for, request
from app import db
from app.vm_node.forms import VmNodeCreationForm
from flask_login import login_required
from app.vm_node import bp
from app.models import Vm_node
from app.models import Cluster
from flask_login import current_user
from flask_table import Table, Col
from config import Config
import ipaddress
import os
import mysql.connector
from mysql.connector import Error
from werkzeug.utils import secure_filename
from app.cluster.routes import userID_exist,a

@bp.route('/vm_node', methods=['GET', 'POST'])
#@login_required
def vm_node():
    cluster_id = request.args.get('id')
    form = VmNodeCreationForm()
    finalpath_key = ""
    if form.vm_key_path.data:
        f =form.vm_key_path.data
        filename = f.filename.split(".")
        docname = secure_filename(filename[0] + "_vm_" + form.vm_name_prefix.data + "." + filename[1])
        finalpath_key = Config.basedir + "/media/" + docname
        path1 = os.path.join(Config.basedir + "/media", docname)
        if os.path.exists(path1) and os.path.isfile(path1):
            print "file already exist"
        else:
            f.save(path1)
            os.chmod(path1, 0o400)
    #form = VmNodeCreationForm()
    if form.validate_on_submit():
        text = ["[kubernetes-master-nodes]","kubernetes-master ansible_host="+str(form.vm_master_ip.data),"","[kubernetes-worker-nodes]","kubernetes-worker1 ansible_host="+str(form.vm_worker_ip.data)]
        with open('/root/keshavk8s/kubernetes-in-FiwareLab/UI/K8s/hosts', 'w') as f:
                for line in text:
                        f.write(line)
                        f.write('\n')
        print(type(form.vm_master_ip.data))
        print(form.vm_worker_ip.data)
        vm_node_data = Vm_node(vm_master_ip=str(form.vm_master_ip.data),
                               vm_worker_ip=str(form.vm_worker_ip.data),
                               vm_name_prefix=form.vm_name_prefix.data,
                                             vm_username=form.vm_username.data,
                                             vm_key_based_auth=form.vm_key_based_auth.data,
                                             vm_password=form.vm_password.data,
                                             vm_key_path=finalpath_key,
                                             cluster_id=cluster_id)
        db.session.add(vm_node_data)
        print("VM node:", vm_node_data)
        print("add done")
        try:
            db.session.commit()
            print("try done")
        except:
            db.session.rollback()
            print("rollback done")
        return redirect(url_for('vm_node.vm_nodes',cluster_id=cluster_id))
                                #,cluster_id=cluster_id))
        print("redirect done")
    return render_template('vm_node/vm_node.html', title='vm_node', form=form)

@bp.route('/vm_nodes/<int:cluster_id>', methods=['GET', 'POST'])
#@login_required
def vm_nodes(cluster_id):
    cluster_list = Cluster.query.filter_by(user_id=userID_exist).filter_by(id=cluster_id).all()
    items =Vm_node.query.filter_by(cluster_id=cluster_id).all()

    def ip_range(start_ip,end_ip):
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        ipaddress_list = [start.exploded.encode('ascii', 'ignore')]
        temp = start
        while temp != end:
            temp += 1
            ipaddress_list.append(temp.exploded.encode('ascii', 'ignore'))
        return ipaddress_list

    vm_data = Vm_node.query.filter_by(cluster_id=cluster_id).first_or_404()
    vm_master_ip_string = vm_data.vm_master_ip
    vm_worker_ip_string = vm_data.vm_worker_ip
    def ip_string_to_list(vm_master_ip_string,vm_worker_ip_string):
        final_vm_ip_list= []
        final_vm_ip_list.append(vm_master_ip_string)
        final_vm_ip_list.append(vm_worker_ip_string)
        return final_vm_ip_list
    vm_master_ip_list = ip_string_to_list(vm_master_ip_string,vm_worker_ip_string)


    class ItemTable2(Table):
        classes = ['table']
        vm_master_ip = Col('Auth URL')
        vm_username = Col('User Name')
        vm_key_based_auth = Col('Key Based Auth')
        vm_password = Col('Password')
        created_at = Col('Project Name')
    table2 = ItemTable2(items)
    table2.border = True
    li_obj = []
    for i in  range(0,len(vm_master_ip_list)):
         obj = {"sn":i+1,"username":vm_data.vm_username,"ip":vm_master_ip_list[i],"vm_key_based_auth":vm_data.vm_key_based_auth,
                "created_at":vm_data.created_at,"cluster_id":vm_data.cluster_id,"name":vm_data.vm_name_prefix+str(i+1)}
         li_obj.append(obj)
    return render_template('vm_node/vm_nodes.html',
                           title='vm_nodes',
                           cluster_list=cluster_list,
                          table2=table2,items=items, vm_master_ip_list=vm_master_ip_list, list_obj = li_obj)

