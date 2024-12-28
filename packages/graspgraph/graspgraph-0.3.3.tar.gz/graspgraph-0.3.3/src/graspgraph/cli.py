from .pdf import *

Task.set(PdfConvertTask())
Task.parse_if_main(__name__, Task.get("help"))
def main():
  pass
