import paho.mqtt.client as mqtt
import json
from zoomdriver import ZoomDriver
from lmsdriver import LmsDriver
from exception import DriverError
from settings import *
import datetime
from logger import Logger


class MessageHandler:

    def __init__(self, topic):
        self._commands_topic = mqtt_command_topic.format(topic)
        self._response_topic = mqtt_response_topic
        self._client = mqtt.Client(protocol=mqtt.MQTTv311)
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message
        self._client.username_pw_set(mqtt_login, mqtt_password)
        self._client.connect(host=mqtt_broker,
                             port=mqtt_port,
                             keepalive=mqtt_keepalive)
        self._logger = Logger()
        self._driver_dict = {'zoom': ZoomDriver,
                             'lms': LmsDriver}
        self._commands_dictionary = {'ON': lambda driver: driver.turn_on,
                                     'OFF': lambda driver: driver.turn_off}

    def on_message(self, client, userdata, msg):
        response = ''
        if msg.topic == self._commands_topic:
            print("{0}: Received message payload: {1}".format(datetime.datetime.now().time(), str(msg.payload)))
            try:
                message_dictionary = json.loads(msg.payload)
                driver_key = message_dictionary['driver'].lower()
                command = message_dictionary['command']
                params = message_dictionary['params']
                sender_id = message_dictionary['id']
                driver = self._driver_dict[driver_key]()
                if command in self._commands_dictionary:
                    driver.set_session(params)
                    method = self._commands_dictionary[command](driver)
                    method()
                    response = 'Команда {0} была успешно выполнена'.format(command)
                else:
                    response = 'Команда {0} не поддерживатся'.format(command)
            except KeyError:
                response = 'Неправильный формат сообщения'
            except DriverError as err:
                response = err.txt
            except Exception as err:
                response = 'Неизвестная ошибка: {0}'.format(err)
        print('{0}: {1}'.format(datetime.datetime.now().time(), response))
        self._logger.persist(response)
        self.publish_response(response, sender_id)

    def publish_response(self, response, sender_id):
        json_string = {
            "answer": response,
            "id": sender_id,
        }
        message = json.dumps(json_string)
        self._client.publish(topic=self._response_topic, payload=message)
        print('{0}: Sent message: {1} on topic: {2}'.format(datetime.datetime.now().time(), message,
                                                            self._response_topic))

    def on_connect(self, client, userdata, flags, rc):
        print('{0}: Connected with rc: {1}'.format(datetime.datetime.now().time(), rc))
        if rc == mqtt.CONNACK_ACCEPTED:
            try:
                self._client.subscribe(self._commands_topic)
            except Exception as e:
                print(e)
            print('{0}: Subscribed on topic: {1}'.format(datetime.datetime.now().time(), self._commands_topic))

    def get_message(self):
        self._client.loop()
