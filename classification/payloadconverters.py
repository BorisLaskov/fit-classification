from classification.entities import StudentClassificationPreviewDto


def save_request_from_s2t(student_to_tasks):
    result = list()
    for username, grades in student_to_tasks.items():
        for task, value in grades.items():
            elem = StudentClassificationPreviewDto(
                classification_identifier=task,
                student_username=username,
                value=value
            )
            result.append(elem)
    return result


def save_request_from_t2s(task_to_students):
    result = list()
    for task, grades in task_to_students.items():
        for username, value in grades.items():
            elem = StudentClassificationPreviewDto(
                classification_identifier=task,
                student_username=username,
                value=value
            )
            result.append(elem)
    return result
