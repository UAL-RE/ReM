from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import Union

from tinydb import TinyDB, Query

from . import __version__ as rem_version
from . import figshare

api_version = "v1.0.0"
readme_url_path = '/readme_tool/'
tinydb_file = 'intake.json'

app = FastAPI()
templates = Jinja2Templates(directory='templates/')

q = Query()  # For TinyDB query


class IntakeData(BaseModel):
    article_id: int
    summary: str = ''
    files: str = ''


class VersionModel(BaseModel):
    rem_api_version: str = rem_version
    rem_web_api_version: str = api_version


@app.get('/version/')
async def get_version() -> VersionModel:
    """Retrieve version metadata"""
    return VersionModel()


@app.get(readme_url_path + 'database/')
async def get_db(db_file: str = tinydb_file) -> TinyDB:
    """Retrieve TinyDB README database

    \f
    :param db_file: JSON filename for TinyDB database

    :return: README database
    """
    db = TinyDB(db_file)
    return db


@app.get(readme_url_path + 'database/read/{article_id}')
async def get_data(article_id: int, index: bool = False,
                   db_file: str = tinydb_file) -> Union[dict, int]:
    """Retrieve record from TinyDB README database

    \f
    :param article_id: Figshare article ID
    :param index: Indicate whether to return ``doc_id`` (True) or record (False).
    :param db_file: JSON filename for TinyDB database

    :return: TinyDB record or ``doc_id``
    """
    db0 = await get_db(db_file=db_file)
    article_query = q['article_id'] == article_id
    match = db0.search(article_query)
    if len(match) == 0:
        raise HTTPException(
            status_code=404,
            detail="Record not found",
        )

    if not index:
        return match[0]
    else:
        return db0.get(article_query).doc_id


@app.post(readme_url_path + 'database/create')
async def add_data(response: IntakeData, db_file: str = tinydb_file):
    """
    Add record to TinyDB README database

    \f
    :param response: Record to include
    :param db_file: JSON filename for TinyDB database
    """
    db0 = await get_db(db_file)
    db0.insert(response.dict())


@app.post(readme_url_path + 'database/update/{doc_id}')
async def update_data(doc_id: int, response: IntakeData,
                      db_file: str = tinydb_file):
    """
    Update record in TinyDB README database

    \f
    :param doc_id: ``doc_id`` identifier from ``get_data`` to update
    :param response: Record to use for update
    :param db_file: JSON filename for TinyDB database

    :return: README database
    """
    db0 = await get_db(db_file)
    db0.update(response.dict(), doc_ids=[doc_id])
    return db0


@app.get(readme_url_path + 'form/read/{article_id}')
async def read_form(article_id: int, request: Request, stage: bool = False,
                    db_file: str = tinydb_file) \
        -> templates.TemplateResponse:
    """
    Return README form with Figshare metadata and README metadata if available

    \f
    :param article_id: Figshare `article_id`
    :param request: HTTP request for template
    :param stage: Figshare stage or production API.
                  Stage is only available for Figshare institutions
    :param db_file: JSON filename for TinyDB database

    :return: HTML content through ``jinja2`` template
    """
    fs_metadata = await figshare.metadata_get(article_id, stage=stage)

    try:
        submit_dict = await get_data(article_id, db_file=db_file)
    except HTTPException:
        submit_dict = {'summary': '', 'files': ''}

    result = {'summary': 'Provide additional summary info',
              'files': 'Provide your files'}

    return templates.TemplateResponse('intake.html',
                                      context={'request': request,
                                               'result': result,
                                               'submit_dict': submit_dict,
                                               'fs': fs_metadata})


@app.post(readme_url_path + 'form/submit/{article_id}')
async def intake_post(article_id: int, request: Request,
                      summary: str = Form(...), files: str = Form(...),
                      stage: bool = False, db_file: str = tinydb_file) \
        -> templates.TemplateResponse:
    """
    Submit data to incorporate in TinyDB database

    :param article_id: Figshare `article_id`
    :param request: HTTP request
    :param summary: Form response for summary data
    :param files: Form response for files data
    :param stage: Figshare stage or production API.
                  Stage is only available for Figshare institutions
    :param db_file: JSON filename for TinyDB database
    :return: HTML content through ``jinja2`` template
    """
    fs_metadata = await figshare.metadata_get(article_id, stage=stage)
    result = {'summary': summary,
              'files': files}

    post_data = {'article_id': fs_metadata['article_id'], **result}

    try:
        doc_id = await get_data(article_id, index=True, db_file=db_file)
        await update_data(doc_id, IntakeData(**post_data), db_file=db_file)
    except HTTPException:
        await add_data(IntakeData(**post_data), db_file=db_file)

    return templates.TemplateResponse('intake.html',
                                      context={'request': request,
                                               'result': result,
                                               'submit_dict': result,
                                               'fs': fs_metadata,
                                               }
                                      )
