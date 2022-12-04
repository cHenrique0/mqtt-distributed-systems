from struct import pack
from random import randint
from time import sleep
import paho.mqtt.client as mqtt

from Sensor import Sensor, SENSORS
from database.Connection import connect, create_table, insert, select, update, drop_table


# MQTT client settings
# HOST = "mqtt://test.mosquitto.org/"
HOST = "127.0.0.1"
PORT = 1883

# Connecting to database
FILE = "./database/sensors.db"
database = connect(FILE)
drop_table(database, "sensors")
create_table(database)

# Creating sensors. If there are no sensors in database, create new ones
sensors = []
temp_sensor = Sensor(area="bedroom", sensor_type=SENSORS.TEMPERATURE)
hum_sensor = Sensor(area="garden", sensor_type=SENSORS.HUMIDITY)
lvl_sensor = Sensor(area="pool", sensor_type=SENSORS.LEVEL)
sensors.extend([temp_sensor, hum_sensor, lvl_sensor])

# Saving the sensors in the database
for sensor in sensors:
    sensor_data = [sensor.get_id(), sensor.get_area(),
                   sensor.get_type(), sensor.get_value()]
    insert(database, "sensors", sensor_data)

# Selecting all sensors from database again
sensor_data = select(database, "sensors")

# Creating client IDs based on IDs for each sensor
clients = {
    "temperature_client": None,
    "humidity_client": None,
    "level_client": None
}
for sensor in sensor_data:
    if sensor[2] == SENSORS.TEMPERATURE.lower():
        clients["temperature_client"] = mqtt.Client(
            client_id=f'NODE:{sensor[0]}-{sensor[1]}',
            protocol=mqtt.MQTTv5
        )
        # temp_sensor = Sensor(sensor[1], sensor[2])
    elif sensor[2] == SENSORS.HUMIDITY.lower():
        clients["humidity_client"] = mqtt.Client(
            client_id=f'NODE:{sensor[0]}-{sensor[1]}',
            protocol=mqtt.MQTTv5
        )
        # hum_sensor = Sensor(sensor[1], sensor[2])
    elif sensor[2] == SENSORS.LEVEL.lower():
        clients["level_client"] = mqtt.Client(
            client_id=f'NODE:{sensor[0]}-{sensor[1]}',
            protocol=mqtt.MQTTv5
        )
        # lvl_sensor = Sensor(sensor[1], sensor[2])

# Connect to MQTT broker
for _, client in clients.items():
    client.connect(HOST, PORT)


print("Publishing data...")
print("Press CTRL+C to exit\n")
while True:

    # Temperature
    # Generate a random value to represent the temperature
    temp_sensor.set_value(randint(0, 40))
    # Update the value in the database
    update(database, "sensors", [
           temp_sensor.get_value(), temp_sensor.get_id()])
    # Encode the value to big-endian(2 bytes)
    payload = pack('>H', temp_sensor.get_value())
    # Publish the value to the topic
    clients["temperature_client"].publish(
        temp_sensor.get_topic(), payload, qos=0)
    # Showing the topic and value on the console
    print(f"{temp_sensor.get_topic()}/{temp_sensor.get_value()}")
    sleep(2)

    # Humidity
    # Generate a random value to represent the humidity
    hum_sensor.set_value(randint(0, 100))
    update(database, "sensors", [
           hum_sensor.get_value(), hum_sensor.get_id()])
    payload = pack('>H', hum_sensor.get_value())
    clients["humidity_client"].publish(hum_sensor.get_topic(), payload, qos=0)
    print(f"{hum_sensor.get_topic()}/{hum_sensor.get_value()}")
    sleep(2)

    # Level
    # Generate a random value to represent the level
    lvl_sensor.set_value(randint(0, 1000))
    update(database, "sensors", [
           lvl_sensor.get_value(), lvl_sensor.get_id()])
    payload = pack('>H', lvl_sensor.get_value())
    clients["level_client"].publish(lvl_sensor.get_topic(), payload, qos=0)
    print(f"{lvl_sensor.get_topic()}/{lvl_sensor.get_value()}")
    sleep(5)
