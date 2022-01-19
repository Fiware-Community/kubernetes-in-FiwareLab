from flask_wtf import Form
from flask import request
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo, IPAddress
from app.models import Pxe_server

class PxeServerCreationForm(Form):
    dhcp_subnet_ip = StringField('dhcp subnet IP', validators=[DataRequired(),IPAddress(ipv4=True, ipv6=False, message=None)])
    dhcp_subnet_netmask = StringField('dhcp subnet netmask', validators=[DataRequired(),IPAddress(ipv4=True, ipv6=False, message=None)])
    dhcp_interface_name = StringField('dhcp interface name',
                                              validators=[DataRequired(), Length(max=50)])
    #pxe_server_ip = StringField('pxe server IP', validators=[DataRequired(),IPAddress(ipv4=True, ipv6=False, message=None)])
    pxe_internet_interface_name = StringField('pxe internet interface name', validators=[DataRequired(),Length(max=50)])

    dhcp_interface_ip = StringField('dhcp interface IP/pxe_server_ip', validators=[DataRequired(),IPAddress(ipv4=True, ipv6=False, message=None)])
    dhcp_interface_netmask = StringField('dhcp interface netmask', validators=[DataRequired(),IPAddress(ipv4=True, ipv6=False, message=None)])
    dhcp_subnet_range_begin = StringField('dhcp subnet range begin', validators=[DataRequired(),IPAddress(ipv4=True, ipv6=False, message=None)])
    dhcp_subnet_range_end = StringField('dhcp subnet range end', validators=[DataRequired(),IPAddress(ipv4=True, ipv6=False, message=None)])
    dhcp_subnet_domain_name_servers = StringField('dhcp subnet domain name servers', validators=[DataRequired()])

    submit = SubmitField('Add pxe server Details')

    """def validate_node_name(self, node_name):
        cluster_id = request.args.get('id')
        node_name = Openstack_node.query.filter_by(node_name=node_name.data).first()
        node_name1 = Openstack_node.query.filter_by(cluster_id=cluster_id).first()
        if node_name is not None:
            raise ValidationError('Please use a different node name.')
        elif node_name1 is not None:
            raise ValidationError('Only one node detail can be added in a cluster')"""