import logging
from flask import Flask
from flask import request, jsonify, redirect
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

    Firefly.sync_down(params)

    az_admin_record = Firefly.get_all_by_custom_field(params, 'tag', "azure app registration")[0]

    all_ad_rotatable_records = Firefly.get_all_by_custom_field(params, 'tag', 'azure ad rotatable')
    all_vm_rotatable_records = Firefly.get_all_by_custom_field(params, 'tag', 'azure vm rotatable')

    ad_rec_to_rotate = all_ad_rotatable_records[0] if len(all_ad_rotatable_records) > 0 else "NO_RECORDS_AD"
    vm_rec_to_rotate = all_vm_rotatable_records[0] if len(all_vm_rotatable_records) > 0 else "NO_RECORDS_VM"

    return """
        <html>
            <head>
                    {css}
            </head>
            
            <body>
                <h1>🐛 Firefly! <img src="https://raw.githubusercontent.com/Keeper-Security/Commander-Firefly/main/docs/878036.svg" alt="Firefly Icon" width="40" height="40"></h1>
                
                <br/>
                <h3>Admin Keeper Record</h3><br />
                <blockquote>UID: <strong>{adm_rec_uid}</strong></blockquote>
                <blockquote>Title: <strong>{title}</strong></blockquote><br />
                <hr/>
                <br/>
                <br/>
                <a href=/api/v1/firefly/rotate/az/ad?uid={ad_rec_uid}>Rotate One Azure Active Directory Record [<strong>{ad_rec_title}</strong>]</a><br/>
                <a href=/api/v1/firefly/rotate/az/ad>Rotate all Azure Active Directory Records (total: <strong>{tot_ad_recs}</strong>)</a> <br/>
                <br/>
                <br/>
                <a href=/api/v1/firefly/rotate/az/vm?uid={vm_rec_uid}>Rotate One Azure VM Local Admin Password [<strong>{vm_title}</strong>]</a><br/>
                <a href=/api/v1/firefly/rotate/az/vm>Rotate all Azure VM Local Admin Passwords (total: <strong>{tot_vm_recs}</strong>)</a> <br/>
                
                <hr />
                Vault revision {vault_rev}. <a href=/api/v1/firefly/sync-down>Sync Down</a> <br/>
            </body>
        </html>
        
    """.format(
               css=getcss(),
               adm_rec_uid=az_admin_record.record_uid,
               title=az_admin_record.title,
               tot_ad_recs=len(all_ad_rotatable_records),
               ad_rec_uid=ad_rec_to_rotate.record_uid,
               ad_rec_title=ad_rec_to_rotate.title,
               tot_vm_recs=len(all_vm_rotatable_records),
               vm_rec_uid=vm_rec_to_rotate.record_uid,
               vm_title=vm_rec_to_rotate.title,
               vault_rev=params.revision)


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


@app.route('/api/v1/firefly/sync-down', methods=['GET'])
def sync_down():

    Firefly.sync_down(params)

    return redirect("/", code=302)


def getcss():
    return """
    <style>
        body {
            background: linear-gradient(-45deg,
                #FFFFFB, 
                #FFFFFF
                );
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }
        
        @keyframes gradient {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
    </style>
    """


if __name__ == '__main__':
    app.run()
