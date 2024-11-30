import paho.mqtt.client as mqtt
import json
from loguru import logger
import os
from dotenv import load_dotenv

# Get the environment variables, which can be self-specified or assignment-specified.
load_dotenv()
TopicInput = os.getenv("TopicInput") 
TopicOutput = os.getenv("TopicOutput")

# Log file position
logger.add("log/engine.log")

# MQTT broker
Broker = "test.mosquitto.org"
Port = 1883

def onConnect(client, userdata, flags, rc, properties):
  logger.info(f"Engine: Connected with result code {rc}")
  client.subscribe(TopicInput + "#")

def onMessage(client, userdata, msg):
  logger.info("Engine Received: " + msg.topic+" "+str(msg.payload))

  # Get the info from web app
  inputData = json.loads(msg.payload.decode())
  
  # Get the topic ID
  topicID = msg.topic.split('/')[-1]

  # Prepare output data
  outputData = {}

  outputData["id"] = inputData.get("id")
  outputData["isEligible"] = inputData.get("familyUnitInPayForDecember")
  outputData["childrenAmount"] = float(inputData.get("numberOfChildren"))

  if inputData.get("familyUnitInPayForDecember") is False:
    outputData["baseAmount"] = 0.0
    outputData["supplementAmount"] = 0.0

  if inputData.get("familyUnitInPayForDecember") and inputData.get("familyComposition") == "single":
    outputData["baseAmount"] = 60.0
    outputData["supplementAmount"] = 60.0

  if inputData.get("familyUnitInPayForDecember") and inputData.get("familyComposition") == "couple":
    outputData["baseAmount"] = 120.0
    outputData["supplementAmount"] = inputData.get("numberOfChildren") * 20.0 + outputData["baseAmount"]

  outputTopic = f"{TopicOutput}{topicID}"

  # Publish to MQTT broker
  client.publish(outputTopic, json.dumps(outputData))
  logger.info(f"Engine Published to {outputTopic}: {outputData}")


def main():
  client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
  client.on_connect = onConnect
  client.on_message = onMessage

  client.connect(Broker, Port, 60)

  client.loop_forever()

if __name__=="__main__":
  main()

