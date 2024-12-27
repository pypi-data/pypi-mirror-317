from pydantic import BaseModel
import yaml
import inflection
from pyemon.path import *

class DatabaseColumn(BaseModel):
  Name: str
  Type: str
  Comment: str = ""
  Caption: str = ""
  Relations: list[str] = []

  def set_caption_if_empty(self, caption):
    if len(self.Caption) == 0:
      self.Caption = caption

  def display_name(self):
    if len(self.Comment) == 0:
      return self.Name
    else:
      return """{}({})""".format(self.Name, self.Comment)

  @classmethod
  def to_name(cls, name):
    return inflection.underscore(inflection.singularize(name))

class DatabaseTable(BaseModel):
  Namespace: str
  Name: str
  Comment: str = ""
  Columns: list[DatabaseColumn] = []

  def path(self):
    return """{}.{}""".format(self.Namespace, self.Name)

  def display_name(self):
    if len(self.Comment) == 0:
      return self.Name
    else:
      return """{}({})""".format(self.Name, self.Comment)

class Database(BaseModel):
  Tables: list[DatabaseTable] = []

  def update(self):
    for table in self.Tables:
      otherTables = list(filter(lambda otherTable: table != otherTable, self.Tables))
      for column in table.Columns:
        columnName = """{}_{}""".format(DatabaseColumn.to_name(table.Name), DatabaseColumn.to_name(column.Name))
        for otherTable in otherTables:
          for otherColumn in otherTable.Columns:
            if columnName == otherColumn.Name:
              relation = """{}.{}""".format(otherTable.path(), otherColumn.Name)
              if relation not in column.Relations:
                column.Relations.append(relation)
                otherColumn.set_caption_if_empty("FK")
    return self

  def load(self, filePath):
    with open(filePath, "r", encoding = "utf-8") as file:
      self.Tables = Database.from_yaml(file).Tables
    return self

  def save(self, filePath):
    Path.from_file_path(filePath).makedirs()
    with open(filePath, "w", encoding = "utf-8", newline = "\n") as file:
      yaml.dump(self.model_dump(), file, sort_keys = False, default_flow_style = False, allow_unicode = True)
    return self

  @classmethod
  def from_yaml(cls, stream):
    return Database(**yaml.safe_load(stream) or {"Tables": []})

  @classmethod
  def from_file_path(cls, filePath):
    return Database().load(filePath)
