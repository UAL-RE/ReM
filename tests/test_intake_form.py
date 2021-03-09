from shutil import copy
import ast
from fastapi.testclient import TestClient

from readme_tool.intake_form import app, VersionModel

client = TestClient(app)

article_id = 12966581
doc_id = 1
new_article_id = 87654321
new_article_id2 = 12026436  # This is for addition testing

value_400 = [-1, 0]

test_file = 'tests_data/tinydb.json'
test_dup_file = 'tests_data/tinydb_dup.json'  # This is a copy for editing. Won't save
copy(test_file, test_dup_file)


def test_get_version():
    response = client.get(f'/version/')
    assert response.status_code == 200
    json_content = response.json()
    assert isinstance(json_content, dict)
    for key in VersionModel().dict():
        assert isinstance(json_content[key], str)


def test_get_db():
    response = client.get(
        f'/api/v1/intake/database/?db_file={test_dup_file}'
    )
    assert response.status_code == 200
    assert isinstance(response.content, bytes)


def test_get_data():
    url = '/api/v1/intake/database'

    # Check for default data
    response = client.get(
        f'{url}/{article_id}?db_file={test_dup_file}'
    )
    assert response.status_code == 200
    content = response.content
    assert isinstance(content, bytes)
    assert isinstance(ast.literal_eval(content.decode('UTF-8')), dict)

    # Check that index is returned
    response = client.get(
        f'{url}/{article_id}?db_file={test_dup_file}&index=True'
    )
    assert response.status_code == 200
    content = response.content
    assert isinstance(content, bytes)
    assert isinstance(ast.literal_eval(content.decode('UTF-8')), int)

    # Check for not available data
    response = client.get(
        f'{url}/{new_article_id}?db_file={test_dup_file}'
    )
    assert response.status_code == 404
    content = ast.literal_eval(response.content.decode())
    assert isinstance(content, dict)
    assert content['detail'] == "Record not found"


def test_add_data():
    post_data = {
        'article_id': 87654321,
        'summary': 'Summary data for add',
        'files': 'Files data for add',
    }

    response = client.post(
        f'/api/v1/intake/database/add?db_file={test_dup_file}',
        json=post_data
    )
    assert response.status_code == 200
    # assert isinstance(content, bytes)
    # assert isinstance(ast.literal_eval(content.decode('UTF-8')), dict)


def test_update_data():
    post_data = {
        'article_id': article_id,
        'summary': 'Summary data for add',
        'files': 'Files data for add',
    }
    response = client.post(f'/api/v1/intake/database/update/{doc_id}?db_file={test_dup_file}',
                           json=post_data)
    assert response.status_code == 200


def test_read_form():
    response = client.get(f'/api/v1/intake/{article_id}?db_file={test_dup_file}')
    assert response.status_code == 200
    content = response.content
    assert isinstance(content, bytes)
    assert isinstance(content.decode(), str)
    assert 'html' in content.decode()

    # Testing reading if record is not available
    response = client.get(f'/api/v1/intake/{new_article_id2}?db_file={test_dup_file}')
    assert response.status_code == 200
    content = response.content
    assert isinstance(content, bytes)
    assert isinstance(content.decode(), str)
    assert 'html' in content.decode()


def test_intake_post():
    post_data = {
        'summary': 'Summary data for add (extended)',
        'files': 'Files data for add (extended)',
    }
    response = client.post(
        f'/api/v1/intake/{article_id}?db_file={test_dup_file}',
        data=post_data)  # Use data for Form data
    assert response.status_code == 200
    content = response.content
    assert isinstance(content, bytes)
    assert isinstance(content.decode(), str)
    assert 'html' in content.decode()

    # Check addition of data
    response = client.post(
        f'/api/v1/intake/{new_article_id2}?db_file={test_dup_file}',
        data=post_data)  # Use data for Form data
    assert response.status_code == 200
    content = response.content
    assert isinstance(content, bytes)
    assert isinstance(content.decode(), str)
    assert 'html' in content.decode()
