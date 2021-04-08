
# POC Deployment Checklist

- [ ] Azure
  - [ ] Azure Account w/ Active Subscription
  - [ ] New or existing Resource Group in the [supported](docs/supported-az-regions.md) Azure Region
  - [ ] Windows VM
  - [ ] Azure Active Directory Accounts
  - [ ] App Registration
  - [ ] App Registration Permissions
    - [ ] Access to Active Directory
    - [ ] RBAC to Windows VM

- [ ] Keeper
  - [ ] Valid Keeper Account
  - [ ] Records
    - [ ] App Registration Info details
      - [ ] Custom Field: `tag`=`azure app registration`
      - [ ] Custom Field: `cmdr:azure_tenant_id`=``
      - [ ] Custom Field: `cmdr:azure_client_id`=``
      - [ ] Custom Field: `cmdr:azure_secret`=``
    - [ ] Active Direcotry Accounts/Users details
      - [ ] Login: Aazure AD Email address
      - [ ] Custom Field: `tag`=`azure ad rotatable`
    - [ ] Windows VM details
      - [ ] Login: Local Admin username
      - [ ] Custom Field: `tag`=`azure vm rotatable`
      - [ ] Custom Field: `az:subscription_id`=``
      - [ ] Custom Field: `az:resource_group_name`=``
      - [ ] Custom Field: `az:vm_name`=``

- [ ] Commander
  - [ ] Installed Python Commander
  - [ ] Generated `config.json` file using Valid Keeper Account
