import paho.mqtt.client as mqtt
import json
import time
from loguru import logger
import os
from dotenv import load_dotenv

# Get the environment variables, which can be self-specified or assignment-specified
load_dotenv()
TopicInput = os.getenv("TopicInput") 
TopicOutput = os.getenv("TopicOutput") 

# Log file position
logger.add("log/webapp.log")

# MQTT broker
Broker = "test.mosquitto.org"
Port = 1883

# Mock data, for 4 cases: not eligible, single, couple no child, couple with children
def publish_message(client):
  
  # Case 1: not eligible
  payloadNotEligible = {
    "id": "id-not-eligible",
    "numberOfChildren": 0,  
    "familyComposition": "single",  
    "familyUnitInPayForDecember": False 
  }

  topicNotEligible = TopicInput + "topic-id-not-eligible" 
  client.publish(topicNotEligible, json.dumps(payloadNotEligible))
  logger.info(f"Broker: Published to {topicNotEligible}:{json.dumps(payloadNotEligible)}")
   
   # Wait for engine to receive
  logger.info("Broker waits for 5s")
  time.sleep(5)
  logger.info("Broker: done waiting") 
  
  # Case 2: Single with no children
  payloadSingleNoChildren = {
    "id": "id-single-no-children",
    "numberOfChildren": 0,  
    "familyComposition": "single",  
    "familyUnitInPayForDecember": True 
  }

  topicSingleNoChildren = TopicInput + "topic-id-single-no-children" 
  client.publish(topicSingleNoChildren, json.dumps(payloadSingleNoChildren))
  logger.info(f"Broker: Published to {topicSingleNoChildren}:{json.dumps(payloadSingleNoChildren)}")
  
  logger.info("Broker waits for 5s")
  time.sleep(5)
  logger.info("Broker: done waiting")
  
  # Case 3: Couple no children
  payloadCoupleNoChildren = {
    "id": "id-copule-no-children",
    "numberOfChildren": 0,  
    "familyComposition": "couple",  
    "familyUnitInPayForDecember": True 
  }

  topicCoupleNoChild = TopicInput + "topic-id-couple-no-children" 
  client.publish(topicCoupleNoChild, json.dumps(payloadCoupleNoChildren))
  logger.info(f"Broker: Published to {topicCoupleNoChild}:{json.dumps(payloadCoupleNoChildren)}")

  # Wait for engine to receive
  logger.info("Broker waits for 5s")
  time.sleep(5)
  logger.info("Broker: done waiting")
  
  # Case 4: Couple with children
  payloadCoupleWithChildren = {
    "id": "id-couple-with-children",
    "numberOfChildren": 2,  
    "familyComposition": "couple",  
    "familyUnitInPayForDecember": True 
  }

  topicCoupleWithChildren = TopicInput + "topic-id-couple-with-children" 
  client.publish(topicCoupleWithChildren, json.dumps(payloadCoupleWithChildren))
  logger.info(f"Broker: Published to {topicCoupleWithChildren}:{json.dumps(payloadCoupleWithChildren)}")
  
  # Wait for engine to receive
  logger.info("Broker waits for 5s")
  time.sleep(5)
  logger.info("Broker: done waiting")
  
  # Case 5: Single with children
  payloadSingleWithChildren = {
    "id": "id-single-with-children",
    "numberOfChildren": 3,  
    "familyComposition": "single",  
    "familyUnitInPayForDecember": True 
  }

  topicSingleWithChildren = TopicInput + "topic-id-single-with-children" 
  client.publish(topicSingleWithChildren, json.dumps(payloadSingleWithChildren))
  logger.info(f"Broker: Published to {topicSingleWithChildren}:{json.dumps(payloadSingleWithChildren)}")  

  # Wait for engine to receive
  logger.info("Broker waits for 5s")
  time.sleep(5)
  logger.info("Broker: done waiting")
  
  # Case 6: Invalid topic ID
  topicInvalidTopicID = TopicInput 
  client.publish(topicInvalidTopicID, None)
  logger.info(f"Broker: Published to {topicInvalidTopicID}:None")
  
  # Wait for engine to receive
  logger.info("Broker waits for 5s")
  time.sleep(5)
  logger.info("Broker: done waiting")
  
  # Case 7: Invalid payload
  payloadInvalid = "123" 

  topicInvalidPayload = TopicInput + "topic-invalid-payload" 
  client.publish(topicInvalidPayload, json.dumps(payloadInvalid))
  logger.info(f"Broker: Published to {topicInvalidPayload}:{json.dumps(payloadInvalid)}")  

  # Wait for engine to receive
  logger.info("Broker waits for 5s")
  time.sleep(5)
  logger.info("Broker: done waiting")
  
  # Case 8: Missing fields in input data 
  payloadMissingFieldsInInputdata = {
    "id": "id-missing-fields",
    "numberOfChildren": 3,  
  }

  topicMissingFieldsOfInputdata = TopicInput + "topic-id-missing-fields" 
  client.publish(topicMissingFieldsOfInputdata, json.dumps(payloadMissingFieldsInInputdata))
  logger.info(f"Broker: Published to {topicMissingFieldsOfInputdata}:{json.dumps(payloadMissingFieldsInInputdata)}")  

  # Wait for engine to receive
  logger.info("Broker waits for 5s")
  time.sleep(5)
  logger.info("Broker: done waiting")
  
  # Case 9: Invalid input value
  payloadInvalidInputValue = {
      "id": "id-invalid-input-value",
      "numberOfChildren": 3,
      "familyComposition": "Christmas",
      "familyUnitInPayForDecember": True
  }

  topicInvalidInputValue = TopicInput + "topic-id-invalid-input-value" 
  client.publish(topicInvalidInputValue, json.dumps(payloadInvalidInputValue))
  logger.info(f"Broker: Published to {topicInvalidInputValue}:{json.dumps(payloadInvalidInputValue)}")  

def on_connect(client, userdata, flags, rc, properties):
  logger.info(f"Broker: connected with result code {rc}")
  client.subscribe(TopicOutput + "#")
  
  publish_message(client)

def on_message(client, userdata, msg):
  logger.info("Broker Received: " + msg.topic+" "+str(msg.payload))

def main():
  mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
  mqttc.on_connect = on_connect
  mqttc.on_message = on_message
  mqttc.connect(Broker, Port, 60)
  mqttc.loop_forever()
  
if __name__=="__main__":
  main()
