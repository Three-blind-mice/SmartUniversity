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
            log_message = "Получено сообщение: {1}".format(str(msg.payload))
            self._logger.persist(log_message)
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

        self.publish_response(response, sender_id)
        log_responce = 'Отправлен ответ: {1}'.format(response)
        self._logger.persist(log_responce)

    def publish_response(self, response, sender_id):
        json_string = {
            "answer": response,
            "id": sender_id,
        }
        message = json.dumps(json_string)
        self._client.publish(topic=self._response_topic, payload=message)

    def on_connect(self, client, userdata, flags, rc):
        log_connect = 'Код соединения с брокером: {1}'.format(rc)
        self._logger.persist(log_connect)
        if rc == mqtt.CONNACK_ACCEPTED:
            try:
                self._client.subscribe(self._commands_topic)
            except Exception as e:
                print(e)
            log_subscribe = 'Оформлена подписка на топик: {1}'.format(self._commands_topic)
            self._logger.persist(log_subscribe)

    def get_message(self):
        self._client.loop()
