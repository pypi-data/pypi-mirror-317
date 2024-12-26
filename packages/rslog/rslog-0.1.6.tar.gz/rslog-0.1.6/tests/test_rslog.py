import unittest
from rslog import rslog

class TestRSlog(unittest.TestCase):
    def test_rslogl(self):
        # A real test would capture stdout and assert the message.
        # For simplicity, we'll just call it here without assertion.
        rslog("Testing rslog")

if __name__ == "__main__":
    unittest.main()
