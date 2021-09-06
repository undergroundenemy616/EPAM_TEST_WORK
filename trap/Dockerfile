FROM python:3.9.6-slim-buster

WORKDIR /project
COPY requirements/ requirements/
RUN pip install -r requirements/dev.txt
COPY . .
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["/project/docker-entrypoint.sh"]
