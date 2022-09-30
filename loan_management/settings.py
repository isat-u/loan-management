import os
from split_settings.tools import include

try:
    with open('loan_management/ENV') as f:
        ENV = f.read().strip()
        print(ENV)
except FileNotFoundError:
    ENV = 'prod'
    env_file = open('loan_management/ENV', 'w')
    env_file.write(ENV)
    env_file.close()

include('apps.py')
include(f'environments/{ENV}.py')
