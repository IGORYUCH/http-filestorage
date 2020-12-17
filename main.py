from flask import Flask, send_file, request, make_response, jsonify
from os import mkdir, listdir, remove, rmdir
from os.path import join, exists
from hashlib import md5
from io import BytesIO
from settings import *

app = Flask(__name__)


@app.errorhandler(405)
def handler_405(error):
    return make_response(jsonify({'error': 'method not allowed for requested url'}), 405)


@app.errorhandler(404)
def handler_404(error):
    return make_response(jsonify({'error': 'requested url not found'}), 404)


@app.route('/api/file/download', methods=['GET'])
def download_file():
    if 'Hash' in request.headers:
        hash = request.headers['Hash']
        prefix = hash[:2]
        absolute_filename = join(app.config['UPLOAD_FOLDER'], prefix, hash)

        if exists(absolute_filename):
            with open(absolute_filename, 'rb') as stored_file:
                data = stored_file.read()
            filename = data[-name_length:].decode('utf-8').strip()

            data_stream = BytesIO(data[:-name_length])
            data_stream.seek(0)

            return send_file(data_stream, attachment_filename=filename, as_attachment=True)
        else:
            return make_response(jsonify({'error': 'no such file'}), 404)
    else:
        return make_response(jsonify({'error': '"Hash" header not found'}), 400)


@app.route('/api/file/delete', methods=['DELETE'])
def delete_file():
    if 'Hash' in request.headers:
        hash = request.headers['Hash']
        prefix = hash[:2]
        folder = join(app.config['UPLOAD_FOLDER'], prefix)
        absolute_filename = join(folder, hash)

        if exists(absolute_filename):
            remove(absolute_filename)

            if not listdir(folder):
                rmdir(folder)

            return make_response(jsonify({hash: 'deleted'}), 200)
        else:
            return make_response(jsonify({'error': 'no such file'}), 404)
    else:
        return make_response(jsonify({'error': '"Hash" header not found'}), 400)


@app.route('/api/file/upload', methods=['POST'])
def upload_file():
    response = {}
    for file in request.files:
        file_storage = request.files[file]
        filename = file_storage.filename
        bytes_filename = filename.encode('utf-8')
        data = file_storage.read()
        hash = md5(data).hexdigest()
        prefix = hash[:2]

        folder = join(app.config['UPLOAD_FOLDER'], prefix)
        absolute_filename = join(folder, hash)

        if not exists(absolute_filename):
            if not exists(folder):
                mkdir(folder)

            adjusted_filename = b' ' * (name_length - len(bytes_filename)) + bytes_filename
            data = data + adjusted_filename

            with open(absolute_filename, 'wb') as stored_file:
                stored_file.write(data)
            response[filename] = hash
        else:
            response[filename] = None
    return make_response(jsonify(response), 200)


app.config.from_object(DevelopmentConfig)
name_length = app.config['ADJUSTED_NAME_LENGTH']

if __name__ == '__main__':
    app.run()
