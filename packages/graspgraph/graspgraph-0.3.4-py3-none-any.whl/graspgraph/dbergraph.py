from .digraph import *
from .database import *

class DbergraphColors:
  def __init__(self, title = "black", cluster = "black", tableFont = "black", tableFrame = "gray", relation = "skyblue", background = "white"):
    self.Title = title
    self.Cluster = cluster
    self.TableFont = tableFont
    self.TableFrame = tableFrame
    self.Relation = relation
    self.Background = background

class Dbergraph:
  def __init__(self, database = None, colors = None, fontName = "Yu Mincho Demibold"):
    if database is None:
      database = Database()
    if colors is None:
      colors = DbergraphColors()
    self.Database = database
    self.Colors = colors
    self.FontName = fontName

  def to_dot(self):
    databases = {}
    for table in self.Database.Tables:
      if table.Namespace in databases:
        databases[table.Namespace].append(table)
      else:
        databases[table.Namespace] = [table]
    dot = Digraph()
    dot.graph_attr["label"] = "<>"
    dot.graph_attr["labelloc"] = "t"
    dot.graph_attr["labeljust"] = "c"
    dot.graph_attr["fontcolor"] = self.Colors.Title
    dot.graph_attr["margin"] = "0"
    dot.graph_attr["rankdir"] = "LR"
    dot.graph_attr["dpi"] = "350"
    dot.graph_attr["bgcolor"] = self.Colors.Background
    dot.node_attr["fontname"] = self.FontName
    dot.node_attr["shape"] = "none"
    dot.edge_attr["color"] = self.Colors.Relation
    relations = []
    for database in sorted(databases.items()):
      with dot.subgraph(name = """cluster_{}""".format(database[0])) as sg:
        sg.attr(label = database[0], labeljust = "l", color = self.Colors.Cluster, fontcolor = self.Colors.Cluster)
        for table in database[1]:
          nodeName = table.path().replace(".", "_")
          strings = []
          strings.append("""<<font color="{}"><table border="1" cellspacing="0" cellpadding="0" color="{}" bgcolor="{}"><tr><td colspan="2"><b>{}</b></td></tr>""".format(self.Colors.TableFont, self.Colors.TableFrame, self.Colors.TableFrame, table.display_name()))
          for column in table.Columns:
            strings.append("""<tr><td bgcolor="{}" cellpadding="2" port="{}"> {} </td><td bgcolor="{}" cellpadding="2" align="left"> {} </td><td bgcolor="{}" cellpadding="2" align="left"> {} </td></tr>""".format(self.Colors.Background, column.Name, column.display_name(), self.Colors.Background, column.Type, self.Colors.Background, column.Caption))
            srcId = """{}:{}""".format(nodeName, column.Name)
            for relation in column.Relations:
              paths = relation.split(".")
              columnName = paths.pop()
              relations.append([srcId, """{}:{}""".format("_".join(paths), columnName)])
          strings.append("</table></font>>")
          sg.node(nodeName, "".join(strings))
    for relation in relations:
      dot.edge(relation[1], relation[0], dir = "back", arrowtail = "crow")
    return dot
