from phue import Bridge
from prometheus_client import start_http_server, Gauge
import time
#import pprint

b = Bridge('10.0.0.133')
#pp = pprint.PrettyPrinter(indent=4)

##Prometheus metrics
front_door_temperature = Gauge('front_door_temperature', 'Outside temperature (C) at the front door')
front_door_presence = Gauge('front_door_presence', 'Presence detected at the front door')
front_door_light_level = Gauge('front_door_light_level', 'Light level (Lux) at the front door')

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        time.sleep(15)
        api = b.get_api()
        for s in api.get('sensors'):
            sensor_data = api.get('sensors').get(s)
            if sensor_data.get('type') == 'ZLLTemperature' and sensor_data.get('name') == 'Hue temperature sensor 1':
                front_door_temperature.set(sensor_data.get('state').get('temperature'))
            if sensor_data.get('type') == 'ZLLPresence' and sensor_data.get('name') == 'Hue motion sensor 1':
                front_door_presence.set(sensor_data.get('state').get('presence'))
            if sensor_data.get('type') == 'ZLLLightLevel' and sensor_data.get('name') == 'Hue ambient light sensor 1':
                front_door_light_level.set(sensor_data.get('state').get('lightlevel'))

        # Print whole api
        #pp.pprint(api)
        # Print sensors
        #pp.pprint(api.get('sensors'))

        # for s in api.get('sensors'):
        #     sensor_data = api.get('sensors').get(s)
        #     if sensor_data.get('type') == 'ZLLTemperature':
        #         print("%s: %s" % (sensor_data.get('name'), sensor_data.get('state').get('temperature')))
        #         front_door_temperature.set(sensor_data.get('state').get('temperature'))
        #     if sensor_data.get('type') == 'ZLLPresence':
        #         print("%s: %s" % (sensor_data.get('name'), sensor_data.get('state').get('presence')))
        #         front_door_presence.set(sensor_data.get('state').get('presence'))
        #     if sensor_data.get('type') == 'ZLLLightLevel':
        #         print("%s: %s" % (sensor_data.get('name'), sensor_data.get('state').get('lightlevel')))
        #         front_door_light_level.set(sensor_data.get('state').get('lightlevel'))
