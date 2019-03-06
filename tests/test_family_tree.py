import unittest
from context import entity
from context import family_tree
from mock import MagicMock, patch, call, ANY


class TestFamilyTree(unittest.TestCase):
    def getMock(self):
        # CREATE THE INITIAL MOCK OBJECT AND RETURN

        # create a magicmock object
        mock = MagicMock()
        
        # Now create a mock reference of the private class variable of
        # familytree
        mock.__family_tree = family_tree.FamilyTree._FamilyTree__family_tree

        return mock

    def test_isSuitableMother(self):
        # first create an entity and set values accordingly.
        
        # a valid entity
        entity1 = entity.Entity("A", "Female")
        entity1.setSpouse("B")

        # an invalid entity with no spouse
        entity2 = entity.Entity("C", "Female")

        # an invalid entity with wrong gender
        entity3 = entity.Entity("D", "Male")

        mock = self.getMock()
        
        # Now create a mock of the method you want to test
        mock.test_isSuitableMother = family_tree.FamilyTree.isSuitableMother
        
        # set values to the family_tree variable
        mock.__family_tree['A'] = entity1
        mock.__family_tree['B'] = entity2
        mock.__family_tree['D'] = entity3
        
        # now test with assert
        self.assertEqual(mock.test_isSuitableMother('A'), True)
        self.assertEqual(mock.test_isSuitableMother('B'), "PERSON_NOT_MARRIED")
        self.assertEqual(mock.test_isSuitableMother('D'), "CHILD_ADDITION_FAILED")




