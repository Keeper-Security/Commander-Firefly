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
import os
import tempfile

import json
from keepercommander.params import KeeperParams
from keepercommander import api

from azureadpwdplugin import AZADRotator

logger = logging.getLogger()


private_key = os.getenv('KEEPER_CONFIG_PRIVATE_KEY')
device_token = os.getenv('KEEPER_CONFIG_DEVICE_TOKEN')
user = os.getenv('KEEPER_USER_EMAIL')
password = os.getenv('KEEPER_USER_PASSWORD')


# TODO: replace UID with using searching by Tags (custom fields)
# az_ad_admin_record_uid = os.getenv('KEEPER_AZAD_ADM_RECORD_UID')


print("KEEPER_CONFIG_PRIVATE_KEY=[%s]" % len(private_key))
print("KEEPER_CONFIG_DEVICE_TOKEN=[%s]" % len(device_token))
print("KEEPER_USER_EMAIL=[%s]" % len(user))
print("KEEPER_USER_PASSWORD=[%s]" % len(password))
# print("KEEPER_AZAD_ADM_RECORD_UID=[%s]" % len(az_ad_admin_record_uid))

class Firefly:

    @staticmethod
    def create_config_file_and_get_params(params):
        # type: (KeeperParams) -> None

        # create a temporary file
        firefly_temp_file = tempfile.NamedTemporaryFile(prefix="commander-config-", suffix=".json", delete=False)

        json_dict = {
            'private_key': private_key,
            'device_token': device_token,
            'user': user,
            'password': password
        }

        str_json = json.dumps(json_dict)

        print(str_json)

        config_file = open(firefly_temp_file.name, "w")
        config_file.write(str_json)
        config_file.close()

        params.config_filename = config_file.name

        with open(params.config_filename, 'r') as f:
            params.config = json.load(f)
            params.server = params.config['server'] if 'server' in params.config else "https://keepersecurity.com"
            params.user = params.config['user']
            params.password = params.config['password']

    @staticmethod
    def login(params):

        # Inputs - hard coded for demo purposes
        Firefly.create_config_file_and_get_params(params)

        api.login(params)

        api.sync_down(params)

        return params

    @staticmethod
    def get_all_records(params):

        logging.info('Getting all records...')

        all_recs = api.search_records(params, '')

        logging.info('Got %s record(s)' % len(all_recs))

        return all_recs

    @staticmethod
    def get_all_by_custom_field(params, cf_title, cf_values):

        records = Firefly.get_all_records(params)

        all_tagged_and_rotatable = []

        for r in records:
            for cf in r.custom_fields:
                if cf_title == cf['name']:
                    if cf['value'] == cf_values:
                        all_tagged_and_rotatable.append(r)

        return all_tagged_and_rotatable

    @staticmethod
    def to_json_str(obj):
        def obj_dict(obj):
            return obj.__dict__

        json_string = json.dumps(obj, default=obj_dict)

        logging.info(json_string)

        return json_string

    @staticmethod
    def rotate_az_ad_acct(params, uid_of_az_ad_admin_record, uid_of_record_to_rotate):

        # 1. Get AZ AD Admin user Record

        az_ad_admin_record = api.get_record(params, uid_of_az_ad_admin_record)

        print(az_ad_admin_record)

        # 2. Rotate password

        #   A. Find record to be rotated
        record_to_rotate = api.get_record(params, uid_of_record_to_rotate)

        print('PWD Before: %s' % record_to_rotate.password)

        AZADRotator.rotate(az_ad_admin_record, record_to_rotate)

        print('PWD After : %s' % record_to_rotate.password)

        params.sync_data = True

        api.update_record(params, record_to_rotate)

        return True

    @staticmethod
    def rotate_all_az_ad_users(params, az_admin_record, records):

        resp_dict = []

        for r in records:
            record_uid = r.record_uid

            is_rotated = Firefly.rotate_az_ad_acct(params, az_admin_record.record_uid, record_uid)

            resp_dict.append(
                {
                    'record_uid': r.record_uid,
                    'status': is_rotated
                }
            )

        return resp_dict

    @staticmethod
    def rotate_single_az_ad_user(params, az_admin_record,  az_ad_user_record_uid):

        is_verified = Firefly.rotate_az_ad_acct(params, az_admin_record.record_uid, az_ad_user_record_uid)

        return {
            az_ad_user_record_uid: is_verified
        }
