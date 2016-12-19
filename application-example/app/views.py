import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
from werkzeug import secure_filename
import subprocess
from datetime import datetime
from app import app



# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    #print '.' in filename and \
    #       filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    #file = request.files['file']
    files = request.files.getlist("file")
    filenames = []
    addresses = []
    translated_files = []

    # check that both files are accepted
    if allowed_file(files[0].filename)==True and allowed_file(files[1].filename)==True:
        for file in files:
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            filenames.append(filename)
            filename_no_ext = filename.rsplit(".")[0]
            # Move the file form the temporal folder to
            # the upload folder we setup
            #flask is not great with paths, so we have to set the path every time
            #otherwise it gets left as the last path
            file.save(os.path.join(app.root_path, 'static/img/', filename))
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
            # runs subprocess of tesseract
            os.chdir(os.path.join(app.root_path, 'static/img/'))
            subprocess.check_call(["tesseract", filename, filename_no_ext])
            translated_files.append(filename_no_ext+'.txt')
            translated_file = open(filename_no_ext+'.txt', 'r')
            address = translated_file.read().replace('\n', '').replace('\t', '').strip()
            translated_file.close()
            addresses.append(address)

        address1 = addresses[0]
        address2 = addresses[1]
        #session['address1'] = address1
        #session['address2'] = address2
        return redirect(url_for('directions',
                                    address1=address1, address2=address2))
    else:
        return redirect(url_for('upload_error'))


@app.route('/directions/')
def directions():
    address1 = request.args['address1']
    address2 = request.args['address2']
    os.chdir(os.path.join(app.root_path, '../'))
    api_file = open('api_key.txt', 'r')
    api_key = api_file.read().strip()
    return render_template('directions.html',address1=address1, address2=address2, API_key=api_key)

@app.route('/upload_error/')
def upload_error():
    return render_template('error.html')
