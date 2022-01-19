from flask import Blueprint, render_template, request
from ..utility.utility import Utility
from subprocess import check_output
from werkzeug import secure_filename

mod = Blueprint('home', __name__, template_folder='templates')
logger = Utility.create_logger()


@mod.route('/')
def homepage():
    return render_template('/index.html')


@mod.route('/buttonclick', methods=['POST'])
def button_click():
    stdout = Utility.run_test_script()
    logger.debug(request)
    return render_template('/test.html', test=stdout.decode('utf-8'))


@mod.route('/nextpage',  methods=['POST'])
def nextpage():
    return render_template('/browse_file.html')


@mod.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    print(request)
    if request.method == 'POST':
        f = request.files['file']
        print(f.filename)
        f.save(secure_filename(f.filename))
        return f.filename + ' file uploaded successfully'
