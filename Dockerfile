FROM ubuntu:20.04

# Labels
LABEL org.opencontainers.image.vendor="MSKCC-OMICS-WORKFLOWS" \
      org.opencontainers.image.authors="Nikhil Kumar (kumarn1@mskcc.org), John Orgera (orgeraj@mskcc.org)" \
      org.opencontainers.image.created="2025-08-21T11:07:00Z" \
      imageprivacy="False" \
      org.opencontainers.image.licenses="GPL-3.0" \
      org.opencontainers.image.version="1.5.2-msk" \
      org.opencontainers.image.source="https://github.com/mskcc/phylowgs" \
      org.opencontainers.image.url="https://github.com/mskcc-omics-workflows/containers/containers/phylowgs/" \
      org.opencontainers.image.title="Phylowgs" \
      org.opencontainers.image.description="Application for inferring subclonal composition and evolution from whole-genome sequencing data."

ENV DEBIAN_FRONTEND=noninteractive
ENV PHYLOWGS_TAG="v1.5.2-msk"
ARG TARGETPLATFORM

RUN apt-get update -y \
      # Install packages
      && apt-get install -y --no-install-recommends python2 python2-dev git curl ca-certificates libblas-dev liblapack-dev gfortran make build-essential libgsl-dev \
      # Setup python
      && curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output /tmp/get-pip.py \
      && python2 /tmp/get-pip.py \
      # Install phylowgs
      && git clone --branch 1.5.2 https://github.com/mskcc/phylowgs /tmp/phylowgs \
      && pip2 install --no-cache-dir -r /tmp/phylowgs/requirements.txt  \
      && cp -r /tmp/phylowgs/ /usr/bin \
      && g++ -I/usr/bin/phylowgs -o /usr/bin/phylowgs/mh.o -O3 /usr/bin/phylowgs/mh.cpp  /usr/bin/phylowgs/util.cpp -I/usr/include -L/usr/lib/aarch64-linux-gnu -lgsl -lgslcblas -lm \
      && chmod -R +x /usr/bin/phylowgs \
      # Clean up
      && rm -r /tmp/phylowgs \
      && apt-get clean \
      && apt-get purge \
      && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
ENV PATH=/usr/bin/phylowgs/parser/:/usr/bin/phylowgs:$PATH