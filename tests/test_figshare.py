from fastapi.testclient import TestClient

from readme_tool.figshare import app, api_version

client = TestClient(app)

article_id = 12966581
stage_article_id = 6941778


def test_figshare_get():
    # Production
    response = client.get(f'/api/{api_version}/figshare/{article_id}')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['id'] == article_id

    # Stage
    response = client.get(f'/api/{api_version}/figshare/{stage_article_id}?stage=True')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['id'] == stage_article_id


def test_metadata_get():
    # Production
    response = client.get(f'/api/{api_version}/metadata/{article_id}')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['article_id'] == article_id

    # Stage
    response = client.get(f'/api/{api_version}/metadata/{stage_article_id}?stage=True')
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['article_id'] == stage_article_id
