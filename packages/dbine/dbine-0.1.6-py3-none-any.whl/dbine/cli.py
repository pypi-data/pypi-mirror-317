from .connection import *
from pyemon.list import *
from pyemon.task import *
from pyemon.status import *
from graspgraph.pdf import *

class PdfWriteTask(Task):
  def run(self, argv):
    yamlFilePath = List.shift(argv)
    pdfFilePath = List.shift(argv)
    if yamlFilePath is None or pdfFilePath is None:
      return
    with Connection(ConnectionConfig.from_file_path(yamlFilePath)) as connection:
      dbergraph = gg.Dbergraph(connection.get_database())
      dbergraph.Database.update()
      dbergraph.to_dot().Write(pdfFilePath, cleanup = True)
      print(Status(pdfFilePath, "done"))
Task.set(PdfWriteTask("<yaml file path> <pdf file path>"))

Task.set(PdfConvertTask())
Task.parse_if_main(__name__, Task.get("help"))
def main():
  pass
