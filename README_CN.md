# **E5 Developer Renewer**

![CICD](https://github.com/KKtheGhost/E5_Developer_Renew/actions/workflows/autoapi.yml/badge.svg?branch=master)
![License](https://shields.io/badge/license-MIT-%23373737)
![Repo Size](https://img.shields.io/github/repo-size/KKtheGhost/E5_Developer_Renew)
![Contributors](https://img.shields.io/github/contributors/KKtheGhost/E5_Developer_Renew)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

请保存你新创建的 application 的 **`Application (client) ID`** 为 **`Value[1]`**，保存 **`Client secret`** 为 **`Value[2]`** 以便之后使用

### <font color="Olive">**3. 为你的新 Application 创建一个新的 Certificate**</font>

在 `App registrations` 页面中，点击你的新应用程序的名称，然后在左侧边栏中点击`Certificates & secrets`。

点击 `New client secret`，并为你的新客户端密码填写一个描述。

请保存你的新客户端密码为 **`Value [3]`**，以备后用。

然后点击左侧边栏中的 `Authentication`。在 `Implicit grant and hybrid flows` 中，选择 `ID tokens` 和 `Access tokens` 。然后点击 `Save` 以完成 `Authentication` 配置。

接下来，在左侧边栏中点击 `API permissions`。点击 `Add a permission`，然后在 `APIs my organization uses` 部分中选择 `Microsoft Graph`。

添加下面列出的所有权限，并点击 `Add permissions` 以完成 `API permissions` 配置：

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

老实说，并非所有权限都是必需的。这取决于 `auto_renew_e5.py` 中的 API 列表。如果你不需要，可以移除这些权限。

最后，点击 `Grant admin consent for <your tenant name>`，将权限授予你的租户。

### <font color="Olive">**4. 获取你 E5 App 的 `refresh token` 并保存为 `Value[4]`.**</font>

请在您的计算机上安装 `rclone`，然后运行以下命令以获取您的首个 refresh token。

- 对于 Windows 用户，您可以从[这里](https://rclone.org/downloads/)下载 `rclone`，或使用 `choco install rclone` 进行安装。
- 对于 Linux 和 macOS 用户，请参考[此文章](https://rclone.org/install/)。

有关更多信息，请参阅[此文章](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)。完成注册大约需要 5 分钟。

完成后，请运行以下命令以获取您的首个 refresh token。
```bash
rclone authorize "onedrive" "<Value[1]>" "<Value[3]>"
```
 > Note: `Client secret (Value[2])` 不是必须的.

在运行命令后，将会弹出一个浏览器窗口，并要求您登录到您的E5帐户。登录后，您将被要求授予新应用程序的权限。请点击 `Accept` 以完成授权。

然后，`rclone` 将返回一个 JSON 字符串：

```json
{
	"access_token": "eyJ0eXAiOi*****************",
	"token_type": "Bearer",
	"refresh_token": "0.AVY******************",
	"expiry": "2023-03-20T23:06:01.8800926+08:00"
}
```
其中的 `refresh_token` 字段就是我们需要的 **`Value[4]`**.

### <font color="Olive">**5. 为你的 E5 自动更新仓库创建一个 Fine-grained Token**</font>

登录到你的 **[GitHub account](https://github.com)**，点击右上角的个人头像，然后点击 `Settings`。

在左侧边栏底部，点击 `Developer settings`，然后点击 `Personal access tokens`。

选择 `Fine-grained permissions`，然后点击 `Generate new token`。

为你的新令牌填写一个描述，并将过期日期设置为 1 年。在 `Repository access` 部分，选择 `Only selected repositories`，然后选择你的 forked 仓库。在 `Repository access` 部分，选择 `Secrets`、`Metadata` 和 `Actions`，将权限设置为 `Read & write`。最后，点击 `Generate token` 完成令牌的创建。

请将你的新的 `fine-grained token` 保存为 **`Value[5]`** 以备后用。

### <font color="Olive">**6. Add the secrets to your repository.**</font>

现在，所有的前提条件都已经准备就绪。让我们把密钥添加到你的代码仓库中。

返回你新创建的分叉仓库，点击左侧边栏末尾的 `Settings`，然后点击左侧边栏的 `Secrets and variables`。

点击 `Actions`，然后选择 `Secrets` 选项卡，再点击 `New repository secret`。

请向你的代码仓库添加以下 4 个密钥：
- `CONFIG_ID`：Save `Application (client) ID` as the value. --> **`Value[1]`**
- `CONFIG_KEY`：Save `Value [3]` as the value. --> **`Value[3]`**
- `CONFIG_REFRESH`：Save `refresh_token` as the value. --> **`Value[4]`**
- `E5_API`：Save `fine-grained token` as the value. --> **`Value[5]`**

现在一切准备就绪。泡一杯咖啡，然后把剩下的工作交给 GitHub Actions。

## **免责声明**
注意：本项目仅供教育和实验目的使用。对于由本项目造成的任何损害，我不承担任何责任。请自行承担使用风险。
