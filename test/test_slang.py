import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

class SlangTestCase(unittest.TestCase):

    def test_init(self):
        id = "123"
        slang = Slang(id)
        self.assertEqual(slang.id, id)

if __name__ == '__main__':
    unittest.main()
