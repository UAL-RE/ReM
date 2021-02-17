#!/usr/bin/env python

import uvicorn

from readme_tool.figshare import app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
