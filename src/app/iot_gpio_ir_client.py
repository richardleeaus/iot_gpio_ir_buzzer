import random
import time
import sys
import iothub_client
import datetime
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue
# from powerbi import PowerBI

import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)  # IR
GPIO.setup(3, GPIO.OUT)  # LED
GPIO.setup(11, GPIO.OUT)  # BUZZER

# chose HTTP, AMQP or MQTT as transport protocol
PROTOCOL = IoTHubTransportProvider.MQTT
CONNECTION_STRING = "HostName=RichardPOC.azure-devices.net;DeviceId=pi1-movement;SharedAccessKey=YAYWnMJwMl29jmJtSk9M7IdTIN5qLB+o9v7slvvCXhQ="
MSG_TXT = "{\"datetime\": \"%s\", \"deviceId\": \"myRaspberryPi\", \"online\": %i}"
MESSAGE_COUNTER = 0
SEND_REPORTED_STATE_CALLBACKS = 0
SEND_CALLBACKS = 0
RECEIVE_CALLBACKS =0

def send_confirmation_callback(message, result, user_context):
    global SEND_CALLBACKS
    print("Confirmation[%d] received for message with result = %s" % (user_context, result))
    map_properties = message.properties()
    key_value_pair = map_properties.get_internals()
    print("    Properties: %s" % key_value_pair)
    SEND_CALLBACKS += 1
    print("    Total calls confirmed: %d" % SEND_CALLBACKS)

def send_reported_state_callback(status_code, user_context):
    global SEND_REPORTED_STATE_CALLBACKS
    print ( "Confirmation for reported state received with:\nstatus_code = [%d]\ncontext = %s" % (status_code, user_context) )
    SEND_REPORTED_STATE_CALLBACKS += 1
    print ( "    Total calls confirmed: %d" % SEND_REPORTED_STATE_CALLBACKS )

# receive_message_callback is invoked when an incoming message arrives on the specified 
# input queue (in the case of this sample, "input1").  Because this is a filter module, 
# we will forward this message onto the "output1" queue.
# def receive_message_callback(message, hubManager):
#     global RECEIVE_CALLBACKS
#     message_buffer = message.get_bytearray()
#     size = len(message_buffer)
#     print ( "    Data: <<<%s>>> & Size=%d" % (message_buffer[:size].decode('utf-8'), size) )
#     map_properties = message.properties()
#     key_value_pair = map_properties.get_internals()
#     print ( "    Properties: %s" % key_value_pair )
#     RECEIVE_CALLBACKS += 1
#     print ( "    Total calls received: %d" % RECEIVE_CALLBACKS )
#     hubManager.forward_event_to_output("output1", message, 0)
#     return IoTHubMessageDispositionResult.ACCEPTED

class HubManager(object):

    def __init__(
            self,
            connection_string,
            protocol=IoTHubTransportProvider.MQTT):
        self.client_protocol = protocol
        self.client = IoTHubClient(connection_string, protocol)
        if protocol == IoTHubTransportProvider.HTTP:
            self.client.set_option("timeout", TIMEOUT)
            self.client.set_option("MinimumPollingTime", MINIMUM_POLLING_TIME)
        # set the time until a message times out
        self.client.set_option("messageTimeout", 100000)
        # for IoT Edge?
        # self.client.set_message_callback("input1", receive_message_callback, self)


    def send_event(self, event, properties, send_context):
        if not isinstance(event, IoTHubMessage):
            event = IoTHubMessage(bytearray(event, 'utf8'))

        if len(properties) > 0:
            prop_map = event.properties()
            for key in properties:
                prop_map.add_or_update(key, properties[key])

        self.client.send_event_async(
            event, send_confirmation_callback, send_context)

    def send_reported_state(self, reported_state, size, user_context):
        self.client.send_reported_state(
            reported_state, size,
            send_reported_state_callback, user_context)


def main(connection_string, protocol):
    global MESSAGE_COUNTER
    try:
        print("\nPython %s\n" % sys.version)
        print("IoT Hub Client for Python")

        hub_manager = HubManager(connection_string, protocol)

        print( "Starting the IoT Hub Python sample using protocol %s..." % hub_manager.client_protocol)

        reported_state = "{\"newState\":\"standBy\"}"

        hub_manager.send_reported_state(reported_state, len(reported_state), 1002)

        while True:
            i = GPIO.input(7)
            if i==0:
                print("No motion sensed")
                # pbi.pub_something("my_channel", MSG_TXT % (datetime.datetime.now(), 0))
                hub_manager.send_event(MSG_TXT % (datetime.datetime.now(), 0), {}, MESSAGE_COUNTER)
            else:
                # GPIO.output(11, True) # beep
                GPIO.output(3,1) # LED
                print("Motion detected")
                
                hub_manager.send_event(MSG_TXT % (datetime.datetime.now(), 1), {}, MESSAGE_COUNTER)
                # pbi.pub_something("my_channel", MSG_TXT % (datetime.datetime.now(), 1))
                print("IoTHubClient.send_event_async accepted message [%d] for transmission to IoT Hub." % MESSAGE_COUNTER )
                time.sleep(.1)
                GPIO.output(11, False)
                GPIO.output(3,0)
            time.sleep(4)
            MESSAGE_COUNTER += 1
            
    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    # pbi = PowerBI()
    main(CONNECTION_STRING, PROTOCOL)
