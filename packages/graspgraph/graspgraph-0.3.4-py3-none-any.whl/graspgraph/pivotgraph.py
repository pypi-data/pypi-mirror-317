from .figure import *
from .array import *

class PivotBar:
  def __init__(self, name, x = [], y = []):
    self.Name = name
    self.X = x
    self.Y = y

class PivotTable:
  def __init__(self, bars = []):
    self.Bars = bars

  def to_array(self):
    array = [[""] + list(map(lambda bar: bar.Name, self.Bars))]
    if 0 < len(self.Bars):
      y = self.Bars[0].Y
      yCount = len(y)
      for i in range(yCount):
        array.append([y[i]])
      for bar in self.Bars:
        for i in range(yCount):
          array[i + 1].append(bar.X[i])
    return array

  @classmethod
  def from_array(cls, array):
    pivotTable = PivotTable()
    count = len(array)
    if 0 < count:
      xValues = []
      for name in array[0][1:]:
        pivotTable.Bars.append(PivotBar(name))
        xValues.append([])
      y = []
      for yIndex in range(1, count):
        y.append(array[yIndex][0])
        for xIndex, value in enumerate(array[yIndex][1:]):
          xValues[xIndex].append(value)
      for i, bar in enumerate(pivotTable.Bars):
        bar.X = xValues[i]
        bar.Y = y
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
    for i, bar in enumerate(pivotTable.Bars):
      barColor = self.Colors.bar(i)
      figure.add_trace(pgo.Bar(showlegend = True, name = bar.Name, x = bar.X, y = bar.Y, marker_color = barColor, textfont = dict(size = 24, color = barColor)))
    figure.update_traces(orientation = "h", textposition = "outside", texttemplate = "%{x:}")
    figure.update_xaxes(zeroline = True, zerolinecolor = self.Colors.Grid, zerolinewidth = 0.5, tickformat = self.Axis.Tick.Format, dtick = self.Axis.Tick.Dtick, linecolor = self.Colors.Grid, linewidth = 3, gridcolor = self.Colors.Grid, griddash = "dot", mirror = True)
    figure.update_yaxes(zeroline = True, zerolinecolor = self.Colors.Grid, zerolinewidth = 0.5, linecolor = self.Colors.Grid, linewidth = 3, mirror = True, autorange = "reversed")
    figure.update_layout(title = dict(text = "", font = dict(color = self.Colors.LayoutTitle, size = 26), x = 0.5),
      xaxis = dict(title = "", color = self.Colors.XTitle),
      yaxis = dict(title = "", color = self.Colors.YTitle),
      legend = dict(orientation = "h", xanchor = "right", x = 1, yanchor = "bottom", y = 1.01, font = dict(size = 20, color = self.Colors.LayoutTitle)),
      font = dict(size = 20),
      paper_bgcolor = self.Colors.Background, plot_bgcolor = self.Colors.Background)
    return figure
