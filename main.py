import os
import sys
import paho.mqtt.client as mqtt
from dotenv import load_dotenv
import psutil
import time
import json

load_dotenv()

NAME = os.getenv("NAME")
BROKER = os.getenv("BROKER")
PORT = int(os.getenv("PORT"))
KEEPALIVE = int(os.getenv("KEEPALIVE"))
TOPIC = os.getenv("TOPIC")
INTERVAL = int(os.getenv("INTERVAL"))

def on_connect(client, userdata, rc, what):
    print("Connected.", userdata, rc, what)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print("Message received.", userdata, msg.payload.decode("utf-8"), msg.topic, msg.qos, msg.retain)

def on_disconnect(client, userdata, rc):
    print("Disconnected.")

def publish(client):
    data = {}
    data["name"] = NAME
    data["cpu_percent"] = psutil.cpu_percent(interval=1) # val
    data["cpu_freq"] = psutil.cpu_freq() # current min max
    data["virtual_memory"] = psutil.virtual_memory() # total available percent used free
    data["swap_memory"] = psutil.swap_memory() # total used free percent sin sout
    data["disk_usage"] = psutil.disk_usage('/') # total used free percent
    data["net_io_counters"] = psutil.net_io_counters() #bytes_sent bytes_recv packets_sent packets_recv errin errout dropin dropout
    data["boot_time"] = psutil.boot_time() # val
    if sys.platform!="win32":
        data["sensors_temperatures"] = psutil.sensors_temperatures()
    client.publish(TOPIC, json.dumps(data))

def main():
    try:
        connected = False
        client = mqtt.Client(NAME)
        client.on_connect = on_connect
        #client.on_message = on_message
        client.on_disconnect = on_disconnect
        while not connected:
            try:
                client.connect(BROKER, PORT, KEEPALIVE)
                connected = True
            except:
                print("still connecting...")
            time.sleep(1)
        client.loop_start()
        while True:
            publish(client)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("KEYBOARD INTERRUPT")
    except Exception as e:
        print("OTHER EXCEPTION:", e)
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()