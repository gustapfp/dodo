from json_reader import JSONReader

ona_json = JSONReader("data_management//ONAformquerquirements//ona_form.json")
ona_as_sections_list = JSONReader.extract_json_data()
