error_case = {
    'invalid_entity': 'PERSON_NOT_FOUND',
    'invalid_gender': 'CHILD_ADDITION_FAILED',
    'invalid_spouse': 'PERSON_NOT_MARRIED',
    'duplicate_name': 'DUPLICATE_PERSON_NAME',
    'no_items': 'NONE',
    'unexpected_behaviour': 'UNEXPECTED_BEHAVIOUR',
    'default': 'FAILURE'
}

success_case = {
    'entity_created': 'ENTITY_SUCESSFULLY_CREATED',
    'child_addition': 'CHILD_ADDITION_SUCCEEDED',
    'default': 'SUCCESS'
}


def errorHandler(case=None):
    if case is None:
        return error_case['default']
    else:
        return error_case[case]


def successHandler(case=None, data=None):
    if case is None and data is None:
        return success_case['default']
    elif case is None and data is not None:
        return ' '.join(data)
    elif case is not None and data is None:
        return success_case[case]
    else:
        return errorHandler(case='unexpected_behaviour')