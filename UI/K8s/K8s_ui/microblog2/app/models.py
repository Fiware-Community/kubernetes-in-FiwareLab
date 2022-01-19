from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from flask_login import UserMixin
from flask import url_for


# cli API
class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


# GUI DB Model for User
class User(PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    #    posts = db.relationship('Post', backref='author', lazy='dynamic')
    clusters = db.relationship('Cluster', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # cli API
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            # 'post_count': self.clusters.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id)
                # 'followers': url_for('api.get_', id=self.id),
            }
        }
        if include_email:
            data['email'] = self.email
        return data


# quit()

# GUI DB Model for Cluster
class Cluster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cluster_name = db.Column(db.String(50), index=True, unique=True, nullable=False)
    description = db.Column(db.String(200))
    cluster_type = db.Column(db.String(20), nullable=False)
    cluster_os = db.Column(db.String(20), nullable=False)
    node_count = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    openstack_nodes = db.relationship('Openstack_node', backref='cluster', lazy=True, uselist=False)
    #openstack_node = db.relationship("Openstack_node", uselist=False, back_populates="cluster")
#    aws_nodes = db.relationship('Aws_node', backref='cluster', lazy=True)
#    vm_nodes = db.relationship('Vm_node', backref='cluster', lazy=True)

    def __repr__(self):
        return '<Cluster {}>'.format(self.cluster_name)


# GUI DB Model for Openstack node
class Openstack_node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.VARCHAR(120), index=True, unique=True, nullable=False)
    flavor_name = db.Column(db.VARCHAR(120), nullable=False)
    image_name = db.Column(db.VARCHAR(120), nullable=False)
    security_group_name = db.Column(db.VARCHAR(120), nullable=False)
    keypair_name = db.Column(db.VARCHAR(120), nullable=False)
    key_path = db.Column(db.VARCHAR(400), nullable=False)
    private_network_name = db.Column(db.VARCHAR(120), nullable=False)
    external_network_name = db.Column(db.VARCHAR(120), nullable=False)
    status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    auth_url = db.Column(db.VARCHAR(50), nullable=False)
    username = db.Column(db.VARCHAR(50), nullable=False)
    password = db.Column(db.VARCHAR(50), nullable=False)
    project_name = db.Column(db.VARCHAR(50), nullable=False)
    user_domain_name = db.Column(db.VARCHAR(50), nullable=False)
    project_domain_name = db.Column(db.VARCHAR(50), nullable=False)
    region_name = db.Column(db.VARCHAR(50), nullable=False)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'), nullable=False)
    #cluster = db.relationship("Cluster", back_populates="openstack_node")

    def __repr__(self):
        return '<Openstack_node {}>'.format(self.node_name)


# GUI DB Model for AWS node
class Aws_node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(120), index=True, unique=True, nullable=False)
    image_name = db.Column(db.VARCHAR(120), nullable=False)
    security_group_name = db.Column(db.VARCHAR(120), nullable=False)
    instance_type = db.Column(db.VARCHAR(120), nullable=False)
    REGION = db.Column(db.VARCHAR(120), nullable=False)
    ACCESS_KEY_ID = db.Column(db.VARCHAR(120), nullable=False)
    SECRET_ACCESS_KEY = db.Column(db.VARCHAR(120), nullable=False)
    keypair_name = db.Column(db.VARCHAR(120), nullable=False)
    key_path = db.Column(db.VARCHAR(400), nullable=False)
    vpc_subnet_id = db.Column(db.VARCHAR(120), nullable=False)
    status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'), nullable=False)

#    def __repr__(self):
#        return '<Aws_node {}>'.format(self.name)


# GUI DB Model for VM node
class Vm_node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vm_name_prefix = db.Column(db.VARCHAR(30), index=True, unique=True, nullable=False)
    vm_ip = db.Column(db.TEXT(120), nullable=False)
    vm_username = db.Column(db.VARCHAR(30), nullable=False)
    vm_key_based_auth = db.Column(db.Boolean(), nullable=False)
    vm_password = db.Column(db.VARCHAR(30))
    vm_key_path = db.Column(db.VARCHAR(400))
#    status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'), nullable=False)

#   def __repr__(self):
#        return '<vm_name_prefix {}>'.format(self.vm_name_prefix)

# GUI DB Model for VM node
class Component(db.Model):
    components_detail_id = db.Column(db.Integer, primary_key=True)
    enable_orion = db.Column(db.Boolean(), nullable=False)
    enable_sth_comet = db.Column(db.Boolean(), nullable=False)
    enable_cygnus_sth = db.Column(db.Boolean(), nullable=False)
    enable_cygnus_sth = db.Column(db.Boolean(), nullable=False)
    enable_iotagent = db.Column(db.Boolean(), nullable=False)
    enable_quantumleap = db.Column(db.Boolean(), nullable=False)
    enable_draco = db.Column(db.Boolean(), nullable=False)
    enable_ckan = db.Column(db.Boolean(), nullable=False)
    orion_version = db.Column(db.VARCHAR(120), nullable=False)
    mongodb_version = db.Column(db.VARCHAR(120), nullable=False)
    sth_version = db.Column(db.VARCHAR(120), nullable=False)
    sth_mongo_version = db.Column(db.VARCHAR(120), nullable=False)
    cygnus_sth_version = db.Column(db.VARCHAR(120), nullable=False)
    iot_version = db.Column(db.VARCHAR(120), nullable=False)
    quantumleap_version = db.Column(db.VARCHAR(120), nullable=False)
    crate_version = db.Column(db.VARCHAR(120), nullable=False)
    draco_version = db.Column(db.VARCHAR(120), nullable=False)
    status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'), nullable=False)
#    def __repr__(self):
#        return '<name {}>'.format(self.name)

class Deployment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cluster_id = db.Column(db.Integer, db.ForeignKey('cluster.id'))
#    deployment_log = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    #def __repr__(self):
     #   return '<Deployment {}>'.format(self.deployment_log)

class Deployment_log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deployment_id = db.Column(db.Integer, db.ForeignKey('deployment.id'))
    task = db.Column(db.String(200))
    log_type = db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return '<Deployment_log {}>'.format(self.task)

class Pxe_server(db.Model):
    pxe_server_id = db.Column(db.Integer, primary_key=True)
    dhcp_subnet_ip = db.Column(db.VARCHAR(50), nullable=False)
    dhcp_subnet_netmask = db.Column(db.VARCHAR(50), nullable=False)
    dhcp_interface_name = db.Column(db.VARCHAR(50), nullable=False)
    pxe_internet_interface_name = db.Column(db.VARCHAR(50), nullable=False)
    dhcp_interface_ip = db.Column(db.VARCHAR(50), nullable=False)
    dhcp_interface_netmask = db.Column(db.VARCHAR(50), nullable=False)
    dhcp_subnet_range_begin = db.Column(db.VARCHAR(50), nullable=False)
    dhcp_subnet_range_end = db.Column(db.VARCHAR(50), nullable=False)
    dhcp_subnet_domain_name_servers = db.Column(db.VARCHAR(50), nullable=False)
    status = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, index=True, default=datetime.now)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
