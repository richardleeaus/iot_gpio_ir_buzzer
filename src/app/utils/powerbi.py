# import requests
# import adal
import json
from pubnub.exceptions import PubNubException

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
 
def publish_callback(result, status):
    print("async Callback success")
    print("publish timetoken: %d" % result.timetoken)
    pass

class PowerBI(object):
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = "sub-c-1de56582-f517-11e8-babf-1e3d8cb2a384"
    pnconfig.publish_key = "pub-c-d64e7ffd-aad4-4a71-97b3-d63ad01d5ed2"
    pnconfig.ssl = False
    
    pubnub = PubNub(pnconfig)
    # api_key = ""
    # client_id = "294b5da3-aeed-42c1-a5c5-1fc2fc473bde"
    # access_token_host = ""
    # headers = ""
    # redirect_uri = "https://login.live.com/oauth20_desktop.srf"
    # resource_uri = "https://analysis.windows.net/powerbi/api"
    # authority_uri = "https://login.windows.net/common/oauth2/authorize"

    # def get_token(self):
    #     authority_url = 'https://login.microsoftonline.com/ignia.com.au'
    #     context = adal.AuthenticationContext(
    #         authority_url,
    #         validate_authority=True,
    #         api_version=None
    #     )

    #     token = context.acquire_token_with_username_password(
    #         resource='https://analysis.windows.net/powerbi/api',
    #         username='richard.lee@ignia.com.au',
    #         password='Shmint69)(*&^',
    #         client_id=self.client_id
    #     )

    #     access_token = token['accessToken']

    # # def something(self):
    # #     url = f'{self.api_url}/v1.0/myorg/groups/{self.group_id}/datasets'
    # #     headers = {
    # #         'Authorization': f'Bearer {self.token["accessToken"]}'
    # #     }

    def pub_something(self, channel, message):
        
        try:
            message = json.loads(message)
            self.pubnub.publish().channel(channel).message(message).pn_async(publish_callback)
            
        except PubNubException as e:
            print(str(e))

if __name__ == '__main__':
    pbi = PowerBI()
    token = pbi.pub_something()

