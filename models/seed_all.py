import sys
import os
from importlib import import_module

SEEDERS = [
    'seed_user',
    'seed_category',
    'seed_article',
    'seed_page',
    'seed_design',
    'seed_widget',
    'seed_navigation',
]

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    for seeder in SEEDERS:
        print(f'Running {seeder}...')
        module = import_module(seeder)
        # Each seeder has a function named like seed_[table]s
        func_name = [fn for fn in dir(module) if fn.startswith('seed_')][0]
        getattr(module, func_name)()
    print('All seeders executed.')
