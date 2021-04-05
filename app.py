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

    az_admin_record = Firefly.get_all_by_custom_field(params, 'tag', "azure app registration")[0]

    return """
        <html>
            <head>
                    
            </head>
            
            <body>
                <h1>🐛 Firefly! <img src="https://raw.githubusercontent.com/Keeper-Security/Commander-Firefly/main/docs/878036.svg" alt="Firefly Icon" width="40" height="40"></h1>
                
                <br/>
                <h3>Admin Keeper Record</h3><br />
                <blockquote>UID: <strong>%s</strong></blockquote>
                <blockquote>Title: <strong>%s</strong></blockquote><br />
                <hr/>
                <br/>
                <br/>
                <a href=/api/v1/firefly/rotate/az/ad>Rotate all Azure Active Directory Records</a> <br/>
                <a href=/api/v1/firefly/rotate/az/ad?uid=50cLhCRC-jK8YZY6EInRJQ>Rotate One Azure Active Directory Records</a><br/>
                <br/>
                <br/>
                <a href=/api/v1/firefly/rotate/az/vm>Rotate all Azure VM Local Admin Passwords</a> <br/>
                <a href=/api/v1/firefly/rotate/az/vm?uid=MojUDKMzMQ1J-jCQfap5sw>Rotate One Azure VM Local Admin Password</a><br/>
            </body>
        </html>
        
    """ % (az_admin_record.record_uid, az_admin_record.title)


@app.route('/api/v1/firefly/rotate/az/ad', methods=['GET'])
def api_az_ad_rotate():

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


@app.route('/api/v1/firefly/rotate/az/vm', methods=['GET'])
def api_az_vm_rotate():

    query_parameters = request.args

    record_uid = query_parameters.get('uid')

    az_admin_record = Firefly.get_all_by_custom_field(params, 'tag', "azure app registration")[0]

    if record_uid:
        app.logger.info('Processing single record [%s] rotation' % record_uid)
        resp = Firefly.rotate_single_az_vm(params, az_admin_record, record_uid)

    else:
        # Rotate all tagged as `azure`, `active directory`, `rotatable`
        app.logger.info('Processing ALL records rotation')
        all_rotatable_records = Firefly.get_all_by_custom_field(params, 'tag', 'azure vm rotatable')
        resp = Firefly.rotate_all_az_vms(params, az_admin_record, all_rotatable_records)

    return jsonify(resp)


if __name__ == '__main__':
    app.run()
