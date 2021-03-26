import logging
from flask import Flask
from flask import request, jsonify
from keepercommander.params import KeeperParams
from logging import StreamHandler
from firefly import Firefly

app = Flask(__name__)
# app.config["DEBUG"] = True
logging.basicConfig(level=logging.DEBUG)
streamHandler = StreamHandler()
app.logger.addHandler(streamHandler)


# Login to Keeper (once)
params = KeeperParams()
Firefly.login(params)


@app.route("/")
def default():
    return """
    
    🐛 Firefly! 🦋
    
    <a href=/api/v1/firefly/rotate>Rote all</a>
    <a href=/api/v1/firefly/rotate?uid=50cLhCRC-jK8YZY6EInRJQ>Rote One</a>

    
    """


@app.route('/api/v1/firefly/rotate', methods=['GET'])
def api_rotate():

    query_parameters = request.args

    record_uid = query_parameters.get('uid')

    if record_uid:
        app.logger.info('Processing single record [%s] rotation' % record_uid)
        resp = Firefly.rotate_single_az_ad_user(params, record_uid)
    else:
        app.logger.info('Processing ALL records rotation')
        resp = Firefly.rotate_all_az_ad_users(params)

    return jsonify(resp)


# app.run()
