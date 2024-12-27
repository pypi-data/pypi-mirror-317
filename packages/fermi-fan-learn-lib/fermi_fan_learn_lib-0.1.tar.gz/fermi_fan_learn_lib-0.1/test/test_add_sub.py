import unittest
from fermi_learn_lib import add, sub
class TestAddSub(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-2, 3), 1)
        self.assertEqual(add(-2, -3), -5)
    def test_sub(self):
        self.assertEqual(sub(2, 3), -1)
        self.assertEqual(sub(-2, 3), -5)
        self.assertEqual(sub(-2, -3), 1)

if __name__ == '__main__':
    unittest.main()