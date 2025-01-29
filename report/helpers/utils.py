from data_management.models import ONAFormAnswered

class ReportGenerator:
    pass

class GraphsGenerator:
    pass

class MetricsCalculator:
    def get_questions_average_grade(self, questions_list: list) -> float:
        questions_answers = [question.answer for question in questions_list]
        print(questions_answers)           




if __name__ == "__main__":
    forms = ONAFormAnswered.objects.all()
    print(forms)

    # from pydantic import BaseModel, Field
    # from typing import List, Optional
    # from datetime import datetime

    # # Simulating related models (FormSectionAnswered, ONAForm, Evaluator)
    # class FormSectionAnswered(BaseModel):
    #     section_name: str

    # class ONAForm(BaseModel):
    #     form_name: str

    # class Evaluator(BaseModel):
    #     name: str
    #     email: str

    # # The main model - ONAFormAnswered
    # class ONAFormAnswered(BaseModel):
    #     answered_sections: List[FormSectionAnswered] = Field(..., description="List of answered sections")
    #     ona_form: ONAForm
    #     evaluator: Evaluator
    #     answered_at: Optional[datetime] = Field(default_factory=datetime.now)

    # # Example of creating some objects
    # form_section_1 = FormSectionAnswered(section_name="Section 1")
    # form_section_2 = FormSectionAnswered(section_name="Section 2")

    # ona_form_instance = ONAForm(form_name="Form 1")
    # evaluator_instance = Evaluator(name="Evaluator 1", email="evaluator1@example.com")

    # # Create an ONAFormAnswered instance
    # ona_form_answered = ONAFormAnswered(
    #     ona_form=ona_form_instance,
    #     evaluator=evaluator_instance,
    #     answered_sections=[form_section_1, form_section_2]
    # )

    # # Output the instance
    # print(ona_form_answered)
