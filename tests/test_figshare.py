from typing import Union
from fastapi.testclient import TestClient
from fastapi import FastAPI

from readme_tool import figshare

app = FastAPI()
app.include_router(figshare.router)
client = TestClient(app)

# Production test (published)
article_id = 12966581
curation_id = 540005

# Stage test (published)
stage_article_id = 6941778
stage_curation_id = 453842

# Stage test (under review)
stage_article_underreview_id = 7048856
stage_curation_underreview_id = 492094

value_400 = [-1, 0]


def test_figshare_get(figshare_api_key, figshare_stage_api_key):
    main_test(figshare_api_key, figshare_stage_api_key, 'figshare')


def test_metadata_get(figshare_api_key, figshare_stage_api_key):
    main_test(figshare_api_key, figshare_stage_api_key, 'metadata')


def main_test(figshare_api_key, figshare_stage_api_key, endpoint):
    def _client_get(article_id0: Union[int, str] = '',
                    curation_id0: Union[int] = None,
                    stage: bool = False,
                    allow_approved: bool = True):
        # allow_approved set to ensure that it works with published data
        params = {
            'curation_id': curation_id0,
            'stage': stage,
            'allow_approved': allow_approved
        }
        return client.get(f'/{endpoint}/{article_id0}', params=params)

    def _bulk_test(article_id0, bad_article_id, c_list, approved_list,
                   code_list0, curation_key0, stage=False):
        for c_id in c_list:  # Checks with/without curation_id
            # Checks for both pending/approved cases
            for approved, s_code in zip(approved_list, code_list0):
                response = _client_get(article_id0,
                                       curation_id0=c_id,
                                       allow_approved=approved,
                                       stage=stage)
                assert response.status_code == s_code  # This is from FastAPI
                # print(article_id0, c_id, approved, s_code, response)
                assert isinstance(response.json(), dict)
                if s_code == 200:
                    assert response.json()['article_id'] == article_id0
                    if c_list is not None and not curation_key0:
                        assert response.json()[curation_key0] == curation_id

        # Check for incorrect entries with prod endpoint
        response = _client_get(bad_article_id, stage=stage)
        assert response.status_code == 404  # This is from figshare

        # Check for lack of article_id input
        response = _client_get(stage=stage)
        assert response.status_code == 404  # This is from FastAPI

        for i in value_400:
            for c_list in [None, i]:  # Checks with/without curation_id
                response = _client_get(i, curation_id0=c_list, stage=stage)
                assert response.status_code == 400  # This is from figshare

    curation_key = ''
    if endpoint == 'figshare':
        curation_key = 'id'
    if endpoint == 'metadata':
        curation_key = 'curation_id'

    figshare.api_key = figshare_api_key
    figshare.stage_api_key = figshare_stage_api_key

    allowed_list = [False, True]
    code_list = [401, 200]

    # Production
    ############
    _bulk_test(article_id, stage_article_id, [None, curation_id],
               allowed_list, code_list, curation_key, stage=False)

    # Stage
    #######
    # Check approved/published data
    _bulk_test(stage_article_id, article_id, [None, stage_curation_id],
               allowed_list, code_list, curation_key, stage=True)

    # Check under review data
    _bulk_test(stage_article_underreview_id, article_id,
               [None, stage_curation_underreview_id], allowed_list,
               [200, 200], curation_key, stage=True)
