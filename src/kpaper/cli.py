# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from kbasic import cyan, yellow, red, File, Folder, ensure_path, could_be_path
from os.path import abspath
from os import system
from argparse import ArgumentParser, Namespace

parser = ArgumentParser(prog='kpaper', usage='kpapering...')
parser.add_argument('command', action='store', nargs='?')
parser.add_argument('path', action='store', default='./', nargs='?')
parser.add_argument('-b', '--basic', action='store_true', help="use a minimal template paper")

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
commands = ['init']

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def kpaper():
    args = parser.parse_args()
    assert could_be_path(args.path), red(f"{args.path} not a valid path...")
    match args:
        case Namespace(command=None): print(yellow(f'no commands given...\nplease choose use one of the following:\n\t* {'\n\t* '.join(commands)}'))
        case Namespace(command='init', path=p, basic=False): copy_template('default', abspath(p))
        case Namespace(command='init', path=p, basic=True): copy_template('minimal', abspath(p))
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