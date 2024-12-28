import plotly.graph_objects as pgo
from pyemon.path import *

class FigureTick:
  def __init__(self, dtick = 1, format = "d"):
    self.Dtick = dtick
    self.Format = format

class Figure(pgo.Figure):
  @property
  def LayoutTitleText(self):
    return self.layout.title.text

  @LayoutTitleText.setter
  def LayoutTitleText(self, value):
    self.layout.title.text = value

  @property
  def XTitleText(self):
    return self.layout.xaxis.title.text

  @XTitleText.setter
  def XTitleText(self, value):
    self.layout.xaxis.title.text = value

  @property
  def YTitleText(self):
    return self.layout.yaxis.title.text

  @YTitleText.setter
  def YTitleText(self, value):
    self.layout.yaxis.title.text = value

  def Write(self, filePath, width = 1600, height = 900):
    Path.from_file_path(filePath).makedirs()
    self.write_image(filePath, width = width, height = height)
