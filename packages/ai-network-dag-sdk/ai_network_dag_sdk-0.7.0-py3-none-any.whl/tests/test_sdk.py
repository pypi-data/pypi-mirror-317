import unittest
from AINetworkDagSdk import AINetworkDagSdk

class TestAINetworkDagSdk(unittest.TestCase):
    def test_initialization(self):
        sdk = AINetworkDagSdk("localhost:50051")
        self.assertIsNotNone(sdk)

if __name__ == "__main__":
    unittest.main()
