import requests

from fastapi import FastAPI
# from pydantic import BaseModel

app = FastAPI()


def figshare_metadata_readme(figshare_dict: dict):
    readme_dict = {
        'title': figshare_dict['title'],
        'description': figshare_dict['description'],
        'doi': figshare_dict['doi']
    }
    return readme_dict


@app.get('/figshare/{article_id}')
def figshare_get(article_id: int, stage: bool = False):
    """
    Retrieve Figshare metadata

    :param article_id: Figshare article ID
    :param stage: Figshare stage or production API.
                  Stage is available for Figshare institutions
    :return response: dict
    """

    if not stage:
        base_url = "https://api.figshare.com"
    else:
        base_url = "https://api.figsh.com"

    url = f"{base_url}/v2/articles/{article_id}"

    response = requests.get(url)
    return response.json()


@app.get('/metadata/{article_id}')
async def metadata_get(article_id: int, stage: bool = False):
    response = figshare_get(article_id, stage=stage)
    readme_dict = figshare_metadata_readme(response)
    return readme_dict
