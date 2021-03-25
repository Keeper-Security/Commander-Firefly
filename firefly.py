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
import base64
import logging
import os
import tempfile

import json
from keepercommander.params import KeeperParams
from keepercommander import api
from keepercommander.plugins import azureadpwd

from azureadpwdplugin import AZADRotator

logger = logging.getLogger()

az_ad_admin_record_uid = '9TKCRisBexRYGdFcLmzC7g'

class Firefly:

    @staticmethod
    def create_config_file_and_get_params(params):
        # type: (KeeperParams) -> None

        private_key = "Pgfd273WVndjXSWqk7XRtmixr8_bk3gnJHf4Db4mO2k"
        device_token = "DJgM5LOATjER-CFOZBjRFFmPk4OGIPTdfFCt2VuWSqeUDQ"
        user = "mustinov+firefly-sa@keeperdemo.io"
        password = "Pa$$word123"

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
    def rotate_all_az_ad_users(params):

        az_ad_user1_record_uid = '50cLhCRC-jK8YZY6EInRJQ'
        az_ad_user2_record_uid = 'OPU-UzB2NubF8jFPduFVZw'

        is_verified_user1 = Firefly.rotate_az_ad_acct(params, az_ad_admin_record_uid, az_ad_user1_record_uid)
        is_verified_user2 = Firefly.rotate_az_ad_acct(params, az_ad_admin_record_uid, az_ad_user2_record_uid)

        return {
            az_ad_user1_record_uid: is_verified_user1,
            az_ad_user2_record_uid: is_verified_user2
        }

    @staticmethod
    def rotate_single_az_ad_user(params, az_ad_user_record_uid):

        is_verified = Firefly.rotate_az_ad_acct(params, az_ad_admin_record_uid, az_ad_user_record_uid)

        return {
            az_ad_user_record_uid: is_verified
        }