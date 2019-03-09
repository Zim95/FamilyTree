
###########################################################
# Here we will have an entity object                      #
# With its private data members                           #
# That will only interact through GETTER & SETTER methods #  
###########################################################
from .helpers import RegularExpressions


class Entity:
    def __init__(self, name, gender, mother=None):
        self.regex = RegularExpressions()
        self.__name = name if self.regex.testStr(name) else None
        self.__gender = gender if self.regex.testGender(gender) else None
        self.__mother = mother if self.regex.testEntity(mother) else None
        self.__father = None
        self.__spouse = None
        self.__son = []
        self.__daughter = []

    # GETTER METHODS
    def getGender(self):
        return self.__gender
    
    def getName(self):
        return self.__name
    
    def getMother(self):
        return self.__mother

    def getFather(self):
        return self.__father
    
    def getSpouse(self):
        return self.__spouse
    
    def getSon(self):
        return self.__son
    
    def getDaughter(self):
        return self.__daughter
    
    # SETTER METHODS
    def setFather(self, value):
        isDuplicate = self.isNotDuplicate(value)
        if isDuplicate != "OK":
            raise ValueError("Father {}".format(isDuplicate))
        self.__father = value if self.regex.testEntity(value) else None

    def setSpouse(self, value):
        isDuplicate = self.isNotDuplicate(value)
        if isDuplicate != "OK":
            raise ValueError("Father {}".format(isDuplicate))
        self.__spouse = value if self.regex.testEntity(value) else None
    
    def setSon(self, value):
        isDuplicate = self.isNotDuplicate(value)
        if isDuplicate != "OK":
            raise ValueError("Father {}".format(isDuplicate))
        self.__son += [value] if self.regex.testEntity(value) else None
    
    def setDaughter(self, value):
        isDuplicate = self.isNotDuplicate(value)
        if isDuplicate != "OK":
            raise ValueError("Father {}".format(isDuplicate))
        self.__daughter += [value] if self.regex.testEntity(value) else None

    # HELPER METHODS
    def isFemale(self):
        return self.getGender() == "Female"
    
    def isNotDuplicate(self, value):
        if value == self.__name:
            return "has the same name as entity"
        elif value == self.__mother:
            return "has the same name as entity's mother"
        elif value == self.__father:
            return "has the same name as entity's father"
        elif value == self.__spouse:
            return "has the same name as entity's spouse"
        elif value in self.__son:
            return "has the same name as entity's son(s)"
        elif value in self.__daughter:
            return "has the same name as entity's daughter(s)"
        else:
            return "OK"
    
    def isUnmarried(self):
        return self.__spouse is None
