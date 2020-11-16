FROM python:3.7

RUN mkdir          /fea-app
COPY ./*           /fea-app/
COPY entrypoint.sh /entrypoint.sh

RUN cd /fea-app \
  && apt-get -y update \
  && apt-get -y install -y dumb-init libc-dev build-essential libatlas-base-dev gfortran\
  && pip install --upgrade --no-cache-dir pip wheel setuptools \
  && pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT [ "/usr/bin/dumb-init", "--" ]
CMD        [ "/entrypoint.sh" ]
