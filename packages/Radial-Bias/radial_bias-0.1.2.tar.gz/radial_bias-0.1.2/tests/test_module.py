import unittest
from Radial_bias_Raunak_gola import module

class TestAddFunction(unittest.TestCase):
    def test_add(self):
        self.assertEqual(module.add(1, 2), 3)
        self.assertEqual(module.add(-1, 1), 0)
        self.assertEqual(module.add(-1, -1), -2)

if __name__ == '__main__':
    unittest.main()
