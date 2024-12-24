import unittest
from zeptum import add, inc

class Test(unittest.TestCase):
    def test_add_oper(self):
        self.assertEqual(add(5, 5), 10)
        self.assertEqual(add(-10, 5), -5)
    
    def test_inc_oper(self):
        self.assertEqual(inc(5), 2)
        self.assertEqual(inc(10), 5)

if __name__ == "__main__":
    unittest.main()