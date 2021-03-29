# Commander Firefly POC

Commander Password Rotator Proof Of Concept (POC)
This template will create fully working Password rotation POC in Azure Cloud that will have endpoints to rotate Active Directory Users Password based on Keeper Record UID.

Following Components will be created and configured:

- App Service (Web App hosting Python Rest endpoints)
  - Source code will be cloned from GitHub project
  - Environment variables will be configured based on the data entered in the initial form

## Prerequisites

- Azure account with Active Subscription. [Link](https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade) to add new Subscription to the existing Azure account
- New or existing Resource Group
- Keeper Account
- Records in Keeper Vault
  1. Azure Service User with appropriate permissions with custom fields
  2. Azure Active Directory users details whose password will be rotated
- Locally installed [Keeper Commander](https://github.com/Keeper-Security/Commander)

## Components Diagram

![img.png](docs/img.png)

## Setup Steps

### 1. Configure Keeper Account
1. Login to [Keeper Vault](https://keepersecurity.com/vault/) with the new or existing Keeper Account
2. Make sure that 2FA is disabled by going to `Settings` -> `Security` and uncheck "Two-Factor Authentication"

### 2. Generate Keeper Commander Configuration file
1. Using [Keeper Commander](https://github.com/Keeper-Security/Commander) on local machine login using command: `keeper login` <br/><br />
![img_2.png](docs/img_2.png)<br/><br /> This will generate a new `config.json` file in the current working directory<br /><br/>![img_3.png](docs/img_3.png)<br />
   Open that file and take note of all the generated values there. We will use them later when we will be deploying Template to Azure

### 3. Create Azure AD Accounts/Users
- Follow steps from [the official Azure Documentation](https://docs.microsoft.com/en-us/azure/active-directory/fundamentals/add-users-azure-active-directory)
- Make a record for each account in Keeper Vault. Enter email address of the Azure AD User in the "Login" field and add following custom fields to mark it as rotatable:

| Custom field name | Custom field value |
| ----------------- | ------------------ |
| `tag` | `azure ad rotatable` |

<br/>Sample record in Keeper Vault
<br/>![img.png](docs/img_7.png)

### 4. Create Azure API Access (App Registration)

Needed for the Function to interact with Azure Active Directory API

1. Create App Registration and Secret.

    Follow steps from [HERE](https://github.com/Keeper-Security/Commander/tree/master/keepercommander/plugins/azureadpwd#configure-azure-application)

2. Create new Keeper Record with custom fields containing App Registration details

    Custom fields:

   | Custom field name | Custom field value |
   | ----------------- | ------------------ |
   | `cmdr:azure_tenant_id` | Tenant ID |
   | `cmdr:azure_client_id` | Client ID |
   | `cmdr:azure_secret` | Client Secret |
   | `tag` | `azure app registration` |

    Refer to [THIS](https://github.com/Keeper-Security/Commander-Firefly/blob/main/docs/img_1.png) image

Sample record in Keeper Vault<br />
![img_1.png](docs/img_8.png)

### 5. Deploy a template to Azure

<br />[![Deploy To Azure](https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/1-CONTRIBUTION-GUIDE/images/deploytoazure.svg?sanitize=true)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2FKeeper-Security%2FCommander-Firefly%2Fmain%2Fdeployment%2Fazuredeploy-az-appservice.json)

Fill out fields:
- Resource Group: Select Resource Group where infrastructure will be created
- Keeper Config Private Key: Value `private_key` from config.json file
- Keeper Config Device Token: Value `device_token` from config.json file
- Keeper User Email: Keeper Account User Email
- Keeper User Password: Keeper Account Password

![img.png](docs/img_9.png)

The following infrastructure will be created <br /> <br /> ![template-view.png](deployment/template-view.png)

### 6. Test

After infrastructure is creates, after about 5 - 10 min, navigate to the URL of the created website. URL can be found in the Overview page <br /> <br /> ![img.png](docs/img_5.png)

1. Rotate All Records

   [app-url]/api/v1/firefly/rotate

2. Rotate a single Record

   [app-url]/api/v1/firefly/rotate?uid=UID123

### 7. Cleanup

Login to Azure Portal, navigate to the Resource Group where the code was deployed and remove following:

- App Service: `firefly-[GUID]`
- App Service plan: `firefly-[GUID]-appServicePlan`
- Scheduler Job Collection: `firefly-[GUID]-cron` <br/> <br/>
![img.png](docs/img_6.png)
