from flask import render_template, redirect, url_for, request
from app import db
from app.component.forms import ComponentAdditionForm, ComponentEditForm
from flask_login import login_required
from app.component import bp
from app.models import Component
from app.models import Cluster
from flask_login import current_user
from flask_table import Table, Col
from flask import jsonify
from app.cluster.routes import userID_exist
@bp.route('/component', methods=['GET', 'POST'])
#@login_required
def add_component():
    cluster_id = request.args.get('id')
    form = ComponentAdditionForm()
    if form.validate_on_submit():
        component_data = Component(enable_orion=form.enable_orion.data,
                                             orion_version=form.orion_version.data,
                                             mongodb_version=form.mongodb_version.data,
                                             enable_sth_comet=form.enable_sth_comet.data,
                                             sth_version=form.sth_version.data,
                                             sth_mongo_version=form.sth_mongo_version.data,
                                             enable_cygnus_sth=form.enable_cygnus_sth.data,
                                             cygnus_sth_version=form.cygnus_sth_version.data,
                                             enable_iotagent=form.enable_iotagent.data,
                                             iot_version=form.iot_version.data,
                                             enable_quantumleap=form.enable_quantumleap.data,
                                             quantumleap_version=form.quantumleap_version.data,
                                             crate_version=form.crate_version.data,
                                             enable_draco=form.enable_draco.data,
                                             draco_version=form.draco_version.data,
                                             enable_ckan=form.enable_ckan.data,
                                             status='Pending',
                                             cluster_id= cluster_id)
        db.session.add(component_data)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('component.component_all_list'))
  
    return render_template('component/add_component.html', title='add_component', form=form)

@bp.route('/edit_component/<cluster_id>', methods=['GET', 'POST'])
#@login_required
def edit_component(cluster_id):
    component_data = Component.query.filter_by(cluster_id=cluster_id).first_or_404()
    form = ComponentEditForm()
    form.enable_orion.data = component_data.enable_orion
    form.mongodb_version.data = component_data.mongodb_version
    form.enable_sth_comet.data = component_data.enable_sth_comet
    form.sth_version.data = component_data.sth_version
    form.enable_cygnus_sth.data = component_data.enable_cygnus_sth
    form.cygnus_sth_version.data = component_data.cygnus_sth_version
    form.enable_iotagent.data = component_data.enable_iotagent
    form.iot_version.data = component_data.iot_version
    form.enable_quantumleap.data = component_data.enable_quantumleap
    form.quantumleap_version.data = component_data.quantumleap_version
    form.crate_version.data = component_data.crate_version
    form.enable_draco.data = component_data.enable_draco
    form.draco_version.data = component_data.draco_version
    form.enable_ckan.data = component_data.enable_ckan
    data_dict=request.form.to_dict()
    print("------------> ",request.form.get("enable_quantumleap"))

    if data_dict and request.method== 'POST' :#and form.validate_on_submit():
        data_dict=request.form.to_dict()
        print("=== ",data_dict)
        def str_to_bool(s):
            if s == 'y':
                return True
            elif s == '':
                return False
        if 'enable_orion' in data_dict:
            component_data.enable_orion = str_to_bool(data_dict['enable_orion'].encode('ascii', 'ignore'))
        else:
            if component_data.enable_orion == True:
                component_data.enable_orion = False
        if 'orion_version' in data_dict:
            component_data.orion_version=data_dict['orion_version'].encode('ascii', 'ignore')
        if 'mongodb_version' in data_dict:
            component_data.mongodb_version=data_dict['mongodb_version'].encode('ascii', 'ignore')
        if 'enable_sth_comet' in data_dict:
            component_data.enable_sth_comet=str_to_bool(data_dict['enable_sth_comet'].encode('ascii', 'ignore'))
        else:
            if component_data.enable_sth_comet == True:
                component_data.enable_sth_comet = False
        if 'sth_version' in data_dict:
            component_data.sth_version=data_dict['sth_version'].encode('ascii', 'ignore')
        if 'sth_mongo_version' in data_dict:
            component_data.sth_mongo_version=data_dict['sth_mongo_version'].encode('ascii', 'ignore')
        if 'enable_cygnus_sth' in data_dict:
            component_data.enable_cygnus_sth=str_to_bool(data_dict['enable_cygnus_sth'].encode('ascii', 'ignore'))
        else:
            if component_data.enable_cygnus_sth == True:
                component_data.enable_cygnus_sth = False
        if 'cygnus_sth_version' in data_dict:
            component_data.cygnus_sth_version=data_dict['cygnus_sth_version'].encode('ascii', 'ignore')
        if 'enable_iotagent' in data_dict:
            component_data.enable_iotagent=str_to_bool(data_dict['enable_iotagent'].encode('ascii', 'ignore'))
        else:
            if component_data.enable_iotagent == True:
                component_data.enable_iotagent = False
        if 'iot_version' in data_dict:
            component_data.iot_version=data_dict['iot_version'].encode('ascii', 'ignore')
        if 'enable_quantumleap' in data_dict:
            component_data.enable_quantumleap=str_to_bool(data_dict['enable_quantumleap'].encode('ascii', 'ignore'))
        else:
            if component_data.enable_quantumleap == True:
                component_data.enable_quantumleap = False
        if 'quantumleap_version' in data_dict:
            component_data.quantumleap_version=data_dict['quantumleap_version'].encode('ascii', 'ignore')
        if 'crate_version' in data_dict:
            component_data.crate_version=data_dict['crate_version'].encode('ascii', 'ignore')
        if 'enable_draco' in data_dict:
            component_data.enable_draco=str_to_bool(data_dict['enable_draco'].encode('ascii', 'ignore'))
        else:
            if component_data.enable_draco == True:
                component_data.enable_draco = False
        if 'draco_version' in data_dict:
            component_data.draco_version=data_dict['draco_version'].encode('ascii', 'ignore')
        if 'enable_ckan' in data_dict:
            component_data.enable_ckan=str_to_bool(data_dict['enable_ckan'].encode('ascii', 'ignore'))
        else:
            if component_data.enable_ckan == True:
                component_data.enable_ckan = False
        try:
            db.session.commit()
        except:
            db.session.rollback()
            #flash('Database error, component could not be added to cluster')
        #return redirect(url_for('openstack_node.openstack_nodes'))
        return redirect(url_for('component.component_all_list'))
        #return redirect(url_for('main.index'))
    return render_template('component/edit_component.html', title='edit_component', form=form)


