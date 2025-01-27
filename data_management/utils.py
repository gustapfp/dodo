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


