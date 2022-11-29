from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Regexp
from app.models import User


class LoginForm1(Form):
    username = StringField('Username', [
                           Length(min=3, max=50, message='Lenth must be between 3 to 50'),
                           DataRequired(),
                           Regexp('^\w+$', message="Username must contain only letters numbers or underscore")
        ])
    remember_me = BooleanField('Remember Me')

    login = SubmitField('Login')


class RegistrationForm1(Form):
    username1 = StringField('Username', [
                           Length(min=3, max=50, message='Lenth must be between 3 to 50'),
                           DataRequired(),
                           Regexp('^\w+$', message="Username must contain only letters numbers or underscore")
        ])
    register = SubmitField('Register')

    def validate_username1(self, username1):
        user = User.query.filter_by(username=username1.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')



class LoginForm(Form):
    username = StringField('Username', [
        Length(min=3, max=50, message='Lenth must be between 3 to 50'),
        DataRequired(),
        Regexp('^\w+$', message="Username must contain only letters numbers or underscore")
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(Form):
    username = StringField('Username', [
        Length(min=3, max=50, message='Lenth must be between 3 to 50'),
        DataRequired(),
        Regexp('^\w+$', message="Username must contain only letters numbers or underscore")
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

