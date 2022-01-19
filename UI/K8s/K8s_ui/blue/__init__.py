from flask import Flask 

app = Flask(__name__)


from blue.home.routes import mod


app.register_blueprint(home.routes.mod, url_prefix='/home')
