import paho.mqtt.client as mqtt
import json
from zoomdriver import ZoomDriver
from lmsdriver import LmsDriver
from exception import DriverError
from settings import *
import datetime

class MessageHandler:
    _driver_dict = {'zoom': ZoomDriver,
                    'lms': LmsDriver}
    _commands_dictionary = {'ON': lambda driver: driver.turn_on,
                            'OFF': lambda driver: driver.turn_off}
    _commands_topic = ''
    _response_topic = ''

    def __init__(self, topic):
        MessageHandler._commands_topic = mqtt_command_topic.format(topic)
        MessageHandler._response_topic = mqtt_response_topic
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        self.client.on_connect = MessageHandler.on_connect
        self.client.on_message = MessageHandler.on_message
        self.client.username_pw_set(mqtt_login, mqtt_password)
        self.client.connect(host=mqtt_broker,
                            port=mqtt_port,
                            keepalive=mqtt_keepalive)

    @staticmethod
    def on_message(client, userdata, msg):
        response = ''
        if msg.topic == MessageHandler._commands_topic:
            print("{0}: Received message payload: {1}".format(datetime.datetime.now().time(), str(msg.payload)))
            try:
                message_dictionary = json.loads(msg.payload)
                driver_key = message_dictionary['driver'].lower()
                command = message_dictionary['command']
                params = message_dictionary['params']
                sender_id = message_dictionary['id']
                driver = MessageHandler._driver_dict[driver_key]()
                if command in MessageHandler._commands_dictionary:
                    driver.set_session(params)
                    method = MessageHandler._commands_dictionary[command](driver)
                    method()
                    response = 'Command {0} successfully executed'.format(command)
                else:
                    response = 'Command {0} is unsupported command'.format(command)
            except KeyError:
                response = 'Wrong format of message'
            except DriverError as err:
                response = err.txt
            except Exception as err:
                print(err)
                response = 'Unknown error'
        print('{0}: {1}'.format(datetime.datetime.now().time(), response))
        MessageHandler.publish_response(client, response, sender_id)

    @staticmethod
    def publish_response(client, response, sender_id):
        json_string = {
            "answer": response,
            "id": sender_id,
        }
        message = json.dumps(json_string)
        client.publish(topic=MessageHandler._response_topic, payload=message)
        print('{0}: Sent message: {1} on topic: {2}'.format(datetime.datetime.now().time(), message, MessageHandler._response_topic))

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print('{0}: Connected with rc: {1}'.format(datetime.datetime.now().time(), rc))
        if rc == mqtt.CONNACK_ACCEPTED:
            client.subscribe(MessageHandler._commands_topic)
            print('{0}: Subscribed on topic: {1}'.format(datetime.datetime.now().time(), MessageHandler._commands_topic))

    def get_message(self):
        self.client.loop()
