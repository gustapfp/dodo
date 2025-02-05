from data_management.models import ONAForm, FormSection, FormSubsection, Question


def serialize_question(question: Question) -> dict:
    """
    Get a question from the Question model and convert to a dict.
    """
    return {
        "question_id": question.question_id,
        "description": question.description,
        "guidance": question.guidance,
        "evidence": question.evidence,
    }


def serialize_form_subsection(form_subsection: FormSubsection) -> dict:
    """
    Get a group of question from a FormSubsection and convert to a dict.
    """

    return {
        "subsection_id": form_subsection.subsection_id,
        "subsection_title": form_subsection.subsection_title,
        "questions_level1": [
            serialize_question(q) for q in form_subsection.questions_level1.all()
        ],
        "questions_level2": [
            serialize_question(q) for q in form_subsection.questions_level2.all()
        ],
    }


def serialize_form_section(form_section: FormSection) -> dict:
    """
    Get a section, serialize the level 3 questions, and the form subsections from the FormSection model and convert to a dict.
    """
    return {
        "section_id": form_section.section_id,
        "section_title": form_section.section_title,
        "questions_level3": [
            serialize_question(q) for q in form_section.questions_level3.all()
        ],
        "form_subsections": [
            serialize_form_subsection(f) for f in form_section.form_subsections.all()
        ],
    }


def serialize_ona_form(ona_form: ONAForm) -> dict:
    """
    Serialize the entire ona form from the ONAform model
    """
    return {
        "form_title": ona_form.form_title,
        "ONA_sections": [
            serialize_form_section(f) for f in ona_form.ONA_sections.all()
        ],
        "hospital": {
            "hospital_level": ona_form.hospital.level,
            "hospital_name": ona_form.hospital.name,
        },
        "updated_at": ona_form.updated_at.isoformat(),
    }


