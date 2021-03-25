# #  _  __
# # | |/ /___ ___ _ __  ___ _ _ ®
# # | ' </ -_) -_) '_ \/ -_) '_|
# # |_|\_\___\___| .__/\___|_|
# #              |_|
# #
# # Keeper Commander
# # Copyright 2021 Keeper Security Inc.
# # Contact: ops@keepersecurity.com
# #
#
# from keepercommander.params import KeeperParams
# from firefly import Firefly
#
#
#
#
# if __name__ == '__main__':
#
#
#
#     az_ad_user1_record_uid = '50cLhCRC-jK8YZY6EInRJQ'
#     az_ad_user2_record_uid = 'OPU-UzB2NubF8jFPduFVZw'
#
#     ff = Firefly
#
#     params = KeeperParams()
#
#     ff.login(params)
#     all_records = ff.get_all_records(params)
#     json_str = ff.to_json_str(all_records)
#
#     ff.rotate_az_ad_acct(
#                          params,
#                          az_ad_admin_record_uid,
#                          az_ad_user1_record_uid
#                          )
