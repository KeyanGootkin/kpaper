# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
from kbasic import cyan, yellow, red, File, TOML, Folder, ensure_path, Any, parse_user_input
from os.path import abspath
from os import system
from sys import argv
from argparse import ArgumentParser, Namespace
from importlib.metadata import version

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
commands = ['init', 'add']
config_attrs = ['title', 'authors', 'abstract']
kpaper_parser = ArgumentParser(
    prog='kpaper', # the program is called kpaper
    usage='kpaper [command] *[arguments]',
    description="a utility for creating python projects corresponding to scientific papers",
    epilog="", 
    add_help=False
)
kpaper_parser.add_argument(
    'command', # the action you want kpaper to take
    action='store', nargs=1
)
kpaper_parser.add_argument(
    '-v', '--verbose',
    action='store_true'
)

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                      Command Line Interface                     <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def kpaper():
    [_script_path_, *cmd] = argv
    if '-v' in cmd | '--verbose' in cmd: print(red("...===ENTER KPAPER===..."))
    match cmd:
        case (): 
            print(yellow(
                f'no commands given...\nplease choose use one of the following:\n\t* {'\n\t* '.join(commands)}'
            ))
        case ('init', *_): kpaper_init()
        case ('add', *_):  kpaper_add()
def kpaper_init():
    init_parser = ArgumentParser(
        prog="kpaper init", 
        parents=[kpaper_parser]
    )
    init_parser.add_argument(
        'paths',
        action='store', nargs='+', default=['./'],
        help="the paths to where you want kpaper projects."
    )
    init_parser.add_argument(
        '-b', '--basic',
        action="store_true",
        help="use a minimal template"
    )
    args = init_parser.parse_args()
    if args.verbose: print(red("...===ENTER INIT===..."))
    paths = [abspath(xi) for xi in args.paths]
    match args:
        case Namespace(basic=True): template_choice = 'minimal'
        case _: template_choice = 'default'
    for p in paths: copy_template(template_choice, p)
def kpaper_add(): 
    add_parser = ArgumentParser(
        prog='kpaper add',
        parents=[kpaper_parser]
    )   
    add_parser.add_argument(
        'definitions',
        action='store', nargs='+'
    )
    args = add_parser.parse_args()
    if args.verbose: print(red("...===ENTER ADD===..."))    
    paper = KPaper('./')
    for kv in args.definitions:
        k, v = kv.split('=')
        k = k.strip()
        v = parse_user_input(v.strip())
        setattr(paper.config, k, v)
        paper.config.save()

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def copy_template(template_name: str, destination) -> None:
    ensure_path(destination)
    print(cyan(f'initializing kpaper project in {abspath(destination)}'))
    kpaperDir = File(__file__).parent
    template: Folder = kpaperDir + f'/templates/{template_name}'
    config_file = File(template.path + '/kpaper.toml')
    config_file.copy(destination+'/kpaper.toml')
    for c in template.children: 
        name = c.split('/')[-1]
        system(f"cp -r {c} {destination}/{name}")    

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class KPaperConfig(TOML):
    header: str = f"""
        # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
        # >-|===|>                    KPaper Configuration File                    <|===|-<
        # >=> {("kpaper v."+version('kpaper')).center(73)} <=<
        # !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
    """
    def __init__(self, path: str):
        TOML.__init__(self, path)
    def __setattr__(self, attr: str, value: Any) -> None:
        assert attr in config_attrs, f"{attr} is not a valid attribute."
        super().__setattr__(attr, value)
class KPaper(Folder):
    def __init__(self, path: str|Folder):
        Folder.__init__(self, path)
        self.config = KPaperConfig(self.path + "/kpaper.toml")