from flask_wtf import Form
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField, validators
from wtforms.validators import ValidationError, DataRequired, Length, Regexp
from app.models import Cluster


class ClusterCreationForm(Form):
    cluster_name = StringField('Name', [
                           Length(max=50, message='max lenth 50 allowed'),
                           DataRequired(),
                           Regexp('^\w+$', message="Username must contain only letters numbers or underscore")
        ])
    description = TextAreaField(u'Description', [validators.optional(), validators.length(max=30)])
    cluster_type = SelectField(u'Cluster Type', choices=[('openstack', 'openstack'), ('AWS', 'AWS'), ('baremetal', 'baremetal')],id='cluster_type_abc')
    cluster_os = SelectField(u'OS Type', choices=[('centos', 'centos'), ('ubuntu', 'ubuntu')])
    node_count = IntegerField('Node Count', default=4, id = 'node_count_abc')
        #FormField(NumberRange(min=1, max=100, message="value must be integer between 1 to 100"))
        #BooleanField('node_count', validators=[DataRequired(),NumberRange(min=1, max=100, message="range of count can be 1 to 100")])
    submit = SubmitField('Create Cluster')

    def validate_cluster_name(self, cluster_name):
        cluster_name = Cluster.query.filter_by(cluster_name=cluster_name.data).first()
        if cluster_name is not None:
            raise ValidationError('Please use a different cluster name.')
