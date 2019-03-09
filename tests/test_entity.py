import unittest
from context import entity


"""
Test Cases:
1. Testing Constructor: (assertRaises)
    a. Two arguements are compulsary. Otherwise: TypeError
    b. Will only accept string values. Integers, Floats, None types 
        should raise TypeError
    c. Will not accept tabs or spaces in string values. Otherwise: ValueError
    d. Gender Should only have two values: Male or Female.
        Otherwise: ValueError
    e. Value for Mother can be: None or a string. Otherwise: ValueError
2. Testing getter methods: (assertEqual)
3. Testing setter methods: (assertRaises)
    a. Test for functionality
    b. Test for duplicates
"""


class TestEntity(unittest.TestCase):
    def testConstructor(self):
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
    
    def testGetterMethods(self):
        # create two valid entity objects. One with Mother and one without
        entity1 = entity.Entity("A", "Female")
        entity2 = entity.Entity("B", "Male", "A")
        # test getname method
        self.assertEqual(entity1.getName(), "A")
        self.assertEqual(entity2.getName(), "B")
        # test getgender method
        self.assertEqual(entity1.getGender(), "Female")
        self.assertEqual(entity2.getGender(), "Male")
        # test getfather method
        self.assertEqual(entity1.getFather(), None)
        self.assertEqual(entity2.getFather(), None)
        # test getmother method
        self.assertEqual(entity1.getMother(), None)
        self.assertEqual(entity2.getMother(), "A")
        # test getson method
        self.assertEqual(entity1.getSon(), [])
        self.assertEqual(entity2.getSon(), [])
        # test getdaughter method
        self.assertEqual(entity1.getDaughter(), [])
        self.assertEqual(entity2.getDaughter(), [])
        # test getspouse method
        self.assertEqual(entity1.getSpouse(), None)
        self.assertEqual(entity2.getSpouse(), None)
        # test isfemale method
        self.assertEqual(entity1.isFemale(), True)
        self.assertEqual(entity2.isFemale(), False)
    
    def testSetterMethods(self):
        # create two valid entity objects. One with Mother and one without
        entity1 = entity.Entity("A", "Female")

        # test set father:
        # a. Test for proper values
        self.assertRaises(TypeError, entity1.setFather, 1)
        self.assertRaises(TypeError, entity1.setFather, 1.0)
        self.assertRaises(ValueError, entity1.setFather, "A B")
        # b. Test for proper set values and duplicates
        self.assertRaises(ValueError, entity1.setFather, "A")
        entity1.setFather("C")
        self.assertEqual(entity1.getFather(), "C")

        # test set Spouse:
        # a. Test for proper values
        self.assertRaises(TypeError, entity1.setSpouse, 1)
        self.assertRaises(TypeError, entity1.setSpouse, 1.0)
        self.assertRaises(ValueError, entity1.setSpouse, "A B")
        # b. Test for proper set values and duplicates
        self.assertRaises(ValueError, entity1.setSpouse, "C")
        entity1.setSpouse("D")
        self.assertEqual(entity1.getSpouse(), "D")

        # test set Son:
        # a. Test for proper values
        self.assertRaises(TypeError, entity1.setSon, 1)
        self.assertRaises(TypeError, entity1.setSon, 1.0)
        self.assertRaises(ValueError, entity1.setSon, "A B")
        # b. Test for proper set values and duplicates
        self.assertRaises(ValueError, entity1.setSon, "D")
        entity1.setSon("E")
        self.assertRaises(ValueError, entity1.setSon, "E")
        entity1.setSon("F")
        self.assertEqual(entity1.getSon(), ["E", "F"])

        # test set Daughter:
        # a. Test for proper values
        self.assertRaises(TypeError, entity1.setDaughter, 1)
        self.assertRaises(TypeError, entity1.setDaughter, 1.0)
        self.assertRaises(ValueError, entity1.setDaughter, "A B")
        # b. Test for proper set values and duplicates
        self.assertRaises(ValueError, entity1.setDaughter, "F")
        entity1.setDaughter("G")
        self.assertRaises(ValueError, entity1.setDaughter, "G")
        entity1.setDaughter("H")
        self.assertEqual(entity1.getDaughter(), ["G", "H"])

    def testHelperMethod(self):
        pass