from typing import List, Dict, Any, TypeVar
from classification.entities import ClassificationDto, \
    ExpressionParseAllRequestDto, ExpressionParseRequestDto, \
    UserSettingsDto, UserCourseSettingsDto, \
    StudentClassificationPreviewDto


DictOrNone = TypeVar('DictOrNone', Dict[str, Any], None)


ClassificationDtoType = TypeVar(
    'ClassificationDtoType',
    ClassificationDto,
    Dict[str, Any]
)


ParseAllDtoType = TypeVar(
    'ParseAllDtoType',
    ExpressionParseAllRequestDto,
    Dict[str, Any]
)


ParseDtoType = TypeVar(
    'ParseDtoType',
    ExpressionParseRequestDto,
    Dict[str, Any]
)


SettingsDtoType = TypeVar(
    'SettingsDtoType',
    UserSettingsDto,
    Dict[str, bool]
)

CourseSettingsDtoType = TypeVar(
    'CourseSettingsDtoType',
    UserCourseSettingsDto,
    Dict[str, Any]
)

StudentClassificationDtoType = TypeVar(
    'StudentClassificationDtoType',
    List[StudentClassificationPreviewDto],
    List[Dict[str, Any]]
)


StudentsToTasksType = Dict[str, Dict[str, Any]]


TasksToStudentsType = Dict[str, Dict[str, Any]]
