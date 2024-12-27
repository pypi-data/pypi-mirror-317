from .figure import *
from .array import *

class PivotTable:
  def __init__(self, yNames = [], xNames = [], xValues = []):
    self.YNames = yNames
    self.XNames = xNames
    self.XValues = xValues

  def to_array(self):
    array = [[""] + self.XNames]
    for i in range(len(self.YNames)):
      array.append([self.YNames[i]] + self.XValues[i])
    return array

  @classmethod
  def from_array(cls, array):
    pivotTable = PivotTable()
    count = len(array)
    if 0 < count:
      pivotTable.XNames = array[0][1:]
      for i in range(1, count):
        pivotTable.YNames.append(array[i][0])
        pivotTable.XValues.append(array[i][1:])
    return pivotTable

class PivotgraphAxis:
  def __init__(self, pivotTable, tick = None):
    self.PivotTable = pivotTable
    if tick is None:
      tick = FigureTick()
    self.Tick = tick

class PivotgraphColors:
  def __init__(self, layoutTitle = "black", xTitle = "black", yTitle = "black", grid = "gray", background = "white", bars = []):
    self.LayoutTitle = layoutTitle
    self.XTitle = xTitle
    self.YTitle = yTitle
    self.Grid = grid
    self.Background = background
    self.Bars = bars

  def bar(self, index = 0):
    if index < len(self.Bars):
      return self.Bars[index]
    return None

class Pivotgraph:
  def __init__(self, axis, colors = None):
    self.Axis = axis
    if colors is None:
      colors = PivotgraphColors()
    self.Colors = colors

  def to_figure(self):
    pivotTable = self.Axis.PivotTable
    figure = Figure()
    for i in range(len(pivotTable.XNames)):
      barColor = self.Colors.bar(i)
      figure.add_trace(pgo.Bar(showlegend = True, name = pivotTable.XNames[i], x = pivotTable.XValues[i], y = pivotTable.YNames, marker_color = barColor, textfont = dict(size = 24, color = barColor)))
    figure.update_traces(orientation = "h", textposition = "outside", texttemplate = " %{x:} ")
    figure.update_xaxes(zeroline = True, zerolinecolor = self.Colors.Grid, zerolinewidth = 0.5, tickformat = self.Axis.Tick.Format, dtick = self.Axis.Tick.Dtick, linecolor = self.Colors.Grid, linewidth = 3, gridcolor = self.Colors.Grid, griddash = "dot", mirror = True)
    figure.update_yaxes(zeroline = True, zerolinecolor = self.Colors.Grid, zerolinewidth = 0.5, linecolor = self.Colors.Grid, linewidth = 3, mirror = True, autorange = "reversed")
    figure.update_layout(title = dict(text = "", font = dict(color = self.Colors.LayoutTitle, size = 26), x = 0.5),
      xaxis = dict(title = "", color = self.Colors.XTitle),
      yaxis = dict(title = "", color = self.Colors.YTitle),
      legend = dict(orientation = "h", xanchor = "right", x = 1, yanchor = "bottom", y = 1.01, font = dict(size = 20, color = self.Colors.LayoutTitle)),
      font = dict(size = 20),
      paper_bgcolor = self.Colors.Background, plot_bgcolor = self.Colors.Background)
    return figure
