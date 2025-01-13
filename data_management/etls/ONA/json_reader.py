import json
from typing import List
from ONA_json_models import Section

class JSONReader:
  def __init__(self, file_path):
    self.file_path = file_path

  def read_json(self) -> json:
    with open(self.file_path, 'r') as json_file:
      json_file = json.load(json_file)
    return json_file

  def extract_json_data(self) -> List[Section]:
    json_file = self.read_json()
    sections = []
    for section in json_file:
      new_section = Section(**section)
      sections.append(new_section)
    return sections


