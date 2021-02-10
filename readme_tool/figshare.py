import requests

from fastapi import FastAPI
# from pydantic import BaseModel

api_version = 'v1'

app = FastAPI()


def figshare_metadata_readme(figshare_dict: dict) -> dict:
    """
    Function to provide shortened dict for README metadata

    :param figshare_dict: Figshare API response

    :return: README metadata based on Figshare response
    """

    readme_dict = {
        'title': figshare_dict['title'],
        'description': figshare_dict['description'],
        'doi': figshare_dict['doi']
    }
    return readme_dict


@app.get(f'/api/{api_version}/figshare/'+'{article_id}')
def figshare_get(article_id: int, stage: bool = False) -> dict:
    """
    API call to retrieve Figshare metadata

    :param article_id: Figshare article ID
    :param stage: Figshare stage or production API.
                  Stage is available for Figshare institutions

    :return: Figshare API response
    """

    if not stage:
        base_url = "https://api.figshare.com"
    else:
        base_url = "https://api.figsh.com"

    url = f"{base_url}/v2/articles/{article_id}"

    response = requests.get(url)
    return response.json()


@app.get(f'/api/{api_version}/metadata/'+'{article_id}')
async def metadata_get(article_id: int, stage: bool = False) -> dict:
    """
    API call for README metadata based on Figshare response

    :param article_id: Figshare article ID
    :param stage: Figshare stage or production API.
                  Stage is available for Figshare institutions

    :return: README metadata API response
    """
    response = figshare_get(article_id, stage=stage)
    readme_dict = figshare_metadata_readme(response)
    return readme_dict