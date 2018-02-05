from classification import entities, payloadconverters


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
