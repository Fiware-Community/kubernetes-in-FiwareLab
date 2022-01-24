from flask_wtf import Form
from wtforms import BooleanField, SubmitField, SelectField
from app.models import Component
from wtforms.validators import ValidationError
from flask import request

class ComponentAdditionForm(Form):
    enable_orion = BooleanField('Enable_Orion', default=False )
    orion_version = SelectField(u'Orion Version', choices=[('latest', 'latest'), ('2.3.0', '2.3.0'),
                                                        ('2.2.0', '2.2.0'), ('2.1.0', '2.1.0'),
                                                        ('2.0.0', '2.0.0'), ('1.15.1', '1.15.1'),
                                                        ('1.15.0', '1.15.0'), ('1.14.0', '1.14.0')
                                                        ])
    mongodb_version = SelectField(u'Mongodb Version', choices=[('3.4', '3.4'), ('3.6', '3.6')])

    enable_sth_comet = BooleanField('Enable Sth Comet', default=False )
    sth_version = SelectField(u'Sth Version', choices=[('2.7.0', '2.7.0'), ('2.6.0', '2.6.0'), ('2.5.0', '2.5.0')])
    sth_mongo_version = SelectField(u'STH Mongo Version', choices=[('4.0', '4.0'), ('3.6', '3.6'), ('3.4', '3.4')])

    enable_cygnus_sth = BooleanField('Enable Cygnus Sth', default=False )
    cygnus_sth_version = SelectField(u'Cygnus Sth Version', choices=[('1.7.1', '1.7.1')])

    enable_iotagent = BooleanField('Enable Iotagent', default=False )
    iot_version = SelectField(u'Iot Version', choices=[('1.13.0', '1.13.0'), ('1.12.0', '1.12.0'), ('1.11.0', '1.11.0')])

    enable_quantumleap = BooleanField('Enable Quantumleap', default=False )
    quantumleap_version = SelectField(u'Quantumleap Version', choices=[('0.7.5', '0.7.5'), ('0.7.4', '0.7.4')])
    crate_version = SelectField(u'Crate Version', choices=[('3.1.2', '3.1.2'), ('3.1.6', '3.1.6'), ('3.3.4', '3.3.4')])

    enable_draco = BooleanField('Enable Draco', default=False )
    draco_version = SelectField(u'Draco Version', choices=[('FIWARE_7.8.1', 'FIWARE_7.8.1'), ('latest', 'latest'),
                                                        ('1.3.1', '1.3.1'), ('1.3.0', '1.3.0')])

    enable_ckan = BooleanField('Enable CKAN', default=False )

    submit = SubmitField('Add Components to cluster')
    def validate_submit(self, submit):
        cluster_id = request.args.get('id')
        comp_details = Component.query.filter_by(cluster_id=cluster_id).first()
        if comp_details is not None:
            raise ValidationError('Component already added to cluster, Please use Edit Component')

class ComponentEditForm(Form):
    enable_orion = BooleanField('Enable_Orion', default=False )
    orion_version = SelectField(u'Orion Version', choices=[('latest', 'latest'), ('2.3.0', '2.3.0'),
                                                        ('2.2.0', '2.2.0'), ('2.1.0', '2.1.0'),
                                                        ('2.0.0', '2.0.0'), ('1.15.1', '1.15.1'),
                                                        ('1.15.0', '1.15.0'), ('1.14.0', '1.14.0')
                                                        ])
    mongodb_version = SelectField(u'Mongodb Version', choices=[('3.4', '3.4'), ('3.6', '3.6')])

    enable_sth_comet = BooleanField('Enable Sth Comet', default=False )
    sth_version = SelectField(u'Sth Version', choices=[('2.7.0', '2.7.0'), ('2.6.0', '2.6.0'), ('2.5.0', '2.5.0')])
    sth_mongo_version = SelectField(u'STH Mongo Version', choices=[('4.0', '4.0'), ('3.6', '3.6'), ('3.4', '3.4')])

    enable_cygnus_sth = BooleanField('Enable Cygnus Sth', default=False )
    cygnus_sth_version = SelectField(u'Cygnus Sth Version', choices=[('1.7.1 ', '1.7.1')])

    enable_iotagent = BooleanField('Enable Iotagent', default=False )
    iot_version = SelectField(u'Iot Version', choices=[('1.13.0', '1.13.0'), ('1.12.0', '1.12.0'), ('1.11.0', '1.11.0')])

    enable_quantumleap = BooleanField('Enable Quantumleap', default=False )
    quantumleap_version = SelectField(u'Quantumleap Version', choices=[('0.7.5', '0.7.5'), ('0.7.4', '0.7.4')])
    crate_version = SelectField(u'Crate Version', choices=[('3.1.2', '3.1.2'), ('3.1.6', '3.1.6'), ('3.3.4', '3.3.4')])

    enable_draco = BooleanField('Enable Draco', default=False )
    draco_version = SelectField(u'Draco Version', choices=[('FIWARE_7.8.1', 'FIWARE_7.8.1'), ('latest', 'latest'),
                                                        ('1.3.1', '1.3.1'), ('1.3.0', '1.3.0')])
    enable_ckan = BooleanField('Enable CKAN', default=False )
    submit = SubmitField('Edit Components to cluster')
