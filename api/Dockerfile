FROM python:3.7.2
ENV PYTHONUNBUFFERED 1
RUN mkdir /api
WORKDIR /api
COPY requirements.txt /api/
RUN pip install -r requirements.txt
COPY . /api/

RUN useradd -ms /bin/bash uwsgi
USER uwsgi
WORKDIR /api

CMD ["sh", "entrypoint.sh"]