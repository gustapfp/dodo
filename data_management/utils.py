from report.models import QuestionAnswer, FormSubsectionAnswered, FormSectionAnswered

def serialize_question(question):
    return {
        "question_id": question.question_id,
        "description": question.description,
        "guidance": question.guidance,
        "evidence": question.evidence,
    }

def serialize_form_subsection(form_subsection):
    return {
        "subsection_id": form_subsection.subsection_id,
        "subsection_title": form_subsection.subsection_title,
        "questions_level1": [serialize_question(q) for q in form_subsection.questions_level1.all()],
        "questions_level2": [serialize_question(q) for q in form_subsection.questions_level2.all()],
    }

def serialize_form_section(form_section):
    return {
        "section_id": form_section.section_id,
        "section_title": form_section.section_title,
        "questions_level3": [serialize_question(q) for q in form_section.questions_level3.all()],
        "form_subsections": [serialize_form_subsection(f) for f in form_section.form_subsections.all()],
    }

def serialize_ona_form(ona_form):
    return {
        "form_title": ona_form.form_title,
        "ONA_sections": [serialize_form_section(f) for f in ona_form.ONA_sections.all()],
        "hospital": {
            "hospital_level": ona_form.hospital.level,
            "hospital_name": ona_form.hospital.name,
            # Add any other necessary fields from the Hospital model
        },
        "updated_at": ona_form.updated_at.isoformat(),
    }

def create_answered_questions(form_data, subsection_questions):
    questions = []
    for question in subsection_questions:
        if question.question_id in form_data:
            answer = form_data.get(question.question_id, None)
            new_question = QuestionAnswer.objects.create(
                question=question, 
                answer=answer
                )
            questions.append(new_question)
    return questions

def create_subsections(form_data, subsections):
    subsection_list = []
    for subsection in subsections:
        new_subsection = FormSubsectionAnswered.objects.create(form_subsection=subsection)

        questions_level_1 = create_answered_questions(form_data, subsection.questions_level1.all())
        new_subsection.answered_questions_level_1.set(questions_level_1)

        questions_level_2 = create_answered_questions(form_data, subsection.questions_level2.all())
        new_subsection.answered_questions_level_2.set(questions_level_2)

        
        subsection_list.append(new_subsection)
    return subsection_list

def create_section(form_data, sections):
    section_list = []
    for section in sections:
        new_section = FormSectionAnswered.objects.create(form_section=section)

        subsection_list = create_subsections(form_data, section.form_subsections.all())
        new_section.answered_subsections.set(subsection_list)


        questions_level_3 = create_answered_questions(form_data, section.questions_level3.all())
        new_section.answered_questions_level_3.set(questions_level_3)
        
        section_list.append(new_section)
        
    return section_list
      