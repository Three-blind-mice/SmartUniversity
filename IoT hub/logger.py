from influxdb import InfluxDBClient
import logging
import datetime


class Logger:

    def __init__(self):
        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', filename=u'iot-hub.log',
                            level=logging.DEBUG)
        self.log = logging.getLogger('ex')
        self.influx_client = InfluxDBClient(host='localhost', port=8086, database='iot-hub')

    def persists(self, msg):
        current_time = datetime.datetime.utcnow().isoformat()
        json_body = [
            {
                "measurement": "pot",
                "tags": {},
                "time": current_time,
                "fields": {
                    "value": msg
                }
            }
        ]
        try:
            self.log.info(json_body)
            #self.influx_client.write_points(json_body)
        except Exception as e:
            print(e)
