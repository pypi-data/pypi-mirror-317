import graphviz
import os
from pyemon.path import *

class Digraph(graphviz.Digraph):
  @property
  def TitleText(self):
    return self.graph_attr["label"][1:][:-1]

  @TitleText.setter
  def TitleText(self, value):
    self.graph_attr["label"] = """<{}>""".format(value)

  def Write(self, filePath, cleanup = False, view = False):
    Path.from_file_path(filePath).makedirs()
    self.render("""{}.dot""".format(os.path.splitext(filePath)[0]), outfile = filePath, cleanup = cleanup, view = view)
