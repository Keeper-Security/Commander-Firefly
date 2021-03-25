import logging

import json
import azure.functions as func
from keepercommander.params import KeeperParams
from firefly import Firefly

logger = logging.getLogger()



def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    az_ad_user_record_uid = req.params.get('az_ad_user_record_uid')

    params = KeeperParams()
    Firefly.login(params)

    if not az_ad_user_record_uid:
        resp = Firefly.rotate_all_az_ad_users(params)
    else:
        resp = Firefly.rotate_single_az_ad_user(params, az_ad_user_record_uid)

    # all_records = Firefly.get_all_records(params)
    json_str = Firefly.to_json_str(resp)

    return func.HttpResponse(
        json_str,
        mimetype="application/json"
    )











    # name = req.params.get('name')
    #
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')
    #
    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
