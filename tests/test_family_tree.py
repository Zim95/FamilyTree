import unittest
from context import entity
from context import family_tree
from mock import MagicMock, patch, call, ANY


class TestFamilyTree(unittest.TestCase):
    @patch('test_family_tree.entity.Entity')
    def getMock(self, MockEntity):
        # CREATE THE INITIAL MOCK OBJECT AND RETURN

        # create a magicmock object
        mock = MagicMock()

        # Now create a mock reference of the private class variable of
        # familytree
        mock.__family_tree = family_tree.FamilyTree._FamilyTree__family_tree

        # for entity object related tests
        mock.entity = MockEntity()

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

    def test_isSuitableSpouse(self):
        mock = self.getMock()
        
        mock.test_isSuitableSpouse = family_tree.FamilyTree.isSuitableSpouse

        mock.isSibling = family_tree.FamilyTree.isSibling
        # now set the value of getgender and isUnmarried
        # and test the results

        # a. CASE: ACCEPTED
        # NOTE: side effects are just a way of providing multiple values
        #       to a function. One value is used as return value for one call.
        mock.return_value.isSibling.return_value = False
        mock.entity.getGender.side_effect = ["Male", "Female"]
        mock.entity.isUnmarried.side_effect = [True, True]
        mock.entity.getMother.side_effect = ["Blah", "Baka"]
        mock.entity.getFather.side_effect = ["Bruh", "Blyat"]
       
        # testing the instance of entity
        # print(vars(mock.entity1))
        # print(mock.entity.getGender()) # calling this will use up a side effect. So DO NOT
        
        mock.__family_tree["A"] = mock.entity
        mock.__family_tree["B"] = mock.entity

        self.assertEqual(mock.test_isSuitableSpouse('A', 'B'), True)

        # b. CASE: REJECTED (Unexpected behavior. i.e Same mother, different father)
        # NOTE: side effects are just a way of providing multiple values
        #       to a function. One value is used as return value for one call.
        mock.return_value.isSibling.return_value = False
        mock.entity.getGender.side_effect = ["Male", "Female"]
        mock.entity.isUnmarried.side_effect = [True, True]
        mock.entity.getMother.side_effect = ["Blah", "Blah"]
        mock.entity.getFather.side_effect = ["Blah", "Bllleh"]
       
        # testing the instance of entity
        # print(vars(mock.entity1))
        # print(mock.entity.getGender()) # calling this will use up a side effect. So DO NOT
        
        mock.__family_tree["A"] = mock.entity
        mock.__family_tree["B"] = mock.entity

        self.assertRaises(ValueError, mock.test_isSuitableSpouse, 'A', 'B')

        # c. CASE: REJECTED (Unexpected behavior. i.e Same father, different mother)
        # NOTE: side effects are just a way of providing multiple values
        #       to a function. One value is used as return value for one call.
        mock.return_value.isSibling.return_value = False
        mock.entity.getGender.side_effect = ["Male", "Female"]
        mock.entity.isUnmarried.side_effect = [True, True]
        mock.entity.getMother.side_effect = ["Blah", "Bleh"]
        mock.entity.getFather.side_effect = ["Blah", "Blah"]
       
        # testing the instance of entity
        # print(vars(mock.entity1))
        # print(mock.entity.getGender()) # calling this will use up a side effect. So DO NOT
        
        mock.__family_tree["A"] = mock.entity
        mock.__family_tree["B"] = mock.entity

        self.assertRaises(ValueError, mock.test_isSuitableSpouse, 'A', 'B')

        # d. CASE: ACCEPTED (Both are orphans)
        # NOTE: side effects are just a way of providing multiple values
        #       to a function. One value is used as return value for one call.
        mock.return_value.isSibling.return_value = False
        mock.entity.getGender.side_effect = ["Male", "Female"]
        mock.entity.isUnmarried.side_effect = [True, True]
        mock.entity.getMother.side_effect = [None, None]
        mock.entity.getFather.side_effect = [None, None]
       
        # testing the instance of entity
        # print(vars(mock.entity1))
        # print(mock.entity.getGender()) # calling this will use up a side effect. So DO NOT
        
        mock.__family_tree["A"] = mock.entity
        mock.__family_tree["B"] = mock.entity

        self.assertEqual(mock.test_isSuitableSpouse('A', 'B'), True)
        
if __name__ == "__main__":
    unittest.main()




