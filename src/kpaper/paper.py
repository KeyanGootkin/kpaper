from kbasic import File, Folder
from importlib.metadata import version 

class KPaperConfig(File):
    def __init__(self, parent: Folder):
        self.parent: Folder = parent
        File.__init__(self, parent.path+'/kpaper.toml')
        self.title: str = parent.name 
        self.authors: list[str] = ["", "Keyan Gootkin",]
        self.abstract: str = ""

    @property 
    def lines(self) -> list[str]:
        return [
            f"# KPaper v.{version('kpaper')} Configuration File",
            f"title = {self.title}",
            f"abstract = {self.abstract}",
            "[authors]",
            f"names = [{", ".join(self.authors)}]",
            f"",
        ]