@bp.route('/component_list/<int:cluster_id>', methods=['GET', 'POST'])
#@login_required
def component_list(cluster_id):
    items = Component.query.filter_by(cluster_id=cluster_id).all()
    class ItemTable2(Table):
        classes = ['table']
        enable_orion = Col('Enable Orion')
        enable_sth_comet = Col('Enable Sth-Comet')
        enable_cygnus_sth = Col('Enable Cygnus-Sth')
        enable_iotagent = Col('enable_iotagent')
        enable_quantumleap = Col('Enable Quantumleap')
        enable_draco = Col('Enable Draco')
        enable_ckan = Col('Enable Ckan')

    table2 = ItemTable2(items)
    table2.border = True
    return render_template('component/component_list.html',
                           title='component_list',
                           table2=table2)

@bp.route('/component_all_list', methods=['GET', 'POST'])
#@login_required
def component_all_list():
    cluster_list = Cluster.query.filter_by(user_id=userID_exist).all()
    
    return render_template('component/all_component_list.html',
                           title='component_list',
                           cluster_list=cluster_list)


@bp.route('/component_list_api/<int:cluster_id>', methods=['GET', 'POST'])
#@login_required
def component_list_api(cluster_id):
    items_li = Component.query.filter_by(cluster_id=cluster_id).all()
    data=[]    
    final_data = {}
    if items_li:
        items = items_li[0]
        print(items)
        com_li = ["Orion","Sth-Comet","Cygnus-Sth","iotagent","Quantumleap","Draco","Ckan"]    
        data = [{"name":com_li[0],"state":items.enable_orion,"version":items.orion_version},
        {"name":com_li[1],"state":items.enable_sth_comet,"version":items.sth_version},
        {"name":com_li[2],"state":items.enable_cygnus_sth,"version":items.cygnus_sth_version},
        {"name":com_li[3],"state":items.enable_iotagent,"version":items.iot_version},
        {"name":com_li[4],"state":items.enable_quantumleap,"version":items.quantumleap_version},
        {"name":com_li[5],"state":items.enable_draco,"version":items.draco_version},
        {"name":com_li[6],"state":items.enable_ckan,"version":"N/A"},
        ]
        # edit_component = ButtonCol('Edit Components', "component.edit_component", url_kwargs=dict(cluster_id='cluster_id'))
        final_data = {"data":data,"cluster_id":cluster_id}
    return jsonify(final_data)
