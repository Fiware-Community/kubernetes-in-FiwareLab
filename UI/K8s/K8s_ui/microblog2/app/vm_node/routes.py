from flask import render_template, flash, redirect, url_for, request
from app import db
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, FileField, TextAreaField, validators, BooleanField, SelectField, FieldList
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, Regexp
from app.models import Vm_node, User

from flask_login import login_required
from app.vm_node import bp
from app.models import Cluster
from flask_login import current_user
from flask_table import Table, Col
from config import Config
import ipaddress
import os
import mysql.connector
from mysql.connector import Error
from werkzeug.utils import secure_filename
from flask import session

@bp.route('/vm_node', methods=['GET', 'POST'])
#@login_required
def vm_node():
    vm_nodecount1 = int(session['vm_nodecount'][0])
    project_id=session['projectid']
    connection1 = mysql.connector.connect(host='localhost',
                                      database='db',
                                      user='root',
                                      password='Abc@1234')
    cursor1 = connection1.cursor()
    sql_select_query1 = """select Projectip from user where username = (%s) """
    cursor1.execute(sql_select_query1,(project_id,))
    get_ip = cursor1.fetchone()
    if get_ip is None:
        get_ip1 = User(Projectip=get_ip)
        db.session.add(get_ip1)
        db.session.commit()
    else:
        Pip1 = str(get_ip[0])
        session['Pip'] = Pip1
        Pip = session['Pip']
    cluster_id = request.args.get('id')
    class VmNodeCreationForm(Form):
        vm_name_prefix = StringField('Name', [
                           Length(max=30, message='max lenth 50 allowed'),
                           DataRequired(),
                           #Regexp('^\w+$', message="vm_name_prefix must contain only letters numbers or underscore")
        ])
        list_ip = Pip.split(",")
        vm_master_ip = SelectField(u'VM Master IP', choices = [(ip, ip) for ip in list_ip])
        for i in range(vm_nodecount1-1):
            locals()['vm_worker_ip{}'.format(i)] = SelectField(u'VM Worker IP {}'.format(i), choices = [(ip, ip) for ip in list_ip])
        vm_username = StringField('vm_username', validators=[DataRequired(), Length(max=30)])
        vm_key_based_auth = BooleanField('Key based authentication', default=False, id = 'vm_key_based_auth_abc')
        vm_password = PasswordField('vm_password', id = 'vm_password_abc')
        vm_key_path = FileField('Key Path In Infra Node')
        submit = SubmitField('Add VM Detail to Cluster')
        def validate_vm_ip(self, vm_ip):
            cluster_id = request.args.get('id')
            node_ip = Vm_node.query.filter_by(vm_ip=vm_ip.data).first()
            node_ip1 = Vm_node.query.filter_by(cluster_id=cluster_id).first()
            if node_ip is not None:
                raise ValidationError('Please use a different node ips.')
            if node_ip1 is not None:
                raise ValidationError('Only one vm node ip detail can be added in a cluster')
        def validate_vm_name_prefix(self, vm_name_prefix):
            #cluster_id = request.args.get('id')
            vm_name_prefix = Vm_node.query.filter_by(vm_master_ip=vm_name_prefix.data).first()
            if vm_name_prefix is not None:
                raise ValidationError('Please use a different vm_name_prefix , this vm_name_prefix is already in use.')

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
        #value = dict(form.vm_worker_ip.choices).get(str(form.vm_worker_ip.data))
        vm_worker_ip_list =[]
        for i in range(vm_nodecount1-1):
                field_value = getattr(form, 'vm_worker_ip{}'.format(i)).data
                vm_worker_ip_list.append(str(field_value))

        resultString = ','.join(vm_worker_ip_list)
        vm_node_data = Vm_node(vm_master_ip=str(form.vm_master_ip.data),
                                             vm_worker_ip=resultString,
                                             vm_name_prefix=form.vm_name_prefix.data,
                                             vm_username=form.vm_username.data,
                                             vm_key_based_auth=form.vm_key_based_auth.data,
                                             vm_password=form.vm_password.data,
                                             vm_key_path=finalpath_key,
                                             cluster_id=cluster_id)
        db.session.add(vm_node_data)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('vm_node.vm_nodes',cluster_id=cluster_id))
                                #,cluster_id=cluster_id))
    return render_template('vm_node/vm_node.html', title='vm_node', form=form, vm_nodecount = vm_nodecount1 )

@bp.route('/vm_nodes/<int:cluster_id>', methods=['GET', 'POST'])
#@login_required
def vm_nodes(cluster_id):
    userID_exist = session['userID_exist']
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
