from flask_wtf import Form
from flask import request
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo
from app.models import Openstack_node

class OpenstackNodeCreationForm(Form):
    auth_url = StringField('Auth URL', validators=[DataRequired(),Length(max=50)])
    username = StringField('User Name', validators=[DataRequired(),Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    project_name = StringField('Project Name', validators=[DataRequired(),Length(max=50)])
    user_domain_name = StringField('User Domain Name', validators=[DataRequired(), Length(max=50)])
    project_domain_name = StringField('Project Domain Name', validators=[DataRequired(),Length(max=50)])
    region_name = StringField('Region Name', validators=[DataRequired(), Length(max=50)])

    node_name = StringField('Node Name', validators=[DataRequired(),Length(max=50)])
    image_name = StringField('Image Name', validators=[DataRequired(), Length(max=50)])
    flavor_name = StringField('Flavor Name', validators=[DataRequired(),Length(max=50)])
    security_group_name = StringField('Security Group Name', validators=[DataRequired(),Length(max=50)])
    keypair_name = StringField('Keypair Name', validators=[DataRequired(),Length(max=50)])
    key_path = FileField('Key Path In Infra Node')
    private_network_name = StringField('Private Network Name', validators=[DataRequired(),Length(max=50)])
    external_network_name = StringField('External Network Name', validators=[DataRequired(),Length(max=50)])
    submit = SubmitField('Add Node Detail to Cluster')

    def validate_node_name(self, node_name):
        cluster_id = request.args.get('id')
        node_name = Openstack_node.query.filter_by(node_name=node_name.data).first()
        node_name1 = Openstack_node.query.filter_by(cluster_id=cluster_id).first()
        if node_name is not None:
            raise ValidationError('Please use a different node name.')
        elif node_name1 is not None:
            raise ValidationError('Only one node detail can be added in a cluster')