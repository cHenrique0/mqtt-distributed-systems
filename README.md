# MQTT - Message Queuing Telemetry Transport

A small project that simulates a residencial automation using the mqtt protocol made as homework of the discipline of Distributed Systems at UFMA.  

The project simulates three sensors(temperature, humidity and water level) in three different areas(bedroom, garden and swimming pool). Each sensor is a mqtt client and publish your data. There are three more clients who subscribe to the topic provided by the sensors and monitor each message published.

##### _This project was made with:_
  * [python 3.10.7](#read-more)
  * [paho-mqtt](#read-more)
  * [mosquitto](#read-more)

## Instructions

Homework: Develop an application using MQTT.

Description:
- Implement the mqtt protocol in a language of your choice.


## Run the project

#### 1. Clone the project
```sh
git clone git@github.com:cHenrique0/mqtt-protocol.git
```

#### 2. Install the requirement

After cloning the project:

```sh
cd mqtt-protocol

pip intall --upgrade pip

pip install -r requirements.txt
```

#### 3. Install the mosquitto broker

For instructions on how to install the broker: [Mosquitto download](https://mosquitto.org/download/)  

***If you are using Windows, you may need to restart your system for the installation to work.***

#### 4. Running
```sh
# Open a terminal and run the publisher
python pub.py

# In another terminal run the subscriber
python sub.py
```

## Read more <a id="read-more"></a>
* [MQTT](https://mqtt.org/)
* [Mosquitto](https://mosquitto.org/)
* [Paho Project](https://www.eclipse.org/paho/)
* [Python](https://www.python.org/downloads/)
