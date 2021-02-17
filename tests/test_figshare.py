from typing import Union
from fastapi.testclient import TestClient

from readme_tool.figshare import app, api_version

client = TestClient(app)

article_id = 12966581
stage_article_id = 6941778

value_400 = [-1, 0]


def test_figshare_get():
    def _client_get(article_id0: Union[int, str] = '', stage=False):
        return client.get(f'/api/{api_version}/figshare/'
                          f'{article_id0}?stage={stage}')

    # Production
    response = _client_get(article_id)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['id'] == article_id

    # Check for incorrect entry
    response = _client_get(stage_article_id)
    assert response.status_code == 404

    for i in value_400:
        response = _client_get(i)
        assert response.status_code == 400

    response = _client_get()
    assert response.status_code == 404

    # Stage
    response = _client_get(stage_article_id, stage=True)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['id'] == stage_article_id

    # Check for incorrect entry
    response = _client_get(article_id, stage=True)
    assert response.status_code == 404

    for i in value_400:
        response = _client_get(i, stage=True)
        assert response.status_code == 400

    response = _client_get(stage=True)
    assert response.status_code == 404


def test_metadata_get():
    def _client_get(article_id0: Union[int, str] = '', stage=False):
        return client.get(f'/api/{api_version}/metadata/'
                          f'{article_id0}?stage={stage}')

    # Production
    response = _client_get(article_id)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['article_id'] == article_id

    # Check for incorrect entry
    response = _client_get(stage_article_id)
    assert response.status_code == 404

    for i in value_400:
        response = _client_get(i)
        assert response.status_code == 400

    response = _client_get()
    assert response.status_code == 404

    # Stage
    response = _client_get(stage_article_id, stage=True)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['article_id'] == stage_article_id

    # Check for incorrect entry
    response = _client_get(article_id, stage=True)
    assert response.status_code == 404

    for i in value_400:
        response = _client_get(i, stage=True)
        assert response.status_code == 400

    response = _client_get(stage=True)
    assert response.status_code == 404
