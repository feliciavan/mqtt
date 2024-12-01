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
  
  # Get the topic ID. If there is no topicID, log error, return
  topicParts = msg.topic.split('/')
  topicID = topicParts[-1]
  if not (len(topicParts) == 3 and len(topicID) != 0):
    logger.error("Invalid topic: " + msg.topic)
    return
  
  # Get the info from web app
  try:
    inputData = json.loads(msg.payload.decode())
  except Exception as e:
    logger.error(f"Error when decoding payload: {e}")
    return

  # Validate fields
  requiredFields = ["id", "familyUnitInPayForDecember", "numberOfChildren", "familyComposition", "familyUnitInPayForDecember"]
  missingFields = [field for field in requiredFields if field not in inputData]
  
  if missingFields:
    logger.error(f"Missing required fields in input data: {missingFields}")
    return

  # Prepare output data
  outputData = {}

  outputData["id"] = inputData.get("id")
  outputData["isEligible"] = inputData.get("familyUnitInPayForDecember")
  outputData["childrenAmount"] = float(inputData.get("numberOfChildren"))

  if inputData.get("familyUnitInPayForDecember") is False:
    outputData["baseAmount"] = 0.0
    outputData["supplementAmount"] = 0.0
  elif inputData.get("familyUnitInPayForDecember") is True and inputData.get("familyComposition") == "single" and outputData["childrenAmount"] == 0:
    outputData["baseAmount"] = 60.0
    outputData["supplementAmount"] = 60.0
  elif inputData.get("familyUnitInPayForDecember") is True and inputData.get("familyComposition") == "couple" and outputData["childrenAmount"] == 0:
    outputData["baseAmount"] = 120.0
    outputData["supplementAmount"] = 120.0
  elif inputData.get("familyUnitInPayForDecember") is True and outputData["childrenAmount"] != 0 and (inputData.get("familyComposition") == "single" or inputData.get("familyComposition") == "couple"):
    outputData["baseAmount"] = 120.0
    outputData["supplementAmount"] = inputData.get("numberOfChildren") * 20.0 + outputData["baseAmount"]
  else:
    logger.error("Invalid input value.")
    return

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

