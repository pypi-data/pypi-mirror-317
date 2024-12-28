from pdf2image import convert_from_path
from pyemon.path import *
from pyemon.task import *
from pyemon.list import *
from pyemon.status import *

class Pdf:
  def __init__(self, pages = []):
    self.Pages = pages

  def load(self, filePath):
    self.Pages = convert_from_path(filePath)
    return self

  def save(self, filePath, pageIndex = 0):
    _, _, ext = Path.split(filePath)
    self.Pages[pageIndex].save(filePath, ext.upper())
    return self

  @classmethod
  def convert(cls, fromFilePath, toFilePath):
    Pdf().load(fromFilePath).save(toFilePath)

class PdfConvertTask(Task):
  def __init__(self, caption = "<pdf file path> <image file path>"):
    super().__init__(caption)

  def run(self, argv):
    pdfFilePath = List.shift(argv)
    imageFilePath = List.shift(argv)
    if pdfFilePath is not None and imageFilePath is not None:
      Pdf.convert(pdfFilePath, imageFilePath)
      print(Status(imageFilePath, "done"))
