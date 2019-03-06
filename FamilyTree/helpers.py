# HELPER MODULES #
import re


class Response:
    def __init__(self):
        self.__error_case = {
            'invalid_entity': 'PERSON_NOT_FOUND',
            'invalid_gender': 'CHILD_ADDITION_FAILED',
            'invalid_spouse_gender': 'SPOUSE_ADDITION_FAILED',
            'invalid_spouse': 'PERSON_NOT_MARRIED',
            'invalid_couple': 'ENTITY_ALREADY_MARRIED',
            'duplicate_name': 'DUPLICATE_PERSON_NAME',
            'is_sibling': 'ENTITIES_ARE_SIBLINGS',
            'no_items': 'NONE',
            'unexpected_behaviour': 'UNEXPECTED_BEHAVIOUR',
            'default': 'FAILURE'
        }

        self.__success_case = {
            'entity_created': 'ENTITY_SUCESSFULLY_CREATED',
            'child_addition': 'CHILD_ADDITION_SUCCEEDED',
            'default': 'SUCCESS'
        }

    def errorHandler(self, case=None):
        if case is None:
            return self.__error_case['default']
        else:
            return self.__error_case[case]

    def successHandler(self, case=None, data=None):
        if case is None and data is None:
            return self.__success_case['default']
        elif case is None and data is not None:
            return ' '.join(data)
        elif case is not None and data is None:
            return self.__success_case[case]
        else:
            return self.errorHandler(case='unexpected_behaviour')


class RegularExpressions:
    def __init__(self):
        self.strvalue = "^[^\s^\t]+$"
        self.arrvalue = "^[\S,?]+"
        self.gender = "(Male|Female)"
    
    def testStr(self, value):
        if re.search(self.strvalue, value):
            return True
        else:
            raise ValueError("Improper Value")
    
    def testGender(self, value):
        if re.search(self.gender, value):
            return True
        else:
            raise ValueError("Gender can only be: Male or Female")
    
    def testEntity(self, value):
        if value is None or self.testStr(value):
            return True
        else:
            raise ValueError("Entity can be None or a valid String")
