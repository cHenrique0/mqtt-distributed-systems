from struct import unpack
import sys
import paho.mqtt.client as mqtt

from database.Connection import connect, select

# MQTT client settings
# HOST= "mqtt://test.mosquitto.org/"
HOST = "127.0.0.1"
PORT = 1883

# Connecting to the database
FILE = "./database/sensors.db"
database = connect(FILE)

# Get the sensors from the database
sensors = select(database, "sensors")

if len(sensors) == 0:
    print("No sensors found in the database")
    sys.exit(-1)


def topic_menu():
    """
    Print the menu
    """
    print("""
    Topics:

    1 - Bedroom
    2 - Garden
    3 - Pool
    4 - All
    """)
    print("Type the number of the topic you want to subscribe: ")


def on_connect(client, data, flags, status, rc):
    """
    Subscribe to the topic when the connection is established
    """

    # Getting the sensors
    temp_sensor = select(database, "sensors", {"sensor_type": "temperature"})
    hum_sensor = select(database, "sensors", {"sensor_type": "humidity"})
    lvl_sensor = select(database, "sensors", {"sensor_type": "level"})

    # Creating the topics to subscribe
    # Reading all publish in area: bedroom
    bedroom = f"area/{temp_sensor[1]}/sensor/{temp_sensor[0]}/#"
    # Reading all publish in area: garden
    garden = f"area/{hum_sensor[1]}/sensor/{hum_sensor[0]}/#"
    # Reading all publish in area: pool
    pool = f"area/{lvl_sensor[1]}/sensor/{lvl_sensor[0]}/#"

    print("Connected to MQTT broker")

    topic_menu()

    answer = int(input(">> ").strip())
    while answer not in [1, 2, 3, 4]:
        print("Invalid option. Try again:")
        answer = int(input(">> "))

    # Subscribing to the topic according to the user's choice
    if answer == 1:
        print(f"Subscribing to: \n* [{bedroom}]")
        client.subscribe(bedroom)
    elif answer == 2:
        print(f"Subscribing to: \n* [{garden}]")
        client.subscribe(garden)
    elif answer == 3:
        print(f"Subscribing to: \n* [{pool}]")
        client.subscribe(pool)
    elif answer == 4:
        print(f"Subscribing to: \n* [{bedroom}]\n* [{garden}]\n* [{pool}]")
        client.subscribe(bedroom)
        client.subscribe(garden)
        client.subscribe(pool)

    print("\nMonitoring:\n")


def on_message(client, data, msg):
    """
    Print the topic and value when a message is received
    """
    decoded_payload = unpack('>H', msg.payload)[0]
    print(f"{msg.topic}/{decoded_payload}")


# Create a client to supervise
mqtt_client = mqtt.Client(client_id="SCADA", protocol=mqtt.MQTTv5)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT broker
mqtt_client.connect(HOST, PORT)

# Start the loop
mqtt_client.loop_forever()
