FROM odoo:15
# Copy entrypoint script and Odoo configuration file
USER root

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libxmlsec1-dev \
    libxml2-dev \
    libxslt1-dev \
    libxml2 \
    libxmlsec1 \
    python3-dev \
    python3-setuptools \
    python3-cryptography \
    python3-wheel \
    python3-pip \
    pkg-config \
    build-essential \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev

COPY ./extra-addons /usr/lib/python3/dist-packages/odoo/extra-addons

WORKDIR /usr/lib/python3/dist-packages/odoo/extra-addons

RUN pip3 install --upgrade pip wheel setuptools \
    && pip3 install -r ./pip-requirements.txt

# RUN pip3 install cryptography pyopenssl urllib3 --upgrade
RUN pip3 install /usr/lib/python3/dist-packages/odoo/extra-addons/PyTrustNFe

COPY ./odoo.conf /etc/odoo/