from requests import get, post, delete
from werkzeug.http import parse_options_header
from os import urandom
from random import choices, randint
from io import BytesIO

HOSTNAME = 'localhost:80'


def test_upload_hash_returned():
    letters = ['a', 'b', 'c', 'd', 'f']
    filename = ''.join(choices(letters, k=randint(1, 6))) + '.' + ''.join(choices(letters, k=randint(1, 6)))
    file_stream = BytesIO(urandom(1024))
    file_stream.seek(0)
    files = {filename: (filename, file_stream, 'multipart/form-data')}
    result = post('http://{0}/api/file/upload'.format(HOSTNAME), files=files)
    json = result.json()
    assert result.status_code == 200 and json[filename]
    return {'filename':filename, 'stream':file_stream, 'hash':json[filename]}


def test_download_file_returned():
    file = test_upload_hash_returned()
    headers = {'Hash':file['hash']}
    result = get('http://{0}/api/file/download'.format(HOSTNAME), headers=headers)
    downloaded_filename = parse_options_header(result.headers['Content-Disposition'])[1]['filename']
    file['stream'].seek(0)
    assert result.status_code == 200 and file['stream'].read() == result.content and downloaded_filename == file['filename']


def test_delete_deleted_file_hash_returned():
    file = test_upload_hash_returned()
    headers = {'Hash': file['hash']}
    result = delete('http://{0}/api/file/delete'.format(HOSTNAME), headers=headers)
    json = result.json()
    assert result.status_code == 200 and json[file['hash']] == 'deleted'


def test_download_not_exists_returned():
    headers = {'Hash': 'nonexistent_hashe'}
    result = get('http://{0}/api/file/download'.format(HOSTNAME), headers=headers)
    json = result.json()
    assert result.status_code == 404 and json.get('error', None)


def test_upload_exists_returned():
    file = test_upload_hash_returned()
    file['stream'].seek(0)
    files = {file['filename']: (file['filename'], file['stream'], 'multipart/form-data')}
    result = post('http://{0}/api/file/upload'.format(HOSTNAME), files=files)
    json = result.json()
    assert result.status_code == 200 and not json[file['filename']]


def test_delete_not_exists_returned():
    headers = {'Hash': 'nonexistent_hashe'}
    result = delete('http://{0}/api/file/delete'.format(HOSTNAME), headers=headers)
    json = result.json()
    assert result.status_code == 404 and json.get('error', None)
