# **E5 Developer Renewer**

![CICD](https://github.com/KKtheGhost/E5_Developer_Renew/actions/workflows/autoapi.yml/badge.svg?branch=master)
![License](https://shields.io/badge/license-MIT-%23373737)
![Repo Size](https://img.shields.io/github/repo-size/KKtheGhost/E5_Developer_Renew)
![Contributors](https://img.shields.io/github/contributors/KKtheGhost/E5_Developer_Renew)

文档地址: [ENG](https://github.com/KKtheGhost/E5_Developer_Renew/blob/master/README.md) | [简体中文](https://github.com/KKtheGhost/E5_Developer_Renew/blob/master/README_CN.md)

---
## **项目简介**

一个用于续期 Microsoft 365 E5 Developer 账号的小项目，具有以下特点：
* 使用 GitHub Actions 续期 Microsoft 365 E5 Developer 账号。
* 100% 免费使用。
* 使用 GitHub Secrets 来保证账号安全，无需担心账号被盗。

## **特别感谢**
* `@WangZiYingWen`：https://github.com/wangziyingwen/
* `TippeColee`：https://github.com/TippeColee/

## **我优化了什么**
- 将所有需要的秘钥隐藏在 GitHub Secrets 中。
- 重命名文件，使其更容易理解。
- 简化 `auto_renew_e5.py` 中的代码。
- 优化 GitHub Action 工作流

## **如何使用本项目**

### <font color="Olive">**1. Fork 本项目到你的 GitHub 账号下**</font>

如何 Fork 项目：https://docs.github.com/en/github/getting-started-with-github/fork-a-repo

### <font color="Olive">**2. 在你的 E5 Azure Active Directory 中注册一个新应用程序**</font>

登录你的 **[Azure Portal](https://portal.azure.com/#allservices/category/All)**，并在顶部侧边栏中点击 `Azure Active Directory`。

在左侧侧边栏中点击 `App registrations`，然后点击 `New registration`。

选择 `Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)` 作为支持的账户类型。

然后在 `Redirect URI` 部分，选择 `Web` 并填入 `http://localhost:53682/` 作为重定向 URI。

点击 `Register` 完成注册。

请保存你新创建的 application 的 **`Application (client) ID [1]`** 和 **`Client secret [2]`** 以便之后使用

### <font color="Olive">**3. 为你的新 Application 创建一个新的 Certificate**</font>

Click your new application's name in the `App registrations` page, and then click `Certificates & secrets` in the left sidebar.

Click `New client secret` and fill in a description for your new client secret.

Please save your new client secret's **`Value [3]`** for later use.

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

### <font color="Olive">**4. Get your first `refresh token [4]`.**</font>

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

Please save your new **`fine-grained token [5]`** for later use.

### <font color="Olive">**6. Add the secrets to your repository.**</font>

Now, all the prerequisites are ready. Let's add the secrets to your repository.

Go back to your new forked repository, click `Settings` in the end of left sidebar, and then click `Secrets and variables` in the left sidebar.

Click `Actions`, then choose the `Secrets` tab, and then click `New repository secret`.

Please add 4 secrets to your repository:
- `CONFIG_ID`：Save `Application (client) ID [1]` as the value.
- `CONFIG_SECRET`：Save `Value [3]` as the value.
- `CONFIG_REFRESH`：Save `refresh_token [4]` as the value.
- `E5_API`：Save `fine-grained token [5]` as the value.

Now everything is ready. You leave the rest to GitHub Actions.

## **Disclaimer**
This project is for educational and experimental purposes only. I am not responsible for any damage caused by this project. Please use it at your own risk.
