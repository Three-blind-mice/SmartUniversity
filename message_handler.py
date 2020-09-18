import paho.mqtt.client as mqtt
import json
from settings import *
from zoomdriver import ZoomDriver, DiscordDriver


class MessageHandler:
    """
    Класс для обработки команд. Команды передаются по протаколу MQTT.
    Объект данного класса устанавливает соединение с MQTT брокером, подписывается на topic,
    принимает поступающие в topic сообщения и в соответствии с командой передает управление определенному драйверу
    Перечень поддерживаемых драйверов указан в словаре driver_dict
    По завершении обработки запроса объект формирует служебное сообщение на служебный топик о выполнении команды
    """
    zoom_driver = ZoomDriver()
    discord_driver = DiscordDriver()
    driver_dict = {'zoom': zoom_driver,
                   'discord': discord_driver}
    commands_dictionary = {'ON': lambda driver: driver.turn_on,
                           'OFF': lambda driver: driver.turn_off}

    def __init__(self, topic):
        MessageHandler.commands_topic = topic
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        self.client.on_connect = MessageHandler.on_connect
        self.client.on_message = MessageHandler.on_message
        self.client.username_pw_set(mqtt_login, mqtt_password)
        self.client.connect(host=mqtt_broker,
                            port=mqtt_port,
                            keepalive=mqtt_keepalive)

    @staticmethod
    def on_message(client, userdata, msg):
        if msg.topic == MessageHandler.commands_topic:
            print("Received message payload:{0}".format(str(msg.payload)))
            try:
                message_dictionary = json.loads(msg.payload)
                driver_key = message_dictionary['driver'].lower()
                command = message_dictionary['command']
                params = message_dictionary['params']
                driver = MessageHandler.driver_dict[driver_key]
                driver.set_params(params)
                if command in MessageHandler.commands_dictionary:
                    method = MessageHandler.commands_dictionary[command](driver)
                    response = 'Command {0} executed with code: {1}'.format(command, method())
                    print(response)
                else:
                    response = '{0}; {1}'.format(UNSUPPORTED_COMMAND_ERROR, command)
                    print(response)
            except KeyError:
                response = MESSAGE_FORMAT_ERROR
                MessageHandler.publish_response(response=response)
                print(response)

        MessageHandler.publish_response(command, response)
    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print('Connected with rc: {}'.format((rc)))
        if rc == mqtt.CONNACK_ACCEPTED:
            client.subscribe(MessageHandler.commands_topic)
            print('Subscribed on topic: {}'.format(MessageHandler.commands_topic))
    @staticmethod
    def publish_response(command=None, response=None):
        pass
        #self.client.publish(topic=mqtt_topic_execute_command, payload=response)

    def get_message(self):
        self.client.loop()
