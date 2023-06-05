# -*- coding: UTF-8 -*-
import argparse
import requests as req
import json,sys,time
# Please register your Azure Application first, and grant it with the mandatory permissions below:
# files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
# user:	    User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
# mail:     Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
# Remember to Click "Grant admin consent for <your tenant>" in the "API Permissions" page.

path = sys.path[0]+r'/refresh_token.txt'
call_count = 0
api_list = [
    'https://graph.microsoft.com/v1.0/me/drive/root',
    'https://graph.microsoft.com/v1.0/me/drive',
    'https://graph.microsoft.com/v1.0/drive/root',
    'https://graph.microsoft.com/v1.0/users',
    'https://graph.microsoft.com/v1.0/me/messages',
    'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
    'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
    'https://graph.microsoft.com/v1.0/me/drive/root/children',
    'https://api.powerbi.com/v1.0/myorg/apps',
    'https://graph.microsoft.com/v1.0/me/mailFolders',
    'https://graph.microsoft.com/v1.0/me/outlook/masterCategories'
]

# Get the access token from microsoft graph api and write the new refresh token to the file.
def gettoken(id, secret, refresh_token):
    headers={'Content-Type':'application/x-www-form-urlencoded'
            }
    data={'grant_type': 'refresh_token',
          'refresh_token': refresh_token,
          'client_id': id,
          'client_secret': secret,
          'redirect_uri': 'http://localhost:53682/'
         }
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',data=data,headers=headers)
    jsontxt = json.loads(html.text)
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    with open(path, 'w+') as f:
        f.write(refresh_token)
    return access_token

def main():
    parser = argparse.ArgumentParser(description='Generate the access token from the refresh token to call the Microsoft Graph API.')
    parser.add_argument('-i', '--id', type=str, help='Application Client ID', required=True)
    parser.add_argument('-s', '--secret', type=str, help='Client Secret', required=True)
    parser.add_argument('-r', '--refresh', type=str, help='Refresh Token', required=True)
    args = parser.parse_args()

#    fo = open(path, "r+")
#    refresh_token = fo.read()
#    fo.close()
    global call_count
    access_token=gettoken(args.id, args.secret, args.refresh)
    headers={
    'Authorization':access_token,
    'Content-Type':'application/json'
    }

    for api in api_list:
        try:
            if req.get(api, headers=headers).status_code == 200:
                call_count += 1
                print(f"Call {api} successfully")
        except:
            pass

    print("End of the test, the total number of successful calls is:", call_count)

if __name__ == '__main__':
    for _ in range(5):
        main()
