from classification.utils import remove_none_entries
from dataclasses import dataclass
from typing import List, Dict, Any, TypeVar


@dataclass
class ClassificationTextDto:

    identifier: str = None
    name: str = None

    def to_dict(self):

        body = dict()

        body['identifier'] = self.identifier
        body['name'] = self.name

        remove_none_entries(body)

        return body


ClassificationTextDtoType = TypeVar(
    'ClassificationTextDtoType',
    ClassificationTextDto,
    Dict[str, str]
)


@dataclass
class ClassificationDto:

    calculated: bool = None
    classification_text_dtos: List[ClassificationTextDtoType] = None
    classification_type: str = None
    course_code: str = None
    expression: str = None
    hidden: bool = None
    id: int = None
    identifier: str = None
    index: int = None
    lowercase_identifier: str = None
    mandatory: bool = None
    maximum_value: float = None
    minimum_required_value: float = None
    semester_code: str = None
    value_type: str = None

    def to_dict(self):

        body = dict()

        body['calculated'] = self.calculated
        body['classificationTextDtos'] = self.classification_text_dtos
        body['classificationType'] = self.classification_type
        body['courseCode'] = self.course_code
        body['expression'] = self.expression
        body['hidden'] = self.hidden
        body['id'] = self.id
        body['identifier'] = self.identifier
        body['index'] = self.index
        body['lowercaseIdentifier'] = self.lowercase_identifier
        body['mandatory'] = self.mandatory
        body['maximumValue'] = self.maximum_value
        body['minimumRequiredValue'] = self.minimum_required_value
        body['semesterCode'] = self.semester_code
        body['valueType'] = self.value_type

        remove_none_entries(body)

        if 'classificationTextDtos' in body:
            objects = body['classificationTextDtos']
            dictionaries = [dto.to_dict() if hasattr(dto, 'to_dict') else dto
                            for dto in objects]
            body['classificationTextDtos'] = dictionaries

        return body


@dataclass
class ExpressionParseAllRequestDto:

    expressions: Any = None
    variable_value_types: Any = None

    def to_dict(self):

        body = dict()

        body['expressions'] = self.expressions
        body['variableValueTypes'] = self.variable_value_types

        remove_none_entries(body)

        return body


@dataclass
class ExpressionParseRequestDto:

    expected_result_type: str = None
    expression: str = None
    variable_value_types: str = None

    def to_dict(self):

        body = dict()

        body['expectedResultType'] = self.expected_result_type
        body['expression'] = self.expression
        body['variableValueTypes'] = self.variable_value_types

        remove_none_entries(body)

        return body


@dataclass
class UserSettingsDto:

    unsubscribe_emails: bool = None

    def to_dict(self):

        body = dict()

        body['unsubscribeEmails'] = self.unsubscribe_emails

        remove_none_entries(body)

        return body


@dataclass
class UserCourseSettingsDto:

    course_code: str = None
    hidden: bool = None
    silenced_notifications: bool = None

    def to_dict(self):

        body = dict()

        body['courseCode'] = self.course_code
        body['hidden'] = self.hidden
        body['silencedNotifications'] = self.silenced_notifications

        remove_none_entries(body)

        return body


@dataclass
class StudentClassificationPreviewDto:

    classification_identifier: str = None
    id: int = None
    note: str = None
    student_username: str = None
    value: Any = None

    def to_dict(self):

        body = dict()

        body['classificationIdentifier'] = self.classification_identifier
        body['id'] = self.id
        body['note'] = self.note
        body['studentUsername'] = self.student_username
        body['value'] = self.value

        remove_none_entries(body)

        return body
