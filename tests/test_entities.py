from classification import entities


def test_classification_text_dto_all_params():
    dto = entities.ClassificationTextDto(identifier='qwerty', name='my-name')
    assert dto.to_dict() == {'identifier': 'qwerty', 'name': 'my-name'}


def test_classification_text_dto_some_params():
    dto = entities.ClassificationTextDto(name='my-name')
    assert dto.to_dict() == {'name': 'my-name'}


def test_classification_dto_all_params():
    cls_text_dtos = [{'identifier': 'qwerty', 'name': 'my-name'},
                     entities.ClassificationTextDto(name='unknown',
                                                    identifier='azerty')]

    dto = entities.ClassificationDto(calculated=True,
                                     classification_text_dtos=cls_text_dtos,
                                     classification_type='SomeTypeOfMine',
                                     course_code='MI-PYT',
                                     expression='2+2*2',
                                     hidden=False,
                                     id=12345,
                                     identifier='PyThOn 101',
                                     index=1337,
                                     lowercase_identifier='python 101',
                                     mandatory=True,
                                     maximum_value=99.99,
                                     minimum_required_value=50,
                                     semester_code='B171',
                                     value_type='pythonical')

    expected = {'calculated': True,
                'classificationTextDtos': [{'identifier': 'qwerty',
                                             'name': 'my-name'},
                                             {'identifier': 'azerty',
                                              'name': 'unknown'}],
                'classificationType': 'SomeTypeOfMine',
                'courseCode': 'MI-PYT',
                'expression': '2+2*2',
                'hidden': False,
                'id': 12345,
                'identifier': 'PyThOn 101',
                'index': 1337,
                'lowercaseIdentifier': 'python 101',
                'mandatory': True,
                'maximumValue': 99.99,
                'minimumRequiredValue': 50,
                'semesterCode': 'B171',
                'valueType': 'pythonical'}

    assert dto.to_dict() == expected


def test_classification_dto_some_params():
    dto = entities.ClassificationDto(calculated=True,
                                     classification_type='SomeTypeOfMine',
                                     course_code='MI-PYT',
                                     hidden=False,
                                     id=12345,
                                     index=1337,
                                     mandatory=True,
                                     minimum_required_value=50,
                                     value_type='pythonical')

    expected = {'calculated': True,
                'classificationType': 'SomeTypeOfMine',
                'courseCode': 'MI-PYT',
                'hidden': False,
                'id': 12345,
                'index': 1337,
                'mandatory': True,
                'minimumRequiredValue': 50,
                'valueType': 'pythonical'}

    assert dto.to_dict() == expected


def test_expression_parse_all_dto_all_params():
    dto = entities.ExpressionParseAllRequestDto(
        expressions=['2+2*2', '1+2+3+4'],
        variable_value_types={'a': 'integer', 'b': 'float'})

    expected = {'expressions': ['2+2*2', '1+2+3+4'],
                'variableValueTypes': {'a': 'integer', 'b': 'float'}}

    assert dto.to_dict() == expected


def test_expression_parse_all_dto_some_params():
    dto = entities.ExpressionParseAllRequestDto(
        variable_value_types={'a': 'integer', 'b': 'float',
                              'c': 'object'})

    expected = {'variableValueTypes': {'a': 'integer', 'b': 'float',
                                       'c': 'object'}}

    assert dto.to_dict() == expected


def test_expression_parse_request_dto_all_params():
    dto = entities.ExpressionParseRequestDto(
        expected_result_type='integer',
        expression='2+2*2',
        variable_value_types={'a': 'integer', 'b': 'float'})

    expected = {'expectedResultType': 'integer',
                'expression': '2+2*2',
                'variableValueTypes': {'a': 'integer', 'b': 'float'}}

    assert dto.to_dict() == expected


def test_expression_parse_request_dto_some_params():
    dto = entities.ExpressionParseRequestDto(
        variable_value_types={'a': 'integer', 'b': 'float'})

    expected = {'variableValueTypes': {'a': 'integer', 'b': 'float'}}

    assert dto.to_dict() == expected


def test_user_settings_dto_all_params():
    dto = entities.UserSettingsDto(unsubscribe_emails=True)
    expected = {'unsubscribeEmails': True}
    assert dto.to_dict() == expected


def test_user_settings_dto_some_params():
    dto = entities.UserSettingsDto()
    expected = {}
    assert dto.to_dict() == expected


def test_user_course_settings_dto_all_params():
    dto = entities.UserCourseSettingsDto(course_code='MI-PYT',
                                         hidden=True,
                                         silenced_notifications=False)

    expected = {'courseCode': 'MI-PYT', 'hidden': True,
                'silencedNotifications': False}

    assert dto.to_dict() == expected


def test_user_course_settings_dto_some_params():
    dto = entities.UserCourseSettingsDto(course_code='MI-PYT')

    expected = {'courseCode': 'MI-PYT'}

    assert dto.to_dict() == expected


def test_student_classification_preview_dto_all_params():
    dto = entities.StudentClassificationPreviewDto(
        classification_identifier='SomeClassID',
        id=1337,
        note='It\'s a kind of magic',
        student_username='studeuse',
        value='???')

    expected = {'classificationIdentifier': 'SomeClassID',
                'id': 1337,
                'note': 'It\'s a kind of magic',
                'studentUsername': 'studeuse',
                'value': '???'}

    assert dto.to_dict() == expected


def test_student_classification_preview_dto_some_params():
    dto = entities.StudentClassificationPreviewDto(
        classification_identifier='SomeClassID',
        note='It\'s a kind of magic')

    expected = {'classificationIdentifier': 'SomeClassID',
                'note': 'It\'s a kind of magic'}

    assert dto.to_dict() == expected
