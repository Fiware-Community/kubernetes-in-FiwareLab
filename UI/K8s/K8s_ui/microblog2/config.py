# WTF_CSRF_ENABLED = True
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    rootdir = os.path.abspath(os.path.dirname(__file__ + "/../../../")) 
    SECRET_KEY = 'you-will-never-guess'
    WTF_CSRF_ENABLED = False
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Abc#1234@localhost/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Abc#1234'
    MYSQL_DB = 'db'