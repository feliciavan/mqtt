import unittest
from unittest.mock import MagicMock
from engine import onConnect

class TestOnConnect(unittest.TestCase):
  def setUp(self):
    self.mockClient = MagicMock()
    self.topicInput = "RE/calculateWinterSupplementInput/#"
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
    