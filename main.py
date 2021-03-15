#!/usr/bin/env python

import uvicorn

import readme_tool

if __name__ == "__main__":
    uvicorn.run("readme_tool.intake_form:app", port=8000, reload=True)
