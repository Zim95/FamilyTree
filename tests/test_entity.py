import unittest
from context import entity


"""
Test Cases:
1. Testing Constructor:
    a. Two arguements are compulsary. Otherwise: TypeError
    b. Will only accept string values. Integers, Floats, None types 
        should raise TypeError
    c. Will not accept tabs or spaces in string values. Otherwise: ValueError
    d. Gender Should only have two values: Male or Female. Otherwise: ValueError
    e. Value for Mother can be: None or a string. Otherwise: ValueError
2. Error if the data members are accessed publicly
3. Root entity creation is only allowed in the Setup (Entities with no parents)
4. Proper values are to be entered into setter methods
5. Improper method name should raise an error
"""


class TestEntity(unittest.TestCase):
    def test_constructor(self):
        # raise Type Error upon only one arguement
        self.assertRaises(TypeError, entity.Entity, "1 a")
        # raise type error for integer, float or None inputs
        self.assertRaises(TypeError, entity.Entity, 1, 2)
        self.assertRaises(TypeError, entity.Entity, 1.0, 2.0)
        self.assertRaises(TypeError, entity.Entity, None, None)
        # should raise value error upon encountering spaces or tabs in strings
        self.assertRaises(ValueError, entity.Entity, "1 a", "1 b")
        # gender should only have two values: Male or Female
        self.assertRaises(ValueError, entity.Entity, "1a", "1b")
        # value for mother can be None or A valid String
        self.assertRaises(ValueError, entity.Entity, "1a", "Male", "Q S")
    
    def testPublicAccess(self):
        # raise Attribute error if data members are accesssed publicly
        self.assertRaise(AttributeError, entity.Entity.__name)