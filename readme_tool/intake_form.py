from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import Union

from tinydb import TinyDB, Query

from . import figshare

app = FastAPI()
templates = Jinja2Templates(directory='templates/')

q = Query()


class IntakeData(BaseModel):
    article_id: int
    summary: str = ''
    files: str = ''


@app.get('/')
async def hello_world() -> str:
    return 'hello world'


@app.get('/api/v1/intake/database/')
async def get_db(db_file: str = 'intake.json') -> TinyDB:
    db = TinyDB(db_file)
    return db


@app.get('/api/v1/intake/database/{article_id}')
async def get_data(article_id: int, index: bool = False,
                   db_file: str = 'intake.json') -> Union[dict, int]:
    print(db_file)
    db0 = await get_db(db_file=db_file)
    print(db0)
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


@app.post('/api/v1/intake/database/add')
async def add_data(response: IntakeData, db_file: str = 'intake.json'):
    db0 = await get_db(db_file)
    db0.insert(response.dict())


@app.post('/api/v1/intake/database/update/{doc_id}')
async def update_data(doc_id: int, response: IntakeData,
                      db_file: str = 'intake.json'):
    db0 = await get_db(db_file)
    db0.update(response.dict(), doc_ids=[doc_id])
    return db0


@app.get('/api/v1/intake/{article_id}')
async def read_form(article_id: int, request: Request, stage: bool = False,
                    db_file: str = 'intake.json'):
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


@app.post('/api/v1/intake/{article_id}')
async def intake_post(article_id: int, request: Request,
                      summary: str = Form(...), files: str = Form(...),
                      stage: bool = False):
    fs_metadata = await figshare.metadata_get(article_id, stage=stage)

    '''
    try:
        submit_dict = await get_data(article_id)
    except HTTPException:
        submit_dict = {'summary': '', 'files': ''}
    '''

    result = {'summary': summary,
              'files': files}

    post_data = {'article_id': fs_metadata['article_id'], **result}

    try:
        doc_id = await get_data(article_id, index=True)
        await update_data(doc_id, IntakeData(**post_data))
    except HTTPException:
        await add_data(IntakeData(**post_data))

    return templates.TemplateResponse('intake.html',
                                      context={'request': request,
                                               'result': result,
                                               'submit_dict': result,
                                               'fs': fs_metadata,
                                               }
                                      )
