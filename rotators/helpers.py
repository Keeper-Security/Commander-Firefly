# -*- coding: utf-8 -*-
#  _  __
# | |/ /___ ___ _ __  ___ _ _ ®
# | ' </ -_) -_) '_ \/ -_) '_|
# |_|\_\___\___| .__/\___|_|
#              |_|
#
# Keeper Commander
# Copyright 2021 Keeper Security Inc.
# Contact: ops@keepersecurity.com
#

import logging
import time
import msal     # pip install msal


def az_get_access_token(client_id, tenant_id, secret, scopes):

    authority = 'https://login.microsoftonline.com/%s' % tenant_id

    # Create a preferably long-lived app instance which maintains a token cache.
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=secret,
        # token_cache=...  # Default cache is in memory only.
        # To learn how to use SerializableTokenCache from
        #   https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
    )

    # Get access token
    result = app.acquire_token_silent(scopes=scopes, account=None)

    if not result:
        logging.debug("No suitable token exists in cache. Let's get a new one from AAD.")
        result = app.acquire_token_for_client(scopes=scopes)

    if 'access_token' not in result:
        logging.error('Azure error: %s, description: %s' % (result['error'], result['error_description']))
        raise Exception

    access_token = result['access_token'] # JWT access token

    return access_token


def pwd_generator():
    epoch_time = int(time.time())
    new_password = 'NEwPa$$Word-%s' % epoch_time
    return new_password
