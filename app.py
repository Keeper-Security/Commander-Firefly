import logging
from flask import Flask
from flask import request, jsonify
from keepercommander.params import KeeperParams
from logging import StreamHandler
from firefly import Firefly

app = Flask(__name__)
app.config["DEBUG"] = True
logging.basicConfig(level=logging.DEBUG)
streamHandler = StreamHandler()
app.logger.addHandler(streamHandler)


# Login to Keeper (once)
params = KeeperParams()
Firefly.login(params)


@app.route("/")
def default():
    return """
    
    🐛 Firefly! <img src="https://www.flaticon.com/svg/vstatic/svg/878/878036.svg?token=exp=1617043390~hmac=a41911213c845e51dd9d77925ec3517e" alt="Firefly Icon" width="20" height="20">
    
    <br/>
    <br/>
    <a href=/api/v1/firefly/rotate>Rote all</a> <br/>
    <a href=/api/v1/firefly/rotate?uid=50cLhCRC-jK8YZY6EInRJQ>Rote One</a>
    
    """


@app.route('/api/v1/firefly/rotate', methods=['GET'])
def api_rotate():

    query_parameters = request.args

    record_uid = query_parameters.get('uid')

    az_admin_record = Firefly.get_all_by_custom_field(params, 'tag', "azure app registration")[0]

    if record_uid:
        app.logger.info('Processing single record [%s] rotation' % record_uid)
        resp = Firefly.rotate_single_az_ad_user(params, az_admin_record, record_uid)

    else:
        # Rotate all tagged as `azure`, `active directory`, `rotatable`
        app.logger.info('Processing ALL records rotation')
        all_rotatable_records = Firefly.get_all_by_custom_field(params, 'tag', 'azure ad rotatable')
        resp = Firefly.rotate_all_az_ad_users(params, az_admin_record, all_rotatable_records)

    return jsonify(resp)


app.run()
