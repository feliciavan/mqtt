import unittest
from unittest.mock import MagicMock
from engine import onConnect
import os
from dotenv import load_dotenv

# Get the environment variables, which can be self-specified or assignment-specified
load_dotenv()
TopicInput = os.getenv("TopicInput")

class TestOnConnect(unittest.TestCase):
  def setUp(self):
    self.mockClient = MagicMock()
    self.topicInput = TopicInput + "#"
    self.mockUserdata = None
    self.flags = None
    self.properties = None
    
  def testSubscribeSuccess(self):
    rc = 0
    onConnect(self.mockClient, self.mockUserdata, self.flags, rc, self.properties)
    self.mockClient.subscribe.assert_called_once_with(self.topicInput)
    
  def testSubscribeRefuse(self):
    rc = 1
    onConnect(self.mockClient, self.mockUserdata, self.flags, rc, self.properties)
    self.mockClient.subscribe.assert_called_once_with(self.topicInput)
    
if __name__=="__main__":
  unittest.main()
    