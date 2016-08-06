FROM ubuntu:14.04
MAINTAINER Toan Nai "toanvnu@gmail.comm"
RUN apt-get clean
RUN apt-get update -y
RUN apt-get install -y tar curl wget  build-essential
RUN apt-get install -y \
    python \
    python-dev \
    python-distribute \
    python-pip \
    python-setuptools \
    libmysqlclient-dev \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev 

COPY ./ldap /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["/usr/bin/python"]
CMD ["run.py"]
