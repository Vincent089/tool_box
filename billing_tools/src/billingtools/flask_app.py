import os
from flask import Flask, render_template, request, abort, send_from_directory, redirect
from flask_sse import sse
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.xml']
app.config['UPLOAD_PATH'] = '/src/input_file'
app.config["REDIS_URL"] = "redis://redis:6379"
app.register_blueprint(sse, url_prefix='/stream')

def update_stream():
    filenames = next(os.walk(app.config['UPLOAD_PATH']), (None, None, []))[2]  # [] if no file
    sse.publish({"files": filenames}, type='files-list')


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@app.errorhandler(400)
def unwanted_file(e):
    return "File is not an XML", 400


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)


@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)

    # makes sure we have a file
    if filename != '':
        # only keeps the file name and not his path
        file_ext = os.path.splitext(filename)[1]

        # checks if the file match the extensions we allow
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)

        # save the file in dir
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))

        # update stream
        sse.publish({"filename": filename}, type='new-file')

    return '', 204


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename, as_attachment=True)


@app.route('/delete/<filename>', methods=['DELETE'])
def delete_report(filename):
    os.remove(os.path.join(app.config['UPLOAD_PATH'], filename))
    return '', 204