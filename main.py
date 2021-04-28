#!/usr/bin/env python

import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from readme_tool import figshare, intake_form

app = FastAPI()


def configure():
    app.mount("/templates", StaticFiles(directory="templates"), name="templates")
    configure_routing()


def configure_routing():
    app.include_router(figshare.router)
    app.include_router(intake_form.router)


if __name__ == "__main__":
    configure()
    uvicorn.run('main:app', port=8000, reload=True)
else:
    configure()
