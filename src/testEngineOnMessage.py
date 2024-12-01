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
      "id": "id-not-eligible",
      "numberOfChildren": 0,
      "familyComposition": "single",
      "familyUnitInPayForDecember": False
    }
    
    msg = MagicMock()
    msg.topic=self.topicInput
    msg.payload = json.dumps(inputData).encode()

    expectedOutput = {
      "id": "id-not-eligible",
      "isEligible": False,
      "childrenAmount": 0.0,
      "baseAmount": 0.0,
      "supplementAmount": 0.0
    }

    with patch.object(self.mockClient, 'publish') as mockPublish:
      onMessage(self.mockClient, self.mockUserdata, msg)
      
      mockPublish.assert_called_once_with(self.topicOutput, json.dumps(expectedOutput))
      
  # Case 2: Single with no children
  def testSingle(self):
      inputData={
        "id": "id-single-no-children",
        "numberOfChildren": 0,
        "familyComposition": "single",
        "familyUnitInPayForDecember": True
      }
      
      msg = MagicMock()
      msg.topic = self.topicInput
      msg.payload = json.dumps(inputData).encode()
      
      expectedOutput = {
        "id": "id-single-no-children",
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
      "id": "id-copule-no-children",
      "numberOfChildren": 0,
      "familyComposition": "couple",
      "familyUnitInPayForDecember": True
    }
    
    msg = MagicMock()
    msg.topic = self.topicInput
    msg.payload = json.dumps(inputData).encode()
    
    expectedOutput = {
      "id": "id-copule-no-children",
      "isEligible": True,
      "childrenAmount": 0.0,
      "baseAmount": 120.0,
      "supplementAmount": 120.0
    }
    
    with patch.object(self.mockClient, 'publish') as mockPublish:
      onMessage(self.mockClient, self.mockUserdata, msg)
      
      mockPublish.assert_called_once_with(self.topicOutput, json.dumps(expectedOutput))
      
  # Case 4: Couple with children
  def testCoupleWithChildren(self):
    inputData={
      "id": "id-couple-with-children",
      "numberOfChildren": 2,
      "familyComposition": "couple",
      "familyUnitInPayForDecember": True
    }
    
    msg = MagicMock()
    msg.topic = self.topicInput
    msg.payload = json.dumps(inputData).encode()
    
    expectedOutput = {
      "id": "id-couple-with-children",
      "isEligible": True,
      "childrenAmount": 2.0,
      "baseAmount": 120.0,
      "supplementAmount": 160.0
    }
    
    with patch.object(self.mockClient, 'publish') as mockPublish:
      onMessage(self.mockClient, self.mockUserdata, msg)
      
      mockPublish.assert_called_once_with(self.topicOutput, json.dumps(expectedOutput))
  
  # Case 5: Single with children
  def testSingleWithChildren(self):
    inputData={
      "id": "id-single-with-children",
      "numberOfChildren": 3,
      "familyComposition": "single",
      "familyUnitInPayForDecember": True
    }
    
    msg = MagicMock()
    msg.topic = self.topicInput
    msg.payload = json.dumps(inputData).encode()
    
    expectedOutput = {
      "id": "id-single-with-children",
      "isEligible": True,
      "childrenAmount": 3.0,
      "baseAmount": 120.0,
      "supplementAmount": 180.0
    }
    
    with patch.object(self.mockClient, 'publish') as mockPublish:
      onMessage(self.mockClient, self.mockUserdata, msg)
      
      mockPublish.assert_called_once_with(self.topicOutput, json.dumps(expectedOutput))

if __name__=="__main__":
  unittest.main()