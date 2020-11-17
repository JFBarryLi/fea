FROM python:3.7

RUN mkdir           /fea-app
COPY ./             /fea-app/
COPY entrypoint.sh  /entrypoint.sh

ENV PIP_CONFIG_FILE pip.conf

RUN cd /fea-app \
  && apt-get -y update \
  && apt-get -y install -y dumb-init libatlas-base-dev\
  && pip install --no-cache-dir -r requirements.txt

EXPOSE 5900

ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]
CMD        [ "/entrypoint.sh" ]
