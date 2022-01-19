from flask_wtf import Form
from flask import request
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import ValidationError, DataRequired, Length, EqualTo
from app.models import Aws_node

class AwsNodeCreationForm(Form):
    ACCESS_KEY_ID = StringField('ACCESS KEY ID', validators=[DataRequired(),Length(max=50)])
    SECRET_ACCESS_KEY = StringField('SECRET_ACCESS_KEY', validators=[DataRequired(),Length(max=50)])
    REGION = StringField('REGION', validators=[DataRequired(),Length(max=50)])

    name = StringField('Node Name', validators=[DataRequired(),Length(max=50)])
    image_name = StringField('Image Name', validators=[DataRequired(), Length(max=50)])
    instance_type = StringField('Instance Type', validators=[DataRequired(),Length(max=50)])
    security_group_name = StringField('Security Group Name', validators=[DataRequired(),Length(max=50)])
    keypair_name = StringField('Keypair Name', validators=[DataRequired(),Length(max=50)])
    key_path = FileField('Key Path In Infra Node')
    vpc_subnet_id = StringField('VPC Subnet Id', validators=[DataRequired(),Length(max=50)])
    submit = SubmitField('Add Node Detail to Cluster')

    def validate_name(self, name):
        cluster_id = request.args.get('id')
        node_name = Aws_node.query.filter_by(name=name.data).first()
        node_name1 = Aws_node.query.filter_by(cluster_id=cluster_id).first()
        if node_name is not None:
            raise ValidationError('Please use a different name.')
        elif node_name1 is not None:
            raise ValidationError('Only one node detail can be added in a cluster')