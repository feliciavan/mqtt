import unittest
from unittest.mock import MagicMock, patch
import json
from engine import onMessage

class TestOnMessage(unittest.TestCase):
  def setUp(self):
    self.mockClient=MagicMock()
    self.topicInput = "RE/calculateWinterSupplementInput/123"
    self.topicOutput = "RE/calculateWinterSupplementOutput/123"
    self.mockUserdata = None
  
  # Case 1: Not Eligible 
  def testNotEligible(self):
    inputData={
      "id": "test1",
      "numberOfChildren": 0,
      "familyComposition": "single",
      "familyUnitInPayForDecember": False
    }
    
    msg = MagicMock()
    msg.topic=self.topicInput
    msg.payload = json.dumps(inputData).encode()

    expectedOutput = {
      "id": "test1",
      "isEligible": False,
      "childrenAmount": 0.0,
      "baseAmount": 0.0,
      "supplementAmount": 0.0
    }

    with patch.object(self.mockClient, 'publish') as mockPublish:
      onMessage(self.mockClient, self.mockUserdata, msg)
      
      mockPublish.assert_called_once_with(self.topicOutput, json.dumps(expectedOutput))
      
  # Case 2: Single
  def testSingle(self):
      inputData={
        "id": "test2",
        "numberOfChildren": 0,
        "familyComposition": "single",
        "familyUnitInPayForDecember": True
      }
      
      msg = MagicMock()
      msg.topic = self.topicInput
      msg.payload = json.dumps(inputData).encode()
      
      expectedOutput = {
        "id": "test2",
        "isEligible": True,
        "childrenAmount": 0.0,
        "baseAmount": 60.0,
        "supplementAmount": 60.0
      }
      
      with patch.object(self.mockClient, 'publish') as mockPublish:
        onMessage(self.mockClient, self.mockUserdata, msg)
        
        mockPublish.assert_called_once_with(self.topicOutput, json.dumps(expectedOutput))

  # Case 3: Couple with no children
  def testCoupleNoChildren(self):
    inputData={
      "id": "test3",
      "numberOfChildren": 0,
      "familyComposition": "couple",
      "familyUnitInPayForDecember": True
    }
    
    msg = MagicMock()
    msg.topic = self.topicInput
    msg.payload = json.dumps(inputData).encode()
    
    expectedOutput = {
      "id": "test3",
      "isEligible": True,
      "childrenAmount": 0.0,
      "baseAmount": 120.0,
      "supplementAmount": 120.0
    }
    
    with patch.object(self.mockClient, 'publish') as mockPublish:
      onMessage(self.mockClient, self.mockUserdata, msg)
      
      mockPublish.assert_called_once_with(self.topicOutput, json.dumps(expectedOutput))
      
  # Case 4: Couple with children
  def testCoupleHasChildren(self):
    inputData={
      "id": "test4",
      "numberOfChildren": 2,
      "familyComposition": "couple",
      "familyUnitInPayForDecember": True
    }
    
    msg = MagicMock()
    msg.topic = self.topicInput
    msg.payload = json.dumps(inputData).encode()
    
    expectedOutput = {
      "id": "test4",
      "isEligible": True,
      "childrenAmount": 2.0,
      "baseAmount": 120.0,
      "supplementAmount": 160.0
    }
    
    with patch.object(self.mockClient, 'publish') as mockPublish:
      onMessage(self.mockClient, self.mockUserdata, msg)
      
      mockPublish.assert_called_once_with(self.topicOutput, json.dumps(expectedOutput))

if __name__=="__main__":
  unittest.main()