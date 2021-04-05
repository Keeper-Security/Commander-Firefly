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

import json
import logging

import requests

from rotators.helpers import pwd_generator, az_get_access_token


class AZADRotator:

    @staticmethod
    def rotate(az_ad_admin_record, rotate_record):
        """
        @type az_ad_admin_record: Record
        @type rotate_record: Record
        """

        tenant_id = az_ad_admin_record.get("cmdr:azure_tenant_id")
        client_id = az_ad_admin_record.get("cmdr:azure_client_id")
        secret = az_ad_admin_record.get("cmdr:azure_secret")

        users_endpoint = 'https://graph.microsoft.com/v1.0/users'
        default_scope = 'https://graph.microsoft.com/.default'

        azure_ac_user_email = rotate_record.login   # The Azure user_id either as the object ID (GUID) or the user principal name (UPN) of the target user
        new_password = pwd_generator()

        try:

            access_token = az_get_access_token(client_id, tenant_id, secret, [default_scope])

            # 1. Getting all users from Azure Graph using the access token
            # all_users = requests.get(  # Use token to call downstream service
            #     users_endpoint,
            #     headers={'Authorization': 'Bearer ' + access_token}
            # ).json()
            #
            # 2. Getting only one user
            # usr = requests.get(
            #     '%s/%s' % (users_endpoint, user_id),
            #     headers={'Authorization': 'Bearer ' + access_token}
            # ).json()

            # 3. Updating user's password
            pwd_change_payload = {
                'passwordProfile': {
                    'password': new_password,
                    'forceChangePasswordNextSignIn': False
                }
            }

            usr_pwd_update_resp = requests.patch(
                '%s/%s' % (users_endpoint, azure_ac_user_email),
                headers={
                    'Authorization': 'Bearer ' + access_token,
                    'Content-Type': 'application/json'
                },
                data=json.dumps(pwd_change_payload)
            )

            resp_status_code = usr_pwd_update_resp.status_code

            if resp_status_code == 204:
                logging.info("Password successfully changed in Azure")

                rotate_record.password = new_password

                return True

            elif resp_status_code == 403:
                resp_data = usr_pwd_update_resp.json()

                if resp_data['error']['code'] == 'Authorization_RequestDenied':
                    logging.error("Status code: %d, message: %s" % (resp_status_code, resp_data['error']['message']))
                    logging.error("Insufficient privileges to perform the password reset")
                    logging.error('\tIf you have access to Azure with administrator permission then you can enable\n'
                                  '\tpermission by navigating to Azure Portal -> Azure AD -> Roles and administrators ->\n'
                                  '\t"Helpdesk Administrator" -> Click on "Add Assignments" > select the application with client\n'
                                  '\tid "%s" > click on Add button.' % client_id)
                else:
                    logging.error("Unknown status code: %d, message: %s" % (resp_status_code, resp_data['error']['message']))
            else:
                logging.error("Unhandled status code: %d, message: %s" % (resp_status_code, usr_pwd_update_resp.json()['error']['message']))

        except Exception as ex:
            logging.error(ex)

        return False
