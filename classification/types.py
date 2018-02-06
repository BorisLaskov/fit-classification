from typing import List, Dict, Any, TypeVar, Optional, Union
from classification.entities import ClassificationDto, \
    ExpressionParseAllRequestDto, ExpressionParseRequestDto, \
    UserSettingsDto, UserCourseSettingsDto, \
    StudentClassificationPreviewDto


RespDict = Optional[Dict[str, Any]]

ClassificationDtoType = Union[ClassificationDto, Dict[str, Any]]

ParseAllDtoType = Union[ExpressionParseAllRequestDto, Dict[str, Any]]

ParseDtoType = Union[ExpressionParseRequestDto, Dict[str, Any]]

SettingsDtoType = Union[UserSettingsDto, Dict[str, bool]]

CourseSettingsDtoType = Union[UserCourseSettingsDto, Dict[str, Any]]

StudentClassificationDtoType = Union[List[StudentClassificationPreviewDto],
                                     List[Dict[str, Any]]]

StudentsToTasksType = Dict[str, Dict[str, Any]]

TasksToStudentsType = Dict[str, Dict[str, Any]]
