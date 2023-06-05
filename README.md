# **E5 Developer Renewer**

![CICD](https://github.com/KKtheGhost/E5_Developer_Renew/actions/workflows/autoapi.yml/badge.svg?branch=master)
![License](https://shields.io/badge/license-MIT-%23373737)
![Repo Size](https://img.shields.io/github/repo-size/KKtheGhost/E5_Developer_Renew)
![Contributors](https://img.shields.io/github/contributors/KKtheGhost/E5_Developer_Renew)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Documentation: [ENG](https://github.com/KKtheGhost/E5_Developer_Renew/blob/master/README.md) | [简体中文](https://github.com/KKtheGhost/E5_Developer_Renew/blob/master/README_CN.md)

---
## **Project Summary**
A Tiny Project to renew Microsoft 365 E5 Developer accounts with features:
* Utilizes GitHub Actions to renew Microsoft 365 E5 Developer accounts.
* 100% Free for use.
* Security is ensured by using GitHub Secrets, no need to worry about the account being stolen.

## **Thanks to**
* `@WangZiYingWen`：https://github.com/wangziyingwen/
* `TippeColee`：https://github.com/TippeColee/

## **What I did**
- Hide all the secrets required for the project in GitHub Secrets.
- Rename the files to make it easier to understand.
- Simplify the code in `auto_renew_e5.py`.
- Optimize the workflow

## **How to use**

### <font color="Olive">**1. Fork this repository to your own GitHub account.**</font>

How to fork a repository: https://docs.github.com/en/github/getting-started-with-github/fork-a-repo

### <font color="Olive">**2. Register a new application in your E5 Azure Active Directory.**</font>

Login to your **[Azure Portal](https://portal.azure.com/#allservices/category/All)**, and click `Azure Active Directory` in the top sidebar.

In the left sidebar, click `App registrations`, and then click `New registration`.

Select `Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)` as the supported account type.

Then in the `Redirect URI` section, select `Web` and fill in `http://localhost:53682/` as the redirect URI.

Click `Register` to finish the registration.

Please save your new application's **`Application (client) ID`** as **`Value[1]`** and **`Client secret`** as **`Value[2]`** for later use.

### <font color="Olive">**3. Create a new certificate for you new application.**</font>

Click your new application's name in the `App registrations` page, and then click `Certificates & secrets` in the left sidebar.

Click `New client secret` and fill in a description for your new client secret.

Please save your `new client secret` as **`Value [3]`** for later use.

Then click `Authentication` in the left sidebar. In `Implicit grant and hybrid flows`, select `ID tokens` and `Access tokens`. The click `Save` to finish the `Authentication` configuration.

Then, click `API permissions` in the left sidebar. Click `Add a permission`, and then select `Microsoft Graph` in the `APIs my organization uses` section.

Add all the permissions listed below, and click `Add permissions` to finish the `API permissions` configuration:
- `files.read.all`
- `files.readwrite.all`
- `sites.read.all`
- `sites.readwriter.all`
- `user.read.all`
- `user.readwrite.all`
- `directory.read.all`
- `directory.readwrite.all`
- `mail.read`
- `mail.readwrite`
- `mailboxsetting.read`
- `mailboxsetting.readwrite`

To be honest, not all of the permissions are required. It depends on the API list in `auto_renew_e5.py`. You can remove the permissions if you don't need.

Finally, click `Grant admin consent for <your tenant name>` to grant the permissions to your tenant.

### <font color="Olive">**4. Get your first `refresh token` as `Value[4]`.**</font>

Install `rclone` on your computer, and then run the following command to get your first refresh token.

- For windows users, you can download `rclone` from [here](https://rclone.org/downloads/), or use `choco install rclone` to install it.
- For Linux and macOS users, please refer to [this article](https://rclone.org/install/).

For more information, please refer to [this article](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app). It will take you about 5 minutes to finish the registration. 

When you are done, please run the following command to get your first refresh token.

```bash
rclone authorize "onedrive" "<Application (client) ID>" "<Value>"
```
 > Note: `Client secret` is not required.

After you run the command, a browser window will pop up, and you will be asked to log in to your E5 account. After you log in, you will be asked to grant the permissions to your new application. Please click `Accept` to finish the authorization.

Then `rclone` will return a JSON string:

```json
{
	"access_token": "eyJ0eXAiOi*****************",
	"token_type": "Bearer",
	"refresh_token": "0.AVY******************",
	"expiry": "2023-03-20T23:06:01.8800926+08:00"
}
```
And the `refresh_token` is what we need.

### <font color="Olive">**5. Create a Fine-grained Token for your forked repository.**</font>

Login to your **[GitHub account](https://github.com)**, and click your profile picture in the top right corner, and then click `Settings`.

In the end of left sidebar, click `Developer settings`, and then click `Personal access tokens`.

Select `Fine-grained permissions`, and then click `Generate new token`.

Fill in a description for your new token, set the expiration date to 1 year. In `Repository access` section, select `Only select repositories`, and then select your forked repository. In `Repository access` section, select `Secrets`, `Metadata` and `Actions`, set the permission to `Read & write`. Finally, click `Generate token` to finish the token creation.

Please save your new **`fine-grained token`** as **`Value[5]`** for later use.

### <font color="Olive">**6. Add the secrets to your repository.**</font>

Now, all the prerequisites are ready. Let's add the secrets to your repository.

Go back to your new forked repository, click `Settings` in the end of left sidebar, and then click `Secrets and variables` in the left sidebar.

Click `Actions`, then choose the `Secrets` tab, and then click `New repository secret`.

Please add 4 secrets to your repository:
- `CONFIG_ID`：Save `Application (client) ID` as the value. --> **`Value[1]`**
- `CONFIG_KEY`：Save `Value [3]` as the value. --> **`Value[3]`**
- `CONFIG_REFRESH`：Save `refresh_token` as the value. --> **`Value[4]`**
- `E5_API`：Save `fine-grained token` as the value. --> **`Value[5]`**

Now everything is ready. You leave the rest to GitHub Actions.

## **Disclaimer**
This project is for educational and experimental purposes only. I am not responsible for any damage caused by this project. Please use it at your own risk.
