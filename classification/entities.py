from classification.utils import remove_none_entries


class ClassificationDto:

    def __init__(self,
                 calculated=None,
                 classification_text_dtos=None,
                 classification_type=None,
                 course_code=None,
                 expression=None,
                 hidden=None,
                 id=None,
                 identifier=None,
                 index=None,
                 lowercase_identifier=None,
                 mandatory=None,
                 maximum_value=None,
                 minimum_required_value=None,
                 semester_code=None,
                 value_type=None):

        self.body = dict()

        self.body['calculated'] = calculated
        self.body['classificationTextDtos'] = classification_text_dtos
        self.body['classificationType'] = classification_type
        self.body['courseCode'] = course_code
        self.body['expression'] = expression
        self.body['hidden'] = hidden
        self.body['id'] = id
        self.body['identifier'] = identifier
        self.body['index'] = index
        self.body['lowercaseIdentifier'] = lowercase_identifier
        self.body['mandatory'] = mandatory
        self.body['maximumValue'] = maximum_value
        self.body['minimumRequiredValue'] = minimum_required_value
        self.body['semesterCode'] = semester_code
        self.body['valueType'] = value_type

        remove_none_entries(self.body)

        if 'classificationTextDtos' in self.body:
            objects = self.body['classificationTextDtos']
            dictionaries = [dto.body for dto in objects]
            self.body['classificationTextDtos'] = dictionaries


class ClassificationTextDto:

    def __init__(self, identifier=None, name=None):

        self.body = dict()

        self.body['identifier'] = identifier
        self.body['name'] = name

        remove_none_entries(self.body)


class ExpressionParseAllRequestDto:

    def __init__(self, expressions=None, variable_value_types=None):

        self.body = dict()

        self.body['expressions'] = expressions
        self.body['variableValueTypes'] = variable_value_types

        remove_none_entries(self.body)


class ExpressionParseRequestDto:

    def __init__(self, expected_result_type=None,
                 expression=None, variable_value_types=None):

        self.body = dict()

        self.body['expectedResultType'] = expected_result_type
        self.body['expression'] = expression
        self.body['variableValueTypes'] = variable_value_types

        remove_none_entries(self.body)


class UserSettingsDto:

    def __init__(self, unsubscribe_emails=None):
        self.body = dict()

        self.body['unsubscribeEmails'] = unsubscribe_emails

        remove_none_entries(self.body)


class UserCourseSettingsDto:

    def __init__(self, course_code=None,
                 hidden=None, silenced_notifications=None):

        self.body = dict()

        self.body['courseCode'] = course_code
        self.body['hidden'] = hidden
        self.body['silencedNotifications'] = silenced_notifications

        remove_none_entries(self.body)


class StudentClassificationPreviewDto:

    def __init__(self, classification_identifier=None,
                 id=None, note=None,
                 student_username=None,
                 value=None):

        self.body = dict()

        self.body['classificationIdentifier'] = classification_identifier
        self.body['id'] = id
        self.body['note'] = note
        self.body['studentUsername'] = student_username
        self.body['value'] = value

        remove_none_entries(self.body)
