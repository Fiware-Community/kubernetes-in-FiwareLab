from flask import url_for
from flask_login import UserMixin
from app import db
# ...

class User(UserMixin, db.Model):
    # ...

    def from_dict(self, data, new_user=False):
        for field in ['username']:
            if field in data:
                setattr(self, field, data[field])
        '''if new_user and 'password' in data:
            self.set_password(data['password'])'''
