# A Rules Engine with MQTT Broker and Winter Supplement Web App

- [A Rules Engine with MQTT Broker and Winter Supplement Web App](#a-rules-engine-with-mqtt-broker-and-winter-supplement-web-app)
  - [Software Language](#software-language)
  - [Prerequisites](#prerequisites)
  - [System Structure](#system-structure)
  - [How to run the Engine](#how-to-run-the-engine)
    - [Download project](#download-project)
    - [Build the Docker images](#build-the-docker-images)
    - [Start the containers](#start-the-containers)
      - [Self-specified](#self-specified)
        - [Check Docker logs](#check-docker-logs)
      - [Assignment-specified](#assignment-specified)
        - [Check Docker logs](#check-docker-logs-1)
  - [Unit Test](#unit-test)
    - [Unit Test for `onConnect`](#unit-test-for-onconnect)
      - [Checklist](#checklist)
    - [Unit Test for `onMessage`](#unit-test-for-onmessage)
      - [Checklist](#checklist-1)


## Software Language

This project is written in Python.

## Prerequisites

This project runs inside Docker. Please install Docker and Docker Compose in your environment. 

## System Structure

The system structure is shown as follows.

```mermaid
graph LR
  A["Winter Supplement Web App (WSWA)"] -->|Publish BRE/calculateWinterSupplementInput/| B[MQTT Broker]
  B --> |Publish BRE/calculateWinterSupplementInput/| C[Engine]
  C --> |Subscribe BRE/calculateWinterSupplementInput/| B
  C -.-> |Publish BRE/calculateWinterSupplementOutput/| B
  B -.-> |Publish BRE/calculateWinterSupplementOutput/| A
  A -.-> |Subscribe BRE/calculateWinterSupplementOutput/| B
```

This system consists of the Winter Supplement Web App (WSWA), an MQTT broker and the rules engine, where the engine is my main develop content. In the WSWA, users input their data, and click submit button. WSWA works as a MQTT client and publishes this message of user input to the MQTT broker. The topic of this MQTT message is `BRE/calculateWinterSupplementInput/`. The engine also works as a MQTT client and subscribes to this topic to receive this message. After receiving the message, the engine processes the data based on the rules of winter supplement. Then the engine publishes the calculated data to the topic `Subscribe BRE/calculateWinterSupplementOutput/`. And the WSWA subscribes to this topic to get the message.

> In order to develop the engine more conveniently, I made the mock version of the WSWA. The MQTT topics are different from the assignment-specified ones. Because the MQTT broker is the same to all developers, I don't want to mix my design with others. 

> In order to deploy and run the project more easily, both the engine and the mock WSWA run inside the Docker containers.

## How to run the Engine

### Download project

```cmd
git clone https://github.com/feliciavan/mqtt.git
```

  
In the `mqtt` directory, modify the content in `.env`, which contains the environment variables about MQTT topics. The content is:

```cmd
TopicInput=RE/calculateWinterSupplementInput/
TopicOutput=RE/calculateWinterSupplementOutput/
```

where it is self-specified in order to separate with the assignment-specified ones. I can set it to the assignment-specified ones, which are

```cmd
TopicInput=BRE/calculateWinterSupplementInput/
TopicOutput=BRE/calculateWinterSupplementOutput/
```

Under this circumstance, I do not need to run the container of the mock WSWA. I can directly use the existing one.

### Build the Docker images

```cmd
docker compose build
```

Check the Docker images

```cmd
docker image ls
```

The output is:

```cmd
REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
mqtt-webapp   latest    301bc19e8d42   4 seconds ago   133MB
mqtt-engine   latest    88d10be74dba   4 seconds ago   133MB
```

where `mqtt-engine` is the engine I developed. `mqtt-webapp` is a mock version of the WSWA. This mock WSWA will publish 5 messages for 5 different cases, which are:

- Case 1: Not eligible
  - Topic: `RE/calculateWinterSupplementInput/topic-id-not-eligible`
  - Message:
    ```json
    {
      "id": "id-not-eligible",
      "numberOfChildren": 0,
      "familyComposition": "single",
      "familyUnitInPayForDecember": false
    }
    ```

- Case 2: Single with no children
  - Topic: `RE/calculateWinterSupplementInput/topic-id-single-no-children`
  - Message:
    ```json
    {
      "id": "id-single-no-children",
      "numberOfChildren": 0,
      "familyComposition": "single",
      "familyUnitInPayForDecember": true
    }
    ```

- Case 3: Couple with no children
  - Topic: `RE/calculateWinterSupplementInput/topic-id-couple-no-children`
  - Message:
    ```json
    {
      "id": "id-couple-no-children",
      "numberOfChildren": 0,
      "familyComposition": "couple",
      "familyUnitInPayForDecember": true
    }
    ```
  
- Case 4: Couple with children
  - Topic: `RE/calculateWinterSupplementInput/topic-id-couple-with-children`
  - Message:
    ```json
    {
      "id": "id-couple-with-children",
      "numberOfChildren": 2,
      "familyComposition": "couple",
      "familyUnitInPayForDecember": true
    }
    ```
  
- Case 5: Single with children
  - Topic: `RE/calculateWinterSupplementInput/topic-id-single-with-children`
  - Message:
    ```json
    {
      "id": "id-single-with-children",
      "numberOfChildren": 3,
      "familyComposition": "single",
      "familyUnitInPayForDecember": true
    }
    ```

Here, I set the topic ID to be the specific case name for evident clarity in the logs. I can also set the topic ID to be the randome UUID.

### Start the containers

#### Self-specified

Set the `.env` to self-specified MQTT topics:

```cmd
TopicInput=RE/calculateWinterSupplementInput/
TopicOutput=RE/calculateWinterSupplementOutput/
```

Start the containers of the engine and the webapp (WSWA):

```cmd
docker compose up -d
```

Check the Docker containers

```cmd
docker ps
```

The output will be

```cmd
CONTAINER ID   IMAGE         COMMAND              CREATED         STATUS         PORTS     NAMES
b084e7d16cfe   mqtt-engine   "python engine.py"   2 seconds ago   Up 2 seconds             engine
ee762992cd59   mqtt-webapp   "python webApp.py"   2 seconds ago   Up 2 seconds             webapp
```

where `webapp` is the mock version of the WSWA and `engine` is the rules engine I developed.

##### Check Docker logs

Check the logs of the engine container:

```cmd
docker logs engine
```

Check the logs of the webapp container:

```cmd
docker logs webapp
```

The logs are located outside the Docker containers as well. The location is mqtt/log, where `engine.log` is the log of the engine container, and `webapp.log` is the log of the webapp container.

#### Assignment-specified

If the previous containers are running, stop them:

```cmd
docker stop webapp engine
```

Set the `.env` to assginment-specified MQTT topics:

```cmd
TopicInput=BRE/calculateWinterSupplementInput/
TopicOutput=BRE/calculateWinterSupplementOutput/
```

At this time, the webapp container is no longer needed, since I am using the existing one, i.e., the online WSWA.

Only start the container of the engine:

```cmd
docker compose up engine -d
```

Check the Docker containers

```cmd
docker ps
```

The output will be

```cmd
CONTAINER ID   IMAGE         COMMAND              CREATED         STATUS         PORTS     NAMES
dbdf113b65d5   mqtt-engine   "python engine.py"   3 seconds ago   Up 2 seconds             engine
```

##### Check Docker logs

Check the logs of the engine:

```cmd
docker logs engine
```

## Unit Test

The code of the engine is in file `engine.py`. It contains 2 callback functions, which are `onConnect` and `onMessage`. The are related to `on_connect` and `on_message` of the MQTT client, respectively. I made 2 unit tests for these 2 functions.

Go inside the Docker container `engine`, to run the unit tests.

```cmd
docker exec -it engine bash
```

In the `/app` directory, `testEngineOnMessage.py` is the unit test for `onMessage`, and `testEngineOnConnect.py` is the unit test for `onConnect`.

### Unit Test for `onConnect`

#### Checklist

- Connection reason code is 0, denoting success. 
- Connection reason code is 1, denoting refuse.

To test `onConnect` function in `engine.py`, run

```cmd
python -m unittest -v testEngineOnConnect.py
```

The test results are:

```cmd
testSubscribeRefuse (testEngineOnConnect.TestOnConnect.testSubscribeRefuse) ... 2024-11-30 15:58:04.064 | INFO     | engine:onConnect:20 - Engine: Connected with result code 1
ok
testSubscribeSuccess (testEngineOnConnect.TestOnConnect.testSubscribeSuccess) ... 2024-11-30 15:58:04.066 | INFO     | engine:onConnect:20 - Engine: Connected with result code 0
ok

----------------------------------------------------------------------
Ran 2 tests in 0.005s

OK
```

### Unit Test for `onMessage`

#### Checklist

- Not eligible
- Single with no children
- Couple with no childre
- Couple with children 
- Single with children
- Invalid topic
- Invalid topic ID 
- Invalid message payload
- Missing fields in message payload

To test `onMessage` function in `engine.py`, run

```cmd
python -m unittest -v testEngineOnMessage.py
```

The test results are:

```cmd
testCoupleNoChildren (testEngineOnMessage.TestOnMessage.testCoupleNoChildren) ... 2024-11-30 19:13:15.550 | INFO     | engine:onMessage:24 - Engine Received: BRE/calculateWinterSupplementInput/unittest b'{"id": "id-copule-no-children", "numberOfChildren": 0, "familyComposition": "couple", "familyUnitInPayForDecember": true}'
2024-11-30 19:13:15.551 | INFO     | engine:onMessage:72 - Engine Published to BRE/calculateWinterSupplementOutput/unittest: {'id': 'id-copule-no-children', 'isEligible': True, 'childrenAmount': 0.0, 'baseAmount': 120.0, 'supplementAmount': 120.0}
ok
testCoupleWithChildren (testEngineOnMessage.TestOnMessage.testCoupleWithChildren) ... 2024-11-30 19:13:15.553 | INFO     | engine:onMessage:24 - Engine Received: BRE/calculateWinterSupplementInput/unittest b'{"id": "id-couple-with-children", "numberOfChildren": 2, "familyComposition": "couple", "familyUnitInPayForDecember": true}'
2024-11-30 19:13:15.553 | INFO     | engine:onMessage:72 - Engine Published to BRE/calculateWinterSupplementOutput/unittest: {'id': 'id-couple-with-children', 'isEligible': True, 'childrenAmount': 2.0, 'baseAmount': 120.0, 'supplementAmount': 160.0}
ok
testFieldsOfInputdata (testEngineOnMessage.TestOnMessage.testFieldsOfInputdata) ... 2024-11-30 19:13:15.554 | INFO     | engine:onMessage:24 - Engine Received: BRE/calculateWinterSupplementInput/unittest b'{"id": "id-single-with-children", "numberOfChildren": 3}'
2024-11-30 19:13:15.555 | ERROR    | engine:onMessage:45 - Missing required fields in input data: ['familyUnitInPayForDecember', 'familyComposition', 'familyUnitInPayForDecember']
ok
testInvalidJSONPayload (testEngineOnMessage.TestOnMessage.testInvalidJSONPayload) ... 2024-11-30 19:13:15.556 | INFO     | engine:onMessage:24 - Engine Received: BRE/calculateWinterSupplementInput/unittest abc
2024-11-30 19:13:15.556 | ERROR    | engine:onMessage:37 - Error when decoding payload: 'str' object has no attribute 'decode'
ok
testInvalidTopic (testEngineOnMessage.TestOnMessage.testInvalidTopic) ... 2024-11-30 19:13:15.557 | INFO     | engine:onMessage:24 - Engine Received: abc b'{}'
2024-11-30 19:13:15.558 | ERROR    | engine:onMessage:30 - Invalid topic: abc
ok
testInvalidTopicID (testEngineOnMessage.TestOnMessage.testInvalidTopicID) ... 2024-11-30 19:13:15.559 | INFO     | engine:onMessage:24 - Engine Received: abc/edf/ b'{}'
2024-11-30 19:13:15.559 | ERROR    | engine:onMessage:30 - Invalid topic: abc/edf/
ok
testNotEligible (testEngineOnMessage.TestOnMessage.testNotEligible) ... 2024-11-30 19:13:15.560 | INFO     | engine:onMessage:24 - Engine Received: BRE/calculateWinterSupplementInput/unittest b'{"id": "id-not-eligible", "numberOfChildren": 0, "familyComposition": "single", "familyUnitInPayForDecember": false}'
2024-11-30 19:13:15.561 | INFO     | engine:onMessage:72 - Engine Published to BRE/calculateWinterSupplementOutput/unittest: {'id': 'id-not-eligible', 'isEligible': False, 'childrenAmount': 0.0, 'baseAmount': 0.0, 'supplementAmount': 0.0}
ok
testSingleNoChildren (testEngineOnMessage.TestOnMessage.testSingleNoChildren) ... 2024-11-30 19:13:15.563 | INFO     | engine:onMessage:24 - Engine Received: BRE/calculateWinterSupplementInput/unittest b'{"id": "id-single-no-children", "numberOfChildren": 0, "familyComposition": "single", "familyUnitInPayForDecember": true}'
2024-11-30 19:13:15.563 | INFO     | engine:onMessage:72 - Engine Published to BRE/calculateWinterSupplementOutput/unittest: {'id': 'id-single-no-children', 'isEligible': True, 'childrenAmount': 0.0, 'baseAmount': 60.0, 'supplementAmount': 60.0}
ok
testSingleWithChildren (testEngineOnMessage.TestOnMessage.testSingleWithChildren) ... 2024-11-30 19:13:15.565 | INFO     | engine:onMessage:24 - Engine Received: BRE/calculateWinterSupplementInput/unittest b'{"id": "id-single-with-children", "numberOfChildren": 3, "familyComposition": "single", "familyUnitInPayForDecember": true}'
2024-11-30 19:13:15.565 | INFO     | engine:onMessage:72 - Engine Published to BRE/calculateWinterSupplementOutput/unittest: {'id': 'id-single-with-children', 'isEligible': True, 'childrenAmount': 3.0, 'baseAmount': 120.0, 'supplementAmount': 180.0}
ok

----------------------------------------------------------------------
Ran 9 tests in 0.016s

OK
```
