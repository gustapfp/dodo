from report.models import QuestionAnswer, FormSubsectionAnswered, FormSectionAnswered
from django.http import QueryDict



def create_answered_questions(form_data:QueryDict, subsection_questions):
    questions = []
    for question in subsection_questions:
        if question.question_id in form_data:
            answer = form_data.get(question.question_id, None)
            new_question = QuestionAnswer.objects.create(
                question=question, answer=answer
            )
            questions.append(new_question)
    return questions


def create_subsections(form_data:QueryDict, subsections):
    subsection_list = []
    for subsection in subsections:
        new_subsection = FormSubsectionAnswered.objects.create(
            form_subsection=subsection
        )

        questions_level_1 = create_answered_questions(
            form_data, subsection.questions_level1.all()
        )
        new_subsection.answered_questions_level_1.set(questions_level_1)

        questions_level_2 = create_answered_questions(
            form_data, subsection.questions_level2.all()
        )
        new_subsection.answered_questions_level_2.set(questions_level_2)

        subsection_list.append(new_subsection)
    return subsection_list


def create_section(form_data:QueryDict, sections):
    section_list = []
    for section in sections:
        new_section = FormSectionAnswered.objects.create(form_section=section)

        subsection_list = create_subsections(form_data, section.form_subsections.all())
        new_section.answered_subsections.set(subsection_list)

        questions_level_3 = create_answered_questions(
            form_data, section.questions_level3.all()
        )
        new_section.answered_questions_level_3.set(questions_level_3)

        section_list.append(new_section)

    return section_list
