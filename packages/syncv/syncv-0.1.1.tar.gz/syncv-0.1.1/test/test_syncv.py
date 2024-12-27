# tests/test_sync.py

import unittest
from syncv.core import initialize, list_contents, clear_contents

class TestSync(unittest.TestCase):

    def test_initialize(self):
        code = initialize()
        self.assertIsNotNone(code)
        self.assertEqual(len(code), 36)  # UUID长度

    def test_list_contents_empty(self):
        contents = list_contents()
        self.assertEqual(contents, [])

    def test_clear_contents(self):
        clear_contents()
        contents = list_contents()
        self.assertEqual(contents, [])

if __name__ == '__main__':
    unittest.main()