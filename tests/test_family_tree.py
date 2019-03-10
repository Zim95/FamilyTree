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
        mock = self.getMock()

        mock.test_isSuitableMother = family_tree.FamilyTree.isSuitableMother

        mock.entity.isFemale.side_effect = [
            False,
            True,
            True
        ]

        mock.entity.getSpouse.side_effect = [
            None,
            'B'
        ]

        mock.__family_tree['A'] = mock.entity

        self.assertEqual(
            mock.test_isSuitableMother('C'),
            'PERSON_NOT_FOUND'
        )
        self.assertEqual(
            mock.test_isSuitableMother('A'),
            "CHILD_ADDITION_FAILED"
        )
        self.assertEqual(
            mock.test_isSuitableMother('A'),
            "PERSON_NOT_MARRIED"
        )
        self.assertEqual(mock.test_isSuitableMother('A'), True)

    def test_isUnmarried(self):
        mock = self.getMock()

        mock.test_isUnmarried = family_tree.FamilyTree.isUnmarried

        mock.entity.getSpouse.side_effect = [
            'None',
            None
        ]

        mock.__family_tree['A'] = mock.entity

        # ERROR: None Value
        self.assertRaises(
            ValueError,
            mock.test_isUnmarried,
            None
        )
        # ERROR: Entity does not exist
        self.assertRaises(
            ValueError,
            mock.test_isUnmarried,
            'C'
        )
        # False: Entity's spouse is not None 
        self.assertEqual(
            mock.test_isUnmarried('A'),
            False
        )
        # True:  Entity's spouse is None 
        self.assertEqual(
            mock.test_isUnmarried('A'),
            True
        )

    @patch.object(family_tree.FamilyTree, 'isSibling')
    def test_isSuitableSpouse(self, isSibling):
        mock = self.getMock()
        
        mock.test_isSuitableSpouse = family_tree.FamilyTree.isSuitableSpouse

        # If we set isSibling to mock the original isSibling
        # Then it will inturn call getFather and getMother methods
        # To which we will have to set return values
        # We want to avoid this
        # Therefore it is advisable to create a class method in mock itself
        # Rather than mock the isSibling method of the original class
        # So that we can set a return value
        # mock.isSibling = family_tree.FamilyTree.isSibling
        # SOLUTION: So we patch the method using 'patch.object'
        # NOTE: 
        # 1. 'patch' will not work as that will only work for objects
        #     and classes. For methods we need to use patch.method
        # 2.  Side effects are just a way of providing multiple values
        #     to a function. One value is used as return value for one call.
        
        isSibling.side_effect = [
            True,
            False,
            False
        ]
        mock.entity.getGender.side_effect = [
            "Male", "Male",
            "Male", "Female",
            "Male", "Female",
            "Male", "Female"
        ]
        mock.entity.isUnmarried.side_effect = [
            True, False,
            True, True
        ]
    
        # testing the instance of entity
        # print(vars(mock.entity1))
        
        mock.__family_tree["A"] = mock.entity
        mock.__family_tree["B"] = mock.entity

        # CASE: Rejected (Duplicate person name)
        # Side effects used: None
        self.assertEqual(
            mock.test_isSuitableSpouse('A', 'A'),
            'DUPLICATE_PERSON_NAME'
        )
        # CASE: Rejected (Invalid Entity)
        # Side effects used: None
        self.assertEqual(
            mock.test_isSuitableSpouse('A', 'C'),
            'PERSON_NOT_FOUND'
        )
        # CASE: Rejected (Same Spouse Gender)
        # Side effects used: getGender-2
        self.assertEqual(
            mock.test_isSuitableSpouse('A', 'B'),
            'SAME_SPOUSE_GENDER'
        )
        # CASE: Rejected (Entities are siblings)
        # Side effects used: getGender-2, isSibling-1 
        self.assertEqual(
            mock.test_isSuitableSpouse('A', 'B'),
            'ENTITIES_ARE_SIBLINGS'
        )
        # CASE: Rejected (Entities already married)
        # Side effects used: getGender-2, isSibling-1, isUnmarried-2
        self.assertEqual(
            mock.test_isSuitableSpouse('A', 'B'),
            'ENTITY_ALREADY_MARRIED'
        )
        # CASE: Accepted (Entities are suitable for marriage)
        # Side effects used: getGender-2, isSibling-1, isUnmarried-2
        self.assertEqual(
            mock.test_isSuitableSpouse('A', 'B'),
            True
        )

    def test_isSibling(self):
        mock = self.getMock()

        mock.test_isSibling = family_tree.FamilyTree.isSibling

        mock.entity.getMother.side_effect = [
            "Blah", "Blah",
            "Blah", "Baka",
            None, None,
            None, None,
            None, None,
            "Blah", "Blah",
            "Blyat", "Baka"
        ]
        mock.entity.getFather.side_effect = [
            "Baka", "Baka",
            "Bruh", "Blyat",
            None, None,
            "Bruh", "Bruh",
            "Bruh", "Blyat",
            None, None,
            None, None
        ]

        mock.__family_tree["A"] = mock.entity
        mock.__family_tree["B"] = mock.entity

        # same mother, same father: True (Entities are siblings)
        self.assertEqual(mock.test_isSibling('A', 'B'), True)
        # different parents: False (Entities have different parents)
        self.assertEqual(mock.test_isSibling('A', 'B'), False)
        # Orphans: False (Entities are orphans/Root Entities)
        self.assertEqual(mock.test_isSibling('A', 'B'), False)
        # Error: None Values
        self.assertRaises(ValueError, mock.test_isSibling, None, None)
        # Error: Invalid Values 
        self.assertRaises(ValueError, mock.test_isSibling, "None", "None")
        # Error: No mother, Same father 
        self.assertRaises(ValueError, mock.test_isSibling, 'A', 'B')
        # Error: No mother, Different father
        self.assertRaises(ValueError, mock.test_isSibling, 'A', 'B'),
        # Error: Same mother, No father
        self.assertRaises(ValueError, mock.test_isSibling, 'A', 'B')
        # Error: Different mother, No father
        self.assertRaises(ValueError, mock.test_isSibling, 'A', 'B')
        
if __name__ == "__main__":
    unittest.main()




