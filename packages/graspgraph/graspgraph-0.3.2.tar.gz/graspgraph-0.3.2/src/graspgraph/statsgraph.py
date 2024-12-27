import numpy as np
from .array import *
from .figure import *

class SimpleStats:
  def __init__(self, values):
    self.__Values = tuple(values)
    if 0 < len(values):
      self.__Avg = sum(values) / len(values)
      self.__Min = min(values)
      self.__Max = max(values)
    else:
      self.__Avg = self.__Min = self.__Max = 0

  @property
  def Values(self):
    return self.__Values

  @property
  def Avg(self):
    return self.__Avg

  @property
  def Min(self):
    return self.__Min

  @property
  def Max(self):
    return self.__Max

class MultipleStats:
  def __init__(self, values, maxCount = 0):
    self.__Values = tuple(values)
    self.__Avg = []
    self.__Min = []
    self.__Max = []
    count = len(values)
    maxCount = min(max(maxCount, 0), count)
    if count <= maxCount:
      self.__Avg = self.__Min = self.__Max = self.__Values
    else:
      for splitedValues in np.array_split(values, maxCount):
        stats = SimpleStats(splitedValues)
        self.__Avg.append(stats.Avg)
        self.__Min.append(stats.Min)
        self.__Max.append(stats.Max)
    self.__Avg = tuple(self.__Avg)
    self.__Min = tuple(self.__Min)
    self.__Max = tuple(self.__Max)

  @property
  def Values(self):
    return self.__Values

  @property
  def Avg(self):
    return self.__Avg

  @property
  def Min(self):
    return self.__Min

  @property
  def Max(self):
    return self.__Max

class StatsgraphAxis:
  def __init__(self, values, maxCount = 0, tick = None):
    self.__Values = tuple(values)
    self.MaxCount = maxCount
    if tick is None:
      tick = FigureTick()
    self.Tick = tick

  @property
  def Values(self):
    return self.__Values

  @property
  def MaxCount(self):
    return self.__MaxCount

  @MaxCount.setter
  def MaxCount(self, value):
    if value <= 0:
      value = max(len(self.__Values), 1)
    self.__MaxCount = value

class StatsgraphColors:
  def __init__(self, layoutTitle = "black", xTitle = "black", yTitle = "black", grid = "gray", background = "white", line = "rgb(0, 0, 0)", fill = "rgba(0, 0, 0, 0.15)"):
    self.LayoutTitle = layoutTitle
    self.XTitle = xTitle
    self.YTitle = yTitle
    self.Grid = grid
    self.Background = background
    self.Line = line
    self.Fill = fill

class Statsgraph:
  def __init__(self, xAxis, yAxis, colors = None):
    self.XAxis = xAxis
    self.YAxis = yAxis
    if colors is None:
      colors = StatsgraphColors()
    self.Colors = colors

  def to_figure(self):
    if len(self.YAxis.Values) <= self.XAxis.MaxCount:
      xValues = self.XAxis.Values
      xDtick = self.XAxis.Tick.Dtick
    else:
      tick = self.XAxis.Values[1] - self.XAxis.Values[0]
      step = (self.XAxis.Values[-1] - self.XAxis.Values[0] + tick) / self.XAxis.MaxCount
      xValues = Array.arange(self.XAxis.Values[0] + step - tick, self.XAxis.Values[-1], step)
      xDtick = max(step, self.XAxis.Tick.Dtick)
      if xValues[-1] <= xDtick:
        xDtick = step
    ySimpleStats = SimpleStats(self.YAxis.Values)
    yMultipleStats = MultipleStats(self.YAxis.Values, self.XAxis.MaxCount)
    yValueGroups = [yMultipleStats.Min, yMultipleStats.Avg, yMultipleStats.Max]
    yRange = [ySimpleStats.Min, min(self.YAxis.Tick.Dtick * self.YAxis.MaxCount + ySimpleStats.Min, ySimpleStats.Max)]
    ticks = [FigureTick(xDtick, self.XAxis.Tick.Format), self.YAxis.Tick]
    if len(xValues) <= 0:
      xValues = [0]
      ticks[0].Dtick = 1
    for i in range(3):
      if len(yValueGroups[i]) <= 0:
        yValueGroups[i] = [0]
        ticks[1].Dtick = 1
    figure = Figure(data = [
      pgo.Scatter(showlegend = False, mode = "lines", x = xValues, y = yValueGroups[0], line = dict(color = self.Colors.Line, width = 0)),
      pgo.Scatter(showlegend = False, mode = "lines", x = xValues, y = yValueGroups[1], line = dict(color = self.Colors.Line, width = 5), fillcolor = self.Colors.Fill, fill = "tonexty"),
      pgo.Scatter(showlegend = False, mode = "lines", x = xValues, y = yValueGroups[2], line = dict(color = self.Colors.Line, width = 0), fillcolor = self.Colors.Fill, fill = "tonexty")])
    figure.update_xaxes(zeroline = True, zerolinecolor = self.Colors.Grid, zerolinewidth = 0.5, tickformat = ticks[0].Format, dtick = ticks[0].Dtick, linecolor = self.Colors.Grid, linewidth = 3, gridcolor = self.Colors.Grid, griddash = "dot", mirror = True)
    figure.update_yaxes(zeroline = True, zerolinecolor = self.Colors.Grid, zerolinewidth = 0.5, tickformat = ticks[1].Format, dtick = ticks[1].Dtick, linecolor = self.Colors.Grid, linewidth = 3, gridcolor = self.Colors.Grid, griddash = "dot", mirror = True)
    figure.update_layout(title = dict(text = "", font = dict(color = self.Colors.LayoutTitle, size = 26), x = 0.5),
      xaxis = dict(title = "", color = self.Colors.XTitle, tick0 = xValues[0]),
      yaxis = dict(title = "", color = self.Colors.YTitle, range = yRange),
      font = dict(size = 14),
      paper_bgcolor = self.Colors.Background, plot_bgcolor = self.Colors.Background)
    return figure
