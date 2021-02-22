from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

from . import figshare

app = FastAPI()
templates = Jinja2Templates(directory='templates/')


@app.get('/')
async def hello_world():
    return 'hello world'


@app.get('/api/v1/intake/{article_id}')
async def read_form(article_id: int, request: Request, stage: bool = False):
    fs_metadata = await figshare.metadata_get(article_id, stage=stage)

    result = {'summary': 'Provide additional summary info',
              'files': 'Provide your files'}

    return templates.TemplateResponse('intake.html',
                                      context={'request': request,
                                               'result': result,
                                               'fs': fs_metadata})


@app.post('/api/v1/intake/{article_id}')
async def intake_post(article_id: int, request: Request,
                      summary: str = Form(...), files: str = Form(...),
                      stage: bool = False):
    fs_metadata = await figshare.metadata_get(article_id, stage=stage)

    result = {'summary': summary,
              'files': files}

    return templates.TemplateResponse('intake.html',
                                      context={'request': request,
                                               'result': result,
                                               'fs': fs_metadata
                                               }
                                      )
