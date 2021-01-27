# Pull base image
FROM python:3.6-slim

# Set environment varibles
ENV PYTHONUNBUFFERED=1 PYTHONPATH=/scripts/ DOCKER=1 DEBIAN_FRONTEND=noninteractive

# Add support for apt-* packages caching through "apt-cacher-ng"
ARG APTPROXY
RUN bash -c 'if [ -n "$APTPROXY" ]; then echo "Acquire::HTTP::Proxy \"http://$APTPROXY\";" > /etc/apt/apt.conf.d/01proxy; fi'

# Install dependencies
RUN apt-get update \
    # Python system packages
    && apt-get --no-install-recommends install -y \
      python \
      python-pip \
      python-dev \
      libsasl2-dev \
      libssl-dev \
      # More System stuff
      nginx-extras \
      gcc \
      dos2unix

# Cleaning installation
RUN apt-get clean -y \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -fr /var/lib/apt/lists/* \
    # Creating working dir
    && mkdir -p /scripts/

# Set work directory
WORKDIR /scripts/

# Gets and install required pachages
ADD requirements.txt requirements.txt
RUN pip install -U pip \
    && pip install -r requirements.txt --no-cache-dir

ADD ../.. /scripts/

CMD ["python", "version"]