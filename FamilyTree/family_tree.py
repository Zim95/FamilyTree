
##############################################
# Here is where the family tree gets created # 
##############################################

from .entity import Entity
from .helpers import Response
import inspect


class FamilyTree:
    __family_tree = {}
    __response = Response()

    @classmethod
    def isSuitableMother(cls, name):
        """
        this method decides if an entity
        is suitable to have children or not

        Passing conditions:
        1. Should be a valid entity
        2. Should be female
        3. Should have a spouse

        None should not be passed here
        """

        if name not in cls.__family_tree:
            return cls.__response.errorHandler(case='invalid_entity')
        elif not cls.__family_tree[name].isFemale():
            return cls.__response.errorHandler(case='invalid_gender')
        elif cls.__family_tree[name].getSpouse() is None:
            return cls.__response.errorHandler(case='invalid_spouse')
        else:
            return True

    @classmethod
    def isUnmarried(cls, name):
        if name is None or name not in cls.__family_tree:
            raise ValueError("Invalid Entity")
        return cls.__family_tree[name].getSpouse() is None

    @classmethod
    def isSibling(cls, name, value):
        """
      
        Conditions:
        1. If both their Mothers are None,
            - That means that both of them are orphans.
            - They are not siblings: return False
        2. If both their Fathers are None,
            - That means an invalid case as
                entities can only be created if they have either
                - No Mother or
                - Both Father and Mother
            - Raise a value error saying:
                Entities can either have no mother or need to have both
                mother and father
        3. If both their parents have the same name.
            - They are siblings: return True
        4. If both their parents have different names.
            - They are not siblings: return False
        
        NOTE: Raise error upon NONE and Invalid values

        """

        if name is None and value is None:
            raise ValueError(
                """
                Values cannot be None
                """
            )
        elif name not in cls.__family_tree or value not in cls.__family_tree:
            raise ValueError(
                """
                Invalid Entity values
                """
            )

        entity_mother = cls.__family_tree[name].getMother()
        entity_father = cls.__family_tree[name].getFather()
        spouse_mother = cls.__family_tree[value].getMother()
        spouse_father = cls.__family_tree[value].getFather()

        if all(v is None for v in [
            entity_father,
            entity_mother,
            spouse_father,
            spouse_mother
        ]):
            return False
        elif entity_father is None and spouse_father is None:
            raise ValueError(
                """
                Entities can either have no Mother and Father or both parents
                """
            )
        elif all(v is None for v in [
            spouse_mother,
            entity_mother
        ]) and all(v is not None for v in[
            entity_father,
            spouse_father
        ]):
            raise ValueError(
                cls.__response.errorHandler('unexpected_behaviour')
            )

        elif entity_mother == spouse_mother and entity_father == spouse_father:
            return True
        elif entity_mother != spouse_mother and entity_father != spouse_father:
            return False
        else:
            raise ValueError(
                cls.__response.errorHandler('unexpected_behaviour')
            )

    @classmethod
    def isSuitableSpouse(cls, name, value):
        """
        
        Conditions:
        1. They cannot have the same name
        2. They both need to be valid members in family tree
        3. They need to be of the opposite gender
        4. They cannot be siblings
        5. They both need to be unmarried

        """

        ftree = cls.__family_tree

        if name == value:
            return cls.__response.errorHandler(case='duplicate_name')
        elif name not in ftree or value not in ftree:
            return cls.__response.errorHandler(case='invalid_entity')
        elif ftree[name].getGender() == ftree[value].getGender():
            return cls.__response.errorHandler(case='invalid_spouse_gender')
        elif cls.isSibling(name, value) is True:
            return cls.__response.errorHandler(case="is_sibling")
        elif not ftree[name].isUnmarried() or not ftree[value].isUnmarried():
            return cls.__response.errorHandler(case="invalid_couple")
        else:
            return True

    @classmethod
    def addChildren(cls, mother, father, name, gender):
        """

        -> Add children to the list of sons, if gender is Male
        -> Add children to the list of daughters, if gender is Female
        -> Raise Error Otherwise
        
        """

        if gender == "Male":
            cls.__family_tree[mother].setSon(name)
            cls.__family_tree[father].setSon(name)
        elif gender == "Female":
            cls.__family_tree[mother].setDaughter(name)
            cls.__family_tree[father].setDaughter(name)
        else:
            raise ValueError("Gender can only be either 'Male' or 'Female'")

    @classmethod
    def createEntity(cls, name, gender, mother=None):
        """
        
        -> Create an entity object
        1. CASE 1: Entity without a mother.
            -> Add the entity object entity to the family tree 
                as name value pairs
        2. CASE 2: Entity with a suitable mother.
            -> Set entity's father.
            -> Add entity to list of mother's and father's son or daughter
            -> Add the entity object entity to the family tree 
                as name value pairs
        3. CASE 3: Entity with an unsuitable mother.
            -> Return back the error response
        
        DO NOT ALLOW DUPLICATES: TEST CASE
        """
        
        entity_object = Entity(name, gender, mother=mother)

        if name in cls.__family_tree:
            return cls.__response.errorHandler('duplicate_name')
        elif mother is None:
            cls.__family_tree[name] = entity_object
        elif cls.isSuitableMother(mother) is True:
            father = cls.__family_tree[mother].getSpouse()
            entity_object.setFather(father)
            cls.addChildren(mother, father, name, gender)
            cls.__family_tree[name] = entity_object
        else:
            return cls.isSuitableMother(mother)
    
    @classmethod
    def addSpouse(cls, name, value):
        
        """
        Suitable?
        YES:
            -> Set spouse names for both entities
        NO:
            -> return the error case
        """
        suitability = cls.isSuitableSpouse(name, value)

        if suitability is True:
            cls.__family_tree[name].setSpouse(value)
            cls.__family_tree[value].setSpouse(name)
        else:
            return suitability
        
