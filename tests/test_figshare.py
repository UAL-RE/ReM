from typing import Union
from fastapi.testclient import TestClient
from fastapi import FastAPI

from readme_tool import figshare

app = FastAPI()
app.include_router(figshare.router)
client = TestClient(app)

# Production test
article_id = 12966581
curation_id = 540005

# Stage test
stage_article_id = 6941778
stage_curation_id = 453842

value_400 = [-1, 0]


def test_figshare_get(figshare_api_key, figshare_stage_api_key):
    def _client_get(article_id0: Union[int, str] = '',
                    curation_id0: Union[int, str] = '',
                    stage: bool = False):
        return client.get(f'/figshare/'
                          f'{article_id0}/{curation_id0}?stage={stage}')

    figshare.api_key = figshare_api_key
    figshare.stage_api_key = figshare_stage_api_key

    # Production
    ############
    response = _client_get(article_id, curation_id)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['article_id'] == article_id
    assert response.json()['id'] == curation_id

    # Check for incorrect entries with prod endpoint
    response = _client_get(stage_article_id)
    assert response.status_code == 404

    for i in value_400:
        response = _client_get(i, i)
        assert response.status_code == 400

    response = _client_get()
    assert response.status_code == 404

    # Stage
    #######
    response = _client_get(stage_article_id, stage_curation_id, stage=True)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['article_id'] == stage_article_id
    assert response.json()['id'] == stage_curation_id

    # Check for incorrect entries with stage endpoint
    response = _client_get(article_id, curation_id, stage=True)
    assert response.status_code == 404

    for i in value_400:
        response = _client_get(i, i, stage=True)
        assert response.status_code == 400

    response = _client_get(stage=True)
    assert response.status_code == 404


def test_metadata_get(figshare_api_key, figshare_stage_api_key):
    def _client_get(article_id0: Union[int, str] = '',
                    curation_id0: Union[int, str] = '',
                    stage: bool = False):
        return client.get(f'/metadata/'
                          f'{article_id0}/{curation_id0}?stage={stage}')

    figshare.api_key = figshare_api_key
    figshare.stage_api_key = figshare_stage_api_key

    # Production
    ############
    response = _client_get(article_id, curation_id)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['article_id'] == article_id

    # Check for incorrect entries with prod endpoint
    response = _client_get(stage_article_id)
    assert response.status_code == 404

    for i in value_400:
        response = _client_get(i, i)
        assert response.status_code == 400

    response = _client_get()
    assert response.status_code == 404

    # Stage
    #######
    response = _client_get(stage_article_id, stage_curation_id,
                           stage=True)
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()['article_id'] == stage_article_id

    # Check for incorrect entries with stage endpoint
    response = _client_get(article_id, curation_id,
                           stage=True)
    assert response.status_code == 404

    for i in value_400:
        response = _client_get(i, i, stage=True)
        assert response.status_code == 400

    response = _client_get(stage=True)
    assert response.status_code == 404
