from os.path import abspath
from sys import argv
def kpaper():
    match argv:
        case [_script_path_, ]: pass 
        case [_script_path_, 'init']:
            print(f'initializing kpaper project in {abspath('./')}')
        case [_script_path_, 'init', str(path)]:
            print(f'initializing kpaper project in {abspath(path)}')