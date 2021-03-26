# Commander-Firefly
Commander Password Rotator POC

[![Deploy To Azure Py-Hi](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FKeeper-Security%2FCommander-Firefly%2Fmain%2Fdeployment%2Fazuredeploy-az-appservice.json)




Setup:
1. Collect Config details
    
    a. Using [Keeper Commander](https://github.com/Keeper-Security/Commander) generate config file
    
    b. 

2. In Keeper Vault create a new record that will contain details for the Azure Active Directory App registration. See below how to obtain one.
Custom fields in the record:
   
| Custom field name | Custom field value |
| ----------------- | ------------------ |
| `cmdr:azure_tenant_id` | Tenant ID |
| `cmdr:azure_client_id` | Client ID |
| `cmdr:azure_secret` | Client Secret |

![img_1.png](img_1.png)

Rest endpoints:
Rotate all records: [app-url]/api/v1/firefly/rotate

Rotate single record: [app-url]/api/v1/firefly/rotate?uid=UID123



## Azure AD App Registration
Steps to obtain Azure Active Directory App registration with permissions to modify password in Active Directory

### Register new application
1. Navigate to new app registration page: Azure portal -> `Azure Active Directory` -> `App Registrations` -> `New Registration`
2. Give a name to the application and leave Supported account type as "Accounts in this organizational directory only (Default Directory only - Single tenant)"
3. Click "Register"

### Add a role to the application
1. Azure portal -> `Azure Active Directory` -> `Roles and administrators`
2. Search for `Helpdesk Administrator` role and click on it
3. Click on `+ Add assignments`
4. Search for the application that was created above, select it, and click on "Add"

### Create App Secret
1. Navigate to Azure portal -> `Azure Active Directory` -> `App Registrations` -> Select app that was created above -> `Certificates & secrets`
2. Under "Client secrets" click on `+ New client secret`
3. Give description to a secret and click "Add"
4. Make sure to copy "Value" of the secret