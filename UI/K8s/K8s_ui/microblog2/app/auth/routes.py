from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import db
from app.auth.forms import LoginForm, RegistrationForm, LoginForm1, RegistrationForm1
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.auth import bp


# ...
#@app.route('/')
#@app.route('/index', methods=['GET', 'POST'])
#@login_required
#def index():
#    return render_template('index.html')
@bp.route('/login1', methods=['GET', 'POST'])
def login1():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LoginForm1()
    register_form = RegistrationForm1()
    if login_form.login.data and login_form.validate():
            #login_form.validate_on_submit():
        #and login_form.login.data:
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login1'))
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
        print "Login form is submitted"
    elif register_form.register.data and register_form.validate():
            #register_form.validate_on_submit():
            #and register_form.register.data:
        user = User(username=register_form.username1.data, email=register_form.email.data)
        user.set_password(register_form.password.data)
        print "reg worng"
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login1'))
        print "Register form is submitted"
    return render_template('auth/login1.html', title='Sign In', login_form=login_form,register_form=register_form)




@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
        # return redirect(url_for('index'))
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)
    #return render_template('auth/register.html', title='Register', form=form)