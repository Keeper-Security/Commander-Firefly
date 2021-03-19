#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
apt-get -y update

# install Python
apt-get -y install python3-setuptools python3-pip

# Install dependencies
python3 -m pip install \
    --no-binary lxml \
    pip \
    setuptools \
    wheel \
    lxml \
    libkeepass==0.2.0 \
    lastpass-python \
    pymssql \
    fido2 \
    ldap3 \
    awscli \
    msal \
    keepass

# install Keeper Commander
python3 -m pip install keepercommander