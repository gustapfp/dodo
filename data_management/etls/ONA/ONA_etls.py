from .json_reader import JSONReader

JSON_PATH = "data_management//ona_form_as_json//sheets_data.json"
json_reader = JSONReader(JSON_PATH)
sections = json_reader.get_sections_list()
subsections = json_reader.get_subsections_list(sections)


def insert_questions(apps, schema_editor):
    QuestionModel = apps.get_model("data_management", "Question")
    questions_to_inset = json_reader.get_questions_list(sections, subsections)

    for question in questions_to_inset:
      
        QuestionModel.objects.create(
            question_id=question.id,
            description=question.description,
            guidance=question.orientation,
            evidence=question.evidence,
            core= question.core,
            level =  question.level
        )


def remove_questions(apps, schema_editor):
    QuestionModel = apps.get_model("data_management", "Question")
    QuestionModel.objects.all().delete()




def insert_subsections(apps, schema_editor):
    SubsectionModel = apps.get_model("data_management", "FormSubsection")
    QuestionModel = apps.get_model("data_management", "Question")

    for subsection in subsections:
        subsection_obj = SubsectionModel.objects.create(
            subsection_id=subsection.id,
            subsection_title=subsection.title,
        )
        # --- Questions Level 1 ---
        q_level1 = subsection.level1
        q_level1_id = [question.id for question in q_level1]

        questions_level1 = []
        for question_id in q_level1_id:
            try:
                question_object = QuestionModel.objects.get(question_id=question_id)
                questions_level1.append(question_object)
            except QuestionModel.DoesNotExist:
                pass

        subsection_obj.questions_level1.set(questions_level1)

        # --- Questions Level 2 ---
        q_level2 = subsection.level2
        q_level2_id = [question.id for question in q_level2]
        questions_level2 = []
        for question_id in q_level2_id:
            try:
                question_object = QuestionModel.objects.get(question_id=question_id)
                questions_level2.append(question_object)
            except QuestionModel.DoesNotExist:
                pass

        subsection_obj.questions_level2.set(questions_level2)


def remove_subsections(apps, schema_editor):
    SubsectionModel = apps.get_model("data_management", "FormSubsection")

    SubsectionModel.objects.all().delete()



def insert_sections(apps, schema_editor):
    SectionModel = apps.get_model("data_management", "FormSection")
    SubsectionModel = apps.get_model("data_management", "FormSubsection")
    QuestionModel = apps.get_model("data_management", "Question")

    for section in sections:
        section_obj = SectionModel.objects.create(
            section_id=section.id,
            section_title=section.title,
        )

        # --- Questions Level 3 ---
        q_level3 = section.level3
        q_level3_id = [question.id for question in q_level3]

        questions_level3 = []
        for question_id in q_level3_id:
            try:
                question_object = QuestionModel.objects.get(question_id=question_id)
                questions_level3.append(question_object)
            except QuestionModel.DoesNotExist:
                pass

        section_obj.questions_level3.set(questions_level3)

        # --- SubSections ---
        json_subsections = section.subsections
        subsection_ids = [subsection.id for subsection in json_subsections]
        subsections_objects = []
        for _subsection_id in subsection_ids:
            try:
                subsection_object = SubsectionModel.objects.get(
                    subsection_id=_subsection_id
                )
                subsections_objects.append(subsection_object)
            except SubsectionModel.DoesNotExist:
                pass

        section_obj.form_subsections.set(subsections_objects)


def remove_sections(apps, schema_editor):
    SubsectionModel = apps.get_model("data_management", "FormSection")

    SubsectionModel.objects.all().delete()

