
###########################################################
# Here is where the family tree gets created              # 
###########################################################

from .entity import Entity
from .helpers import Response


class FamilyTree:
    __family_tree = {}
    __response = Response()

    @classmethod
    def isSuitable(cls, name):
        """
        this method decides if an entity
        is suitable to have children or not

        Passing conditions:
        1. Should be a valid entity
        2. Should be female
        3. Should have a spouse

        """
        valid_entity = name in cls.__family_tree
        valid_gender = cls.__family_tree[name].isFemale()
        valid_spouse = cls.__family_tree[name].getSpouse() is not None

        if not valid_entity:
            return cls.__response.errorHandler(case='invalid_entity')
        elif not valid_gender:
            return cls.__response.errorHandler(case='invalid_gender')
        elif not valid_spouse:
            return cls.__response.errorHandler(case='invalid_spouse')
        else:
            return True

    @classmethod
    def createEntity(cls, name, gender, mother=None):
        pass