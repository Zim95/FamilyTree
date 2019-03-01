
###########################################################
# Here is where the family tree gets created              # 
###########################################################

from .entity import Entity


class FamilyTree:
    __family_tree = {}

    @classmethod
    def isSuitable(cls, name):
        # this method decides if an entity 
        # is suitable to have children or not
        # Passing conditions:
        # 1. Should be a valid entity
        # 2. Should be female
        # 3. Should have a spouse
        valid_entity = name in cls.__family_tree
        valid_gender = cls.__family_tree[name].isFemale()
        valid_spouse = cls.__family_tree[name].getSpouse() is not None

        return valid_entity and valid_gender and valid_spouse

    @classmethod
    def createEntity(cls, name, gender, mother=None):
        pass