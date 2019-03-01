
###########################################################
# Here we will have an entity object                      #
# With its private data members                           #
# That will only interact through GETTER & SETTER methods #  
###########################################################


class Entity:
    def __init__(self, name, gender, mother=None):
        self.__name = name
        self.__gender = gender
        self.__mother = mother
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
        self.__father = value

    def setSpouse(self, value):
        self.__spouse = value
    
    def setSon(self, value):
        self.__son += value
    
    def setDaughter(self, value):
        self.__daughter += value

    def isFemale(self):
        return self.getGender() == "Female"
    
