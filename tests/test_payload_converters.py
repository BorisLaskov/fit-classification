from classification import entities, payloadconverters
from pytest import fixture


def test_student_to_tasks_to_save_request_conversion():
    input = {'student_1': {'lab1': 5, 'lab2': 10},
             'student_2': {'lab3': 50, 'lab4': -101}}
    expected = [
        entities.StudentClassificationPreviewDto(
            classification_identifier='lab1',
            student_username='student_1',
            value=5),
        entities.StudentClassificationPreviewDto(
            classification_identifier='lab2',
            student_username='student_1',
            value=10),
        entities.StudentClassificationPreviewDto(
            classification_identifier='lab4',
            student_username='student_2',
            value=-101),
        entities.StudentClassificationPreviewDto(
            classification_identifier='lab3',
            student_username='student_2',
            value=50),
    ]

    actual = payloadconverters.save_request_from_s2t(input)
    assert len(actual) == len(expected)
    for e in expected:
        assert e in actual


def test_task_to_students_to_save_request_conversion():
    input = {'lab1': {'student_1': 14, 'student_3': -21},
             'lab2': {'student_2': 66, 'student_4': 'over9000'}}
    expected = [
        entities.StudentClassificationPreviewDto(
            classification_identifier='lab1',
            student_username='student_1',
            value=14),
        entities.StudentClassificationPreviewDto(
            classification_identifier='lab2',
            student_username='student_2',
            value=66),
        entities.StudentClassificationPreviewDto(
            classification_identifier='lab1',
            student_username='student_3',
            value=-21),
        entities.StudentClassificationPreviewDto(
            classification_identifier='lab2',
            student_username='student_4',
            value='over9000'),
    ]

    actual = payloadconverters.save_request_from_t2s(input)
    assert len(actual) == len(expected)
    for e in expected:
        assert e in actual


@fixture
def get_request_payload():
    return [
        {'classificationMap':
             {'lab01': 1.0,
              'mark': 'F',
              'pandas': 3.75,
              'sem_check': False,
              'tasks': 4.75,
              'tasks_check': False,
              'total': 4.75},
         'email': '...@fit.cvut.cz',
         'firstName': '...',
         'fullName': None,
         'lastName': '...',
         'username': 'student_1'},
        {'classificationMap':
             {'lab01': 5.0,
              'lab02': 3.0,
              'lab03': 4.8,
              'lab04': 3.0,
              'lab05': 4.2,
              'mark': 'F',
              'sem_approved': True,
              'sem_check': False,
              'sem_def': 'https://github.com/...',
              'tasks': 25.0,
              'tasks_check': True,
              'total': 25.0,
              'wt01': 5.0},
         'email': '...@fit.cvut.cz',
         'firstName': '...',
         'fullName': None,
         'lastName': '...',
         'username': 'student_2'},
        {'classificationMap':
             {'lab01': 2.0,
              'lab03': 4.8,
              'lab04': 5.0,
              'lab05': 4.5,
              'mark': 'F',
              'pandas': 4.375,
              'sem_approved': True,
              'sem_check': False,
              'sem_def': 'https://gitlab.fit.cvut.cz/...',
              'tasks': 32.675,
              'tasks_check': True,
              'total': 32.675,
              'wt01': 5.0,
              'wt02': 2.0,
              'wt3': 5.0},
         'email': '...@fit.cvut.cz',
         'firstName': '...',
         'fullName': None,
         'lastName': '...',
         'username': 'student_3'}
    ]


def test_student_to_tasks_from_get_response_converter(get_request_payload):
    input = get_request_payload
    expected = {'student_1': {'lab01': 1.0,
                              'mark': 'F',
                              'pandas': 3.75,
                              'sem_check': False,
                              'tasks': 4.75,
                              'tasks_check': False,
                              'total': 4.75},
                'student_2': {'lab01': 5.0,
                              'lab02': 3.0,
                              'lab03': 4.8,
                              'lab04': 3.0,
                              'lab05': 4.2,
                              'mark': 'F',
                              'sem_approved': True,
                              'sem_check': False,
                              'sem_def': 'https://github.com/...',
                              'tasks': 25.0,
                              'tasks_check': True,
                              'total': 25.0,
                              'wt01': 5.0},
                'student_3': {'lab01': 2.0,
                              'lab03': 4.8,
                              'lab04': 5.0,
                              'lab05': 4.5,
                              'mark': 'F',
                              'pandas': 4.375,
                              'sem_approved': True,
                              'sem_check': False,
                              'sem_def': 'https://gitlab.fit.cvut.cz/...',
                              'tasks': 32.675,
                              'tasks_check': True,
                              'total': 32.675,
                              'wt01': 5.0,
                              'wt02': 2.0,
                              'wt3': 5.0}
                }
    actual = payloadconverters.s2t_from_get_response(input)
    assert actual == expected


def test_task_to_students_from_get_response_converter(get_request_payload):
    input = get_request_payload
    expected = {'lab01': {'student_1': 1.0,
                          'student_2': 5.0,
                          'student_3': 2.0},
                'mark': {'student_1': 'F',
                         'student_2': 'F',
                         'student_3': 'F'},
                'pandas': {'student_1': 3.75,
                           'student_3': 4.375},
                'sem_check': {'student_1': False,
                              'student_2': False,
                              'student_3': False},
                'tasks': {'student_1': 4.75,
                          'student_2': 25.0,
                          'student_3': 32.675},
                'tasks_check': {'student_1': False,
                                'student_2': True,
                                'student_3': True},
                'total': {'student_1': 4.75,
                          'student_2': 25.0,
                          'student_3': 32.675},
                'lab02': {'student_2': 3.0},
                'lab03': {'student_2': 4.8,
                          'student_3': 4.8},
                'lab04': {'student_2': 3.0,
                          'student_3': 5.0},
                'lab05': {'student_2': 4.2,
                          'student_3': 4.5},
                'sem_approved': {'student_2': True,
                                 'student_3': True},
                'sem_def': {'student_2': 'https://github.com/...',
                            'student_3': 'https://gitlab.fit.cvut.cz/...'},
                'wt01': {'student_2': 5.0,
                         'student_3': 5.0},
                'wt02': {'student_3': 2.0},
                'wt3': {'student_3': 5.0}
                }
    actual = payloadconverters.t2s_from_get_response(input)
    assert actual == expected
