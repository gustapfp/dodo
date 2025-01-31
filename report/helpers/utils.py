
from report.models import ONAFormAnswered, FormSubsectionAnswered, FormSectionAnswered, QuestionAnswer
from collections import Counter

class ReportGenerator:
    pass

class GraphsGenerator:
    pass

class MetricsCalculator:
    def __get_subsection_questions(self, subsection: FormSubsectionAnswered) -> list[QuestionAnswer]:
        leve1_questions = subsection.answered_questions_level_1.all()
        level2_questions = subsection.answered_questions_level_2.all()

        questions_answers = leve1_questions.union(level2_questions)
        return questions_answers
       
    def __get_questions_average_distribution(self, questions_list: list[QuestionAnswer]) -> dict[str, int]:
        questions_answers = [question.answer for question in questions_list]
        answers_distribution = Counter(questions_answers)
        return answers_distribution
    

    def __get_subsection_average_distribution(self, subsection_questions: list[QuestionAnswer]) ->  dict[str, dict[str, int]]:
        subsection_distribution = self.__get_questions_average_distribution(questions_list=subsection_questions)
        return dict(subsection_distribution)
    
    def __get_section_and_subsection_answers_distribution(self, section:FormSectionAnswered) -> dict[str, int]: 
        subsections = section.answered_subsections.all()
        level3_questions = section.answered_questions_level_3.all()

        section_answers = level3_questions
        subsection_distribution = {}
        for subsction in subsections:
            subsection_title = subsction.form_subsection.subsection_title
            subsection_questions_level_1_and_level_2 = self.__get_subsection_questions(subsction)
            subsection_distribution[subsection_title] = self.__get_subsection_average_distribution(subsection_questions_level_1_and_level_2)
            
            section_answers = section_answers.union(subsection_questions_level_1_and_level_2)
           
        section_distribution = self.__get_questions_average_distribution(section_answers)

        return section_distribution, subsection_distribution
    
    def __get_ona_form_total_metrics(self, distribution_by_section:dict) -> dict[str, int]:
        total_counts = Counter()
        for section, counts in distribution_by_section.items():
            total_counts.update(counts)
        return dict(total_counts)
            
        
    def get_ona_form_average_distribution(self, ona_form: ONAFormAnswered) -> dict[str, dict[str, int]]:
        sections = ona_form.answered_sections.all()
        

        distribution_by_section = {}
        distribution_by_subsections = {}
        for section in sections:
            section_name = section.form_section.section_title
            section_distribution, subsection_distribution = self.__get_section_and_subsection_answers_distribution(section)

            distribution_by_section[section_name] = dict(section_distribution)

            distribution_by_subsections[section_name] = dict(subsection_distribution)
            
        total_distribution = self.__get_ona_form_total_metrics(distribution_by_section)

        metrics = {
            "Subsections Distribution" : distribution_by_subsections,
            "Sections Distribution": distribution_by_section,
            "ONA answer Distribution" : total_distribution,
        }
        print(metrics)

        return metrics
        


    
        





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
