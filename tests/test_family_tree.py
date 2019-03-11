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
            'isSuitableMotherB'
        ]

        mock.__family_tree['isSuitableMotherA'] = mock.entity

        self.assertEqual(
            mock.test_isSuitableMother('isSuitableMotherC'),
            'PERSON_NOT_FOUND'
        )
        self.assertEqual(
            mock.test_isSuitableMother('isSuitableMotherA'),
            "CHILD_ADDITION_FAILED"
        )
        self.assertEqual(
            mock.test_isSuitableMother('isSuitableMotherA'),
            "PERSON_NOT_MARRIED"
        )
        self.assertEqual(mock.test_isSuitableMother('isSuitableMotherA'), True)

    def test_isUnmarried(self):
        mock = self.getMock()

        mock.test_isUnmarried = family_tree.FamilyTree.isUnmarried

        mock.entity.getSpouse.side_effect = [
            'None',
            None
        ]

        mock.__family_tree['isUnmarriedA'] = mock.entity

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
            'isUnmarriedC'
        )
        # False: Entity's spouse is not None 
        self.assertEqual(
            mock.test_isUnmarried('isUnmarriedA'),
            False
        )
        # True:  Entity's spouse is None 
        self.assertEqual(
            mock.test_isUnmarried('isUnmarriedA'),
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
        #     and classes. For methods we need to use patch.object.
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
        
        mock.__family_tree["isSuitableSpouseA"] = mock.entity
        mock.__family_tree["isSuitableSpouseB"] = mock.entity

        # CASE: Rejected (Duplicate person name)
        # Side effects used: None
        self.assertEqual(
            mock.test_isSuitableSpouse('isSuitableSpouseA', 'isSuitableSpouseA'),
            'DUPLICATE_PERSON_NAME'
        )
        # CASE: Rejected (Invalid Entity)
        # Side effects used: None
        self.assertEqual(
            mock.test_isSuitableSpouse('isSuitableSpouseA', 'isSuitableSpouseC'),
            'PERSON_NOT_FOUND'
        )
        # CASE: Rejected (Same Spouse Gender)
        # Side effects used: getGender-2
        self.assertEqual(
            mock.test_isSuitableSpouse('isSuitableSpouseA', 'isSuitableSpouseB'),
            'SAME_SPOUSE_GENDER'
        )
        # CASE: Rejected (Entities are siblings)
        # Side effects used: getGender-2, isSibling-1 
        self.assertEqual(
            mock.test_isSuitableSpouse('isSuitableSpouseA', 'isSuitableSpouseB'),
            'ENTITIES_ARE_SIBLINGS'
        )
        # CASE: Rejected (Entities already married)
        # Side effects used: getGender-2, isSibling-1, isUnmarried-2
        self.assertEqual(
            mock.test_isSuitableSpouse('isSuitableSpouseA', 'isSuitableSpouseB'),
            'ENTITY_ALREADY_MARRIED'
        )
        # CASE: Accepted (Entities are suitable for marriage)
        # Side effects used: getGender-2, isSibling-1, isUnmarried-2
        self.assertEqual(
            mock.test_isSuitableSpouse('isSuitableSpouseA', 'isSuitableSpouseB'),
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

        mock.__family_tree["isSiblingA"] = mock.entity
        mock.__family_tree["isSiblingB"] = mock.entity

        # same mother, same father: True (Entities are siblings)
        self.assertEqual(mock.test_isSibling('isSiblingA', 'isSiblingB'), True)
        # different parents: False (Entities have different parents)
        self.assertEqual(mock.test_isSibling('isSiblingA', 'isSiblingB'), False)
        # Orphans: False (Entities are orphans/Root Entities)
        self.assertEqual(mock.test_isSibling('isSiblingA', 'isSiblingB'), False)
        # Error: None Values
        self.assertRaises(ValueError, mock.test_isSibling, None, None)
        # Error: Invalid Values 
        self.assertRaises(ValueError, mock.test_isSibling, "None", "None")
        # Error: No mother, Same father 
        self.assertRaises(ValueError, mock.test_isSibling, 'isSiblingA', 'isSiblingB')
        # Error: No mother, Different father
        self.assertRaises(ValueError, mock.test_isSibling, 'isSiblingA', 'isSiblingB')
        # Error: Same mother, No father
        self.assertRaises(ValueError, mock.test_isSibling, 'isSiblingA', 'isSiblingB')
        # Error: Different mother, No father
        self.assertRaises(ValueError, mock.test_isSibling, 'isSiblingA', 'isSiblingB')
    
    def test_addChildren(self):
        mock = self.getMock()

        mock.test_addChildren = family_tree.FamilyTree.addChildren

        mock.__family_tree['addChildrenP'] = mock.entity
        mock.__family_tree['addChildrenQ'] = mock.entity
        mock.__family_tree['addChildrenR'] = mock.entity

        self.assertRaises(
            ValueError,
            mock.test_addChildren,
            'addChildrenX',
            'addChildrenY',
            'addChildrenZ',
            'addChildrenM'
        )

        # test if set son was called with R twice
        mock.test_addChildren('addChildrenP', 'addChildrenQ', 'addChildrenR', 'Male')
        mock.entity.setSon.assert_called_with('addChildrenR')
        
        # test if set daughter was called with R twice
        mock.test_addChildren('addChildrenP', 'addChildrenQ', 'addChildrenR', 'Female')
        mock.entity.setSon.assert_called_with('addChildrenR')

        # test for error if gender is invalid
        self.assertRaises(
            ValueError,
            mock.test_addChildren,
            'addChildrenP',
            'addChildrenQ',
            'addChildrenR',
            'addChildrenM'
        )
    
    @patch.object(family_tree.FamilyTree, 'isSuitableMother')
    def test_createEntity(self, isSuitableMother):
        mock = self.getMock()

        mock.test_createEntity = family_tree.FamilyTree.createEntity

        mock.__family_tree["createEntityA"] = mock.entity
        mock.__family_tree["createEntityF"] = mock.entity

        # Side effects
        isSuitableMother.side_effect = [
            True,
            'False',
            'asd'
        ]
        mock.entity.getSpouse.return_value = 'createEntityF'

        # CASE: Error (Duplicate Name)
        self.assertEqual(
            mock.test_createEntity('createEntityA', 'Male'),
            'DUPLICATE_PERSON_NAME'
        )

        # CASE: Error (Invalid Gender Type)
        self.assertRaises(
            ValueError,
            mock.test_createEntity,
            'createEntityB',
            'createEntityM'
        )
        
        # CASE: Mother is None. A new entity will be created
        mock.test_createEntity('createEntityB', 'Male')
        self.assertEqual('createEntityB' in mock.__family_tree, True)

        # Error: Mother and Entity have the same name
        self.assertRaises(
            ValueError,
            mock.test_createEntity,
            'createEntityC',
            'Male',
            'createEntityC'
        )

        # Error: Mother is an invalid entity
        self.assertRaises(
            ValueError,
            mock.test_createEntity,
            'createEntityC',
            'Male',
            'Mother'
        )


        # CASE: Mother is not None. A new entity will be created under 
        # conditions
        # Condition 1: PASS: Mother is Suitable .i.e isSuitableMother will 
        # return True. Here we have set the first side_effect to be true
        mock.test_createEntity('createEntityC', 'Male', 'createEntityA')
        mock.entity.getSpouse.assert_called_once_with()
        self.assertEqual('createEntityC' in mock.__family_tree, True)
        
        # Condition 2: FAIL: Mother is un Suitable .i.e isSuitableMother will 
        # return some error value. Here we have set the third side_effect to a 
        # random error value.
        # This is because the second side effect gets used up in the elif 
        # condition and only the third side effect is returned to us
        self.assertEqual(
            mock.test_createEntity('createEntityD', 'Male', 'createEntityA'),
            'asd'
        )
        
    def test_addSpouse(self):
        pass

if __name__ == "__main__":
    unittest.main()




