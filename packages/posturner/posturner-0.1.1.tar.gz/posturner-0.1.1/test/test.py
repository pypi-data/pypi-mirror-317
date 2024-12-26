import unittest
from posturner import trans_universal_pos
class TestStringMethods(unittest.TestCase):
    def test_trans_universal_pos(self):
        result = trans_universal_pos("adjective")
        assert result == "ADJ"