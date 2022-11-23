from flask_wtf import Form
from flask import request
from wtforms import StringField, SubmitField, PasswordField, FileField, TextAreaField, validators, BooleanField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, Regexp
from app.models import Vm_node, User
import mysql.connector
from mysql.connector import Error
from app.cluster.routes import a

#for vm_node
connection1 = mysql.connector.connect(host='localhost',
                                      database='db',
                                      user='root',
                                      password='Abc@1234')
cursor1 = connection1.cursor()
sql_select_query1 = """select Projectip from user where username = (%s) """
cursor1.execute(sql_select_query1,(a,))
get_ip = cursor1.fetchone()
if get_ip is None:
	get_ip1 = User(Projectip=get_ip)
	db.session.add(get_ip1)
        db.session.commit()
else:
	Pip = str(get_ip[0])				


class VmNodeCreationForm(Form):
    vm_name_prefix = StringField('Name', [
                           Length(max=30, message='max lenth 50 allowed'),
                           DataRequired(),
                           #Regexp('^\w+$', message="vm_name_prefix must contain only letters numbers or underscore")
        ])
    #vm_ip = TextAreaField(u'vm_ips', [validators.optional(), validators.length(max=300)])
    list_ip = Pip.split(",")
    vm_master_ip = SelectField(u'VM Master IP', choices = [(ip, ip) for ip in list_ip])
    vm_worker_ip = SelectField(u'VM Worker IP', choices= [(ip, ip) for ip in list_ip])
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

