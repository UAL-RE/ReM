#!/usr/bin/env python

import uvicorn

from readme_tool.intake_form import app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
