from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel
from typing import Union

from . import figshare

app = FastAPI()
templates = Jinja2Templates(directory='templates/')

db = []


class IntakeData(BaseModel):
    article_id: int
    summary: str = ''
    files: str = ''


@app.get('/')
async def hello_world() -> str:
    return 'hello world'


@app.get('/api/v1/intake/database/')
async def get_db() -> list:
    return db


@app.get('/api/v1/intake/database/{article_id}')
async def get_data(article_id: int, index: bool = False) -> Union[dict, int]:
    db0 = await get_db()

    match_idx = [i for i in range(len(db0)) if db0[i].dict()['article_id'] == article_id]
    if len(match_idx) == 0:
        raise HTTPException(
            status_code=404,
            detail="Record not found",
        )
    else:
        match = [db0[i] for i in match_idx]

    if not index:
        return match[0]
    else:
        return match_idx[0]


@app.get('/api/v1/intake/{article_id}')
async def read_form(article_id: int, request: Request, stage: bool = False):
    fs_metadata = await figshare.metadata_get(article_id, stage=stage)

    try:
        submit_dict = await get_data(article_id)
    except HTTPException:
        submit_dict = {'summary': '', 'files': ''}
    print(submit_dict)

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
        match_index = await get_data(article_id, index=True)
        db[match_index] = IntakeData(**post_data)
    except HTTPException:
        db.append(IntakeData(**post_data))

    return templates.TemplateResponse('intake.html',
                                      context={'request': request,
                                               'result': result,
                                               'submit_dict': result,
                                               'fs': fs_metadata,
                                               }
                                      )