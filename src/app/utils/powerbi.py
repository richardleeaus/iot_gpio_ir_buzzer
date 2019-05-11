# import requests
# import adal
import json
import os
from pubnub.exceptions import PubNubException
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from dotenv import load_dotenv
load_dotenv()
 
def publish_callback(result, status):
    print("async Callback success")
    print("publish timetoken: %d" % result.timetoken)
    pass

class PowerBI(object):
    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = os.getenv('pbi_subscribe_key')
    pnconfig.publish_key = os.getenv('pbi_publish_key')
    pnconfig.ssl = False
    
    pubnub = PubNub(pnconfig)

    def pub_something(self, channel, message):
        
        try:
            message = json.loads(message)
            self.pubnub.publish().channel(channel).message(message).pn_async(publish_callback)
            
        except PubNubException as e:
            print(str(e))

if __name__ == '__main__':
    pbi = PowerBI()
    token = pbi.pub_something()

