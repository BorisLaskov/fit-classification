from classification.classification import Classification
from classification.exceptions import MissingParameterError


class ClassificationParamsProxy:
    """This proxy class can store some parameters for API calls.

    You can pass parameters listed below either during the creation
    of this object or later via directly setting its attributes.
    Later you can omit them in methods calls. Or supply them anyway
    to override saved defaults.

    Note:
        This proxy can do everything that
        :py:class:`~.classification.Classification` class can.
        See its documentation for all the parameters. Here we describe
        only attributes not present in the default implementation.

    Warning:
        Please note, that due to the fact that some parameters
        can be stored internally, they default to ``None`` now.
        However, they can still be needed to make API calls.
        are not compulsory in method calls. Keep in mind that:

        - If a required parameter is neither saved in proxy
          nor passed to a method explicitly,
          a :py:exc:`~classification.exceptions.MissingParameterError`
          will be raised.
        - The order of arguments in methods of the plain client
          and its proxy version can be different.
          If you prefer to do without named arguments in Python,
          be sure to double check what you are
          passing to a method.


    Attributes:
        classification (str): The implementation of the real library,
            created automatically.
        course_code (str): Stores the code of the course.
        semester (str): Stores the semester identifier.
        group_code (str): Stores the code of the group.
        lang (str): Stores the language tag.

    """

    PARAM_ERROR = 'The following parameter must be supplied: '

    def __init__(self, client_id, client_secret,
                 callback_host='localhost', callback_port=8080,
                 force_new_token=False, session=None,
                 course_code=None, semester=None,
                 group_code=None, lang=None):

        self.classification = Classification(client_id, client_secret,
                                             callback_host, callback_port,
                                             force_new_token, session)
        self.course_code = course_code
        self.semester = semester
        self.group_code = group_code
        self.lang = lang

    def reinit_session(self, callback_host='localhost', callback_port=8080,
                       force_new_token=False):

        self.classification.reinit_session(callback_host, callback_port,
                                           force_new_token)

    def drop_session(self):
        self.classification.drop_session()

    # -----------------------------------------------
    # ---------- CLASSIFICATION CONTROLLER ----------
    # -----------------------------------------------
    def delete_classification(self, classification_id, course_code=None,
                              semester=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        semester = self._get_param(semester, 'semester', False)

        return self.classification \
            .delete_classification(course_code, classification_id,
                                   semester, **kwargs)

    def find_classifications_for_course(self, course_code=None,
                                        semester=None, lang=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        semester = self._get_param(semester, 'semester', False)
        lang = self._get_param(lang, 'lang', False)

        return self.classification \
            .find_classifications_for_course(course_code, semester,
                                             lang, **kwargs)

    def save_classification(self, course_code=None, classification_dto=None,
                            **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)

        return self.classification \
            .save_classification(course_code, classification_dto, **kwargs)

    def change_order_of_classifications(self, indexes, course_code=None,
                                        semester=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        semester = self._get_param(semester, 'semester', False)

        return self.classification \
            .change_order_of_classifications(course_code, indexes,
                                             semester, **kwargs)

    def find_classification(self, identifier, course_code=None,
                            semester=None, lang=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        semester = self._get_param(semester, 'semester', False)
        lang = self._get_param(lang, 'lang', False)

        return self.classification \
            .find_classification(course_code, identifier,
                                 semester, lang, **kwargs)

    def clone_classification_definitions(self, target_semester,
                                         target_course_code,
                                         source_semester,
                                         source_course_code,
                                         remove_existing,
                                         **kwargs):

        return self.classification \
            .clone_classification_definitions(target_semester,
                                              target_course_code,
                                              source_semester,
                                              source_course_code,
                                              remove_existing,
                                              **kwargs)

    # -----------------------------------------------
    # -------------- EDITOR CONTROLLER --------------
    # -----------------------------------------------
    def get_editors(self, course_code=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)

        return self.classification \
            .get_editors(course_code, **kwargs)

    def delete_editor(self, username, course_code=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)

        return self.classification \
            .delete_editor(course_code, username, **kwargs)

    def add_editor(self, username, course_code=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)

        return self.classification \
            .add_editor(course_code, username, **kwargs)

    # -----------------------------------------------
    # ------------ EXPRESSION CONTROLLER ------------
    # -----------------------------------------------
    def evaluate_all(self, expressions_dto=None, **kwargs):

        return self.classification \
            .evaluate_all(expressions_dto, **kwargs)

    def try_validity(self, expression=None, **kwargs):

        return self.classification \
            .try_validity(expression, **kwargs)

    def get_functions(self, **kwargs):

        return self.classification \
            .get_functions(**kwargs)

    # -----------------------------------------------
    # ----------- NOTIFICATION CONTROLLER -----------
    # -----------------------------------------------
    def get_all_notifications(self, username, count=None, page=None,
                              lang=None, **kwargs):

        lang = self._get_param(lang, 'lang', False)

        return self.classification \
            .get_all_notifications(username, count, page, lang, **kwargs)

    def get_unread_notifications(self, username, count=None, page=None,
                                 lang=None, **kwargs):

        lang = self._get_param(lang, 'lang', False)

        return self.classification \
            .get_unread_notifications(username, count, page, lang, **kwargs)

    def unread_all_notifications(self, username, **kwargs):

        return self.classification \
            .unread_all_notifications(username, **kwargs)

    def read_all_notifications(self, username, **kwargs):

        return self.classification \
            .read_all_notifications(username, **kwargs)

    def unread_notification(self, username, id, **kwargs):

        return self.classification \
            .unread_notification(username, id, **kwargs)

    def read_notification(self, username, id, **kwargs):

        return self.classification \
            .read_notification(username, id, **kwargs)

    # -----------------------------------------------
    # ------------- SETTINGS CONTROLLER -------------
    # -----------------------------------------------
    def get_settings(self, semester=None, lang=None, **kwargs):

        semester = self._get_param(semester, 'semester', False)
        lang = self._get_param(lang, 'lang', False)

        return self.classification \
            .get_settings(semester, lang, **kwargs)

    def save_my_settings(self, user_settings_dto=None, **kwargs):

        return self.classification \
            .save_my_settings(user_settings_dto, **kwargs)

    def save_student_course_settings(self, user_course_settings_dto=None,
                                     semester=None, **kwargs):

        semester = self._get_param(semester, 'semester', False)

        return self.classification \
            .save_student_course_settings(user_course_settings_dto,
                                          semester, **kwargs)

    def save_teacher_course_settings(self, user_course_settings_dto=None,
                                     semester=None, **kwargs):

        semester = self._get_param(semester, 'semester', False)

        return self.classification \
            .save_teacher_course_settings(user_course_settings_dto,
                                          semester, **kwargs)

    # -----------------------------------------------
    # ------ STUDENT CLASSIFICATION CONTROLLER ------
    # -----------------------------------------------
    def find_student_group_classifications(self, course_code=None,
                                           group_code=None,
                                           semester=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        group_code = self._get_param(group_code, 'group_code', True)
        semester = self._get_param(semester, 'semester', False)

        return self.classification \
            .find_student_group_classifications(course_code, group_code,
                                                semester, **kwargs)

    def find_student_classifications_for_definitions(self, identifier,
                                                     course_code=None,
                                                     group_code=None,
                                                     semester=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        group_code = self._get_param(group_code, 'group_code', True)
        semester = self._get_param(semester, 'semester', False)

        return self.classification \
            .find_student_classifications_for_definitions(course_code,
                                                          identifier,
                                                          group_code,
                                                          semester, **kwargs)

    def save_student_classifications(self, course_code=None,
                                     student_classifications=None,
                                     semester=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        semester = self._get_param(semester, 'semester', False)

        return self.classification \
            .save_student_classifications(course_code,
                                          student_classifications,
                                          semester, **kwargs)

    def save_student_classifications_simple_s2t(self, course_code=None,
                                                student_to_tasks=None,
                                                semester=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        semester = self._get_param(semester, 'semester', False)

        return self.classification \
            .save_student_classifications_simple_s2t(course_code,
                                                     student_to_tasks,
                                                     semester, **kwargs)

    def save_student_classifications_simple_t2s(self, course_code=None,
                                                task_to_students=None,
                                                semester=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        semester = self._get_param(semester, 'semester', False)

        return self.classification \
            .save_student_classifications_simple_t2s(course_code,
                                                     task_to_students,
                                                     semester, **kwargs)

    def find_student_classification(self, student_username, course_code=None,
                                    semester=None, lang=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        semester = self._get_param(semester, 'semester', False)
        lang = self._get_param(lang, 'lang', False)

        return self.classification \
            .find_student_classification(course_code, student_username,
                                         semester, lang, **kwargs)

    # -----------------------------------------------
    # ---------- STUDENT GROUP CONTROLLER -----------
    # -----------------------------------------------
    def get_course_groups(self, course_code=None,
                          semester=None, lang=None, **kwargs):

        course_code = self._get_param(course_code, 'course_code', True)
        semester = self._get_param(semester, 'semester', False)
        lang = self._get_param(lang, 'lang', False)

        return self.classification \
            .get_course_groups(course_code, semester, lang, **kwargs)

    # -----------------------------------------------
    # -------------- HELPER FUNCTIONS ---------------
    # -----------------------------------------------
    def _get_param(self, supplied, var_name, required):
        result = supplied or getattr(self, var_name)
        if required and result is None:
            raise MissingParameterError(self.PARAM_ERROR + var_name)
        return result
