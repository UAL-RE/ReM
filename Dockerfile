# Using base image provided by nginx unit
FROM nginx/unit:1.22.0-python3.9
# Alternatively you can use different tags from https://hub.docker.com/r/nginx/unit

WORKDIR /rem

COPY main.py /rem/main.py
COPY templates /rem/templates
COPY README.md /rem/README.md
COPY requirements.txt /rem/requirements.txt
COPY readme_tool /rem/readme_tool
COPY setup.py /rem/setup.py
COPY nginx_config.json /docker-entrypoint.d/config.json
COPY . /rem
RUN chmod 775 intake.json
RUN python setup.py develop
