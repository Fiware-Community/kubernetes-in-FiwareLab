from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import db
from app.auth.forms import LoginForm, RegistrationForm, LoginForm1, RegistrationForm1
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app.auth import bp
import mysql.connector
from mysql.connector import Error
from flask import session
@bp.route('/<sub>', methods=['GET', 'POST','DELETE'])
def userLogin_auth(sub):
        session['projectid']= str(sub)
        project_id = session['projectid']
        connection = mysql.connector.connect(host='localhost',
                                                database='db',
                                                user='root',
                                                password='Abc@1234')

        cursor = connection.cursor()
        sql_select_query = """select username from user where username = (%s) """
        cursor.execute(sql_select_query,(project_id,))
        db_user = cursor.fetchone()
        ip = request.args.get('ip')
        instance_ip = ''.join(ip)
        instance_ip.encode('ascii','ignore')
        if db_user is None:
                sub1= User(username=project_id,Projectip=instance_ip)
                db.session.add(sub1)
                db.session.commit()
                print(sub1)
                return redirect(url_for('main.index'))

        else:
                try:
                        sql = '''UPDATE user SET Projectip = (%s) WHERE username = (%s) '''
                        cursor.execute(sql,(instance_ip,project_id))
                        connection.commit()
                except:
                        connection.rollback()
                finally:
                        return render_template('cluster/clusters.html',project_id = project_id)

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
        '''if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login1'))'''
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
        print "Login form is submitted"
    elif register_form.register.data and register_form.validate():
            #register_form.validate_on_submit():
            #and register_form.register.data:
        #user = User(username=register_form.username1.data, email=register_form.email.data)
        user = User(username=register_form.username1.data )
        #user.set_password(register_form.password.data)
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
