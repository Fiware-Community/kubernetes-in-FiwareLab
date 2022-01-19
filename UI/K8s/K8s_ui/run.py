from blue import app
UPLOAD_FOLDER = '/home/necuser/Downloads/flask_pro1'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.run(debug=True)