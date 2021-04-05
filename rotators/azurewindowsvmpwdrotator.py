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

from rotators.helpers import az_get_access_token, pwd_generator


class AzureWindowsVMPwdRotator:

    @staticmethod
    def rotate(az_ad_admin_record, rotate_record):

        """
        @type az_ad_admin_record: Record
        @type rotate_record: Record
        """

        tenant_id = az_ad_admin_record.get("cmdr:azure_tenant_id")
        client_id = az_ad_admin_record.get("cmdr:azure_client_id")
        secret = az_ad_admin_record.get("cmdr:azure_secret")

        # tenant_id = 'fbf38e29-d16d-485e-9873-df686b048694'
        # client_id = '1ab34aa4-b306-4960-ae7f-3b1dce4502c8'
        # app_secret = 'fjo3XlGS6-K_SHzmV6g2g-fHNrX~1Y6q._'

        default_scope = 'https://management.azure.com/.default'

        # subscriptionId = "fc486557-0d15-4acc-b9b9-4498ed9ee90f"
        subscriptionId = rotate_record.get("az:subscription_id")

        # resourceGroupName = "mustinov-firefly-poc-pwd-rotation_group"
        resourceGroupName = rotate_record.get("az:resource_group_name")

        # vmName = "mustinov-firefly-poc-pwd-rotation"
        vmName = rotate_record.get("az:vm_name")


        # local_admin_user_name = "mustinov"
        local_admin_user_name = rotate_record.login

        local_admin_new_password = pwd_generator()

        try:

            access_token = az_get_access_token(client_id, tenant_id, secret, [default_scope])

            vm_pwd_change_payload = {
                'properties': {
                    'publisher': 'Microsoft.Compute',
                    'type': 'VMAccessAgent',
                    'typeHandlerVersion': '2.0',
                    'autoUpgradeMinorVersion': True,
                    'settings': {
                        'UserName': local_admin_user_name
                    },
                    'protectedSettings': {
                        'Password': local_admin_new_password
                    }
                },
                'location': "westus"
            }

            print(json.dumps(vm_pwd_change_payload))

            vm_pwd_update_change_resp = requests.put(
                'https://management.azure.com/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Compute/virtualMachines/%s/extensions/enablevmaccess?api-version=2020-12-01' % (subscriptionId, resourceGroupName, vmName),
                headers={
                    'Authorization': 'Bearer ' + access_token,
                    'Content-Type': 'application/json'
                },

                data=json.dumps(vm_pwd_change_payload)
            )

            if vm_pwd_update_change_resp.ok:
                print("CHANGED!!!!!!")

                rotate_record.password = local_admin_new_password

                return True
            else:
                print("Reason: %s" % vm_pwd_update_change_resp.reason)
                print("\t%s" % vm_pwd_update_change_resp.text)

        except Exception as ex:
            logging.error(ex)

        return False


if __name__ == '__main__':
    AzureWindowsVMPwdRotator.rotate(None, None)

