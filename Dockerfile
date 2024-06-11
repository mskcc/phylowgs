FROM python:2.7

LABEL maintainer="Nikhil Kumar (kumarn1@mskcc.org)" \
      version.phylowgs="v1.5-msk" \
      version.python="2.7" \
      source.phylowgs="https://github.com/mskcc/phylowgs"

ENV PHYLOWGS_TAG="v1.5-msk"

RUN apt-get update \
  && apt-get install -y git make build-essential libgsl-dev \
  && cd /tmp \
  && git clone --branch 1.5 https://github.com/mskcc/phylowgs \
  && cd phylowgs \
  && pip2 install -r requirements.txt  \
  && g++ -o mh.o -O3 mh.cpp  util.cpp `gsl-config --cflags --libs` \
  && cp -r . /usr/bin \
  && rm -r /tmp/phylowgs
