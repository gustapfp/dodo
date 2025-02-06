import json
from typing import List
from .json_base_models import Section, Subsection, Question

class JSONReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_json(self) -> json:
        with open(self.file_path, "r", encoding="utf-8") as json_file:
            json_file = json.load(json_file)
        return json_file

    def get_sections_list(self) -> List[Section]:
        json_file = self.read_json()
        sections = []
        for section in json_file:
            section_dict = json_file[section]
            new_section = Section(
                id =  section_dict['id'],
                title=section,
                subsections =   section_dict['subsections'],
                level3 =  section_dict['level3'],
            )      
            sections.append(new_section)
        return sorted(sections, key=lambda section: section.title)

    def get_subsections_list(self, section_list: list) -> List[Subsection]:
        subsections = []
        for section in section_list:
            nested_subsections = section.subsections
            for subsection in nested_subsections:

                new_subsection = Subsection(
                    id= subsection.id ,
                    level1= subsection.level1 ,
                    level2= subsection.level2 ,
                    title= subsection.title ,

                )
                subsections.append(new_subsection)

        # Sort by the number in front of the subsection title 
        sorted_subsections = sorted(subsections, key=lambda sub: tuple(map(int, sub.title.split()[0].split('.')))) 

        return sorted_subsections

    def extract_level_1_questions(self, subsections_list: list) -> List[Question]:
        level_1_questions = []
        for subsection in subsections_list:
            level_1_questions.extend(subsection.level1)
        return level_1_questions

    def extract_level_2_questions(self, subsections_list: list) -> List[Question]:
        level_2_questions = []
        for subsection in subsections_list:
            level_2_questions.extend(subsection.level2)
        return level_2_questions

    def extract_level_3_questions(self, sections_list: list) -> List[Question]:
        level_3_questions = []
        for section in sections_list:
            level_3_questions.extend(section.level3)
        return level_3_questions

    def get_questions_list(
        self, sections_list: list, subsections_list: list
    ) -> List[Question]:
        level1_questions = self.extract_level_1_questions(subsections_list)
        level2_questions = self.extract_level_2_questions(subsections_list)
        level3_questions = self.extract_level_3_questions(sections_list)
        return level1_questions + level2_questions + level3_questions


if __name__ == "__main__":
    json_reader = JSONReader("data_management//ona_form_as_json//sheets_data.json")
    sections = json_reader.get_sections_list()
    subsections = json_reader.get_subsections_list(sections)
    questions = json_reader.get_questions_list(sections, subsections)

