from kbasic.parsing import TOML, File, Folder
from importlib.metadata import version 

class Author:
    def __init__(
            self, 
            name: str, 
            affiliation: str = None, 
            corresponding: str = None, 
            orcid: str = None
        ) -> None:
        self.name = name 
        self.affiliation = affiliation
        self.corresponding = corresponding
        self.orcid = orcid

class KPaperConfig(TOML):
    def __init__(self, parent: Folder):
        self.parent: Folder = parent
        File.__init__(self, parent.path+'/kpaper.toml')
        self.title: str = parent.name 
        self.authors: list[str] = ["Keyan Gootkin",]
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