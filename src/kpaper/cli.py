# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from kbasic import cyan, yellow, File, Folder, ensure_path, could_be_path
from os.path import abspath
from os import system
from sys import argv

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
commands = ['init']

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def kpaper():
    [_script_path_, *args] = argv
    match args:
        case []: yellow(f'no commands given...\nplease choose use one of the following: {'\n'.join(commands)}')
        case ['init']: copy_template('default', './')
        case ['init', '-b'|'--basic']: copy_template('minimal', './')
        case ['init', str(x)]: 
            if could_be_path(x): copy_template('default', x)
            else: raise NotADirectoryError(f"{x} is not a possible path to a project")
        case ['init', '-b'|'--basic', str(x)]: 
            if could_be_path(x): copy_template('minimal', x)
            else: raise NotADirectoryError(f"{x} is not a possible path to a project")
def copy_template(template_name: str, destination) -> None:
    ensure_path(destination)
    print(cyan(f'initializing kpaper project in {abspath(destination)}'))
    kpaperDir = File(__file__).parent
    template: Folder = kpaperDir + f'/templates/{template_name}'
    config_file = File(kpaperDir.path + '/templates/config-template')
    config_file.copy(destination+'/.kpaper')
    for c in template.children: 
        name = c.split('/')[-1]
        system(f"cp -r {c} {destination+'/'+name}")    

class KPaperConfig(File):
    def __init__(self, ): pass 

class KPaper(Folder):
    def __init__(self, path: str|Folder): pass