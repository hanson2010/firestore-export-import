import os
from pathlib import Path

from export_lib import export_collections
from import_lib import import_collections
from helpers.firestore_native import Firestore


def connect():
    env_name1 = 'GOOGLE_APPLICATION_CREDENTIALS'
    env_name2 = 'GOOGLE_CLOUD_PROJECT'
    # Check if the environment variable exists
    if env_name1 not in os.environ:
        print(f"Error: Environment variable '{env_name1}' is not defined.")
        exit(1)
    if env_name2 not in os.environ:
        print(f"Error: Environment variable '{env_name2}' is not defined.")
        exit(1)
    env_value1 = os.environ[env_name1]
    print(f'Firestore credential is at {env_value1}.')
    env_value2 = os.environ[env_name2]
    print(f'Firestore credential is at {env_value2}.')

    return Firestore(Path(env_value1), env_value2)
    

if __name__ == '__main__':
    print('Welcome to the Firestore Export and Import program!')

    print('Please select from the following options:')
    print('1. Export Firestore in native mode to json file')
    print('2. Calculate the sum of two numbers')
    print('3. Print a message')

    selection = int(input('Enter your selection: '))

    if selection == 1:
        client = connect()
        export_collections(client)
    elif selection == 2:
        client = connect()
        import_collections(client)
    else:
        print('Invalid selection. Please enter a number between 1 and 3.')
