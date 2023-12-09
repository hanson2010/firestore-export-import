import json
import os
from pathlib import Path

from helpers.firestore_native import Firestore


def export(collections_exclude='', output_dir='./output'):
    env_name = 'GOOGLE_APPLICATION_CREDENTIALS'
    env_name2 = 'GOOGLE_CLOUD_PROJECT'
    # Check if the environment variable exists
    if env_name not in os.environ:
        print(f"Error: Environment variable '{env_name}' is not defined.")
        exit(1)
    env_value = os.environ[env_name]
    print(f'Firestore credential is at {env_value}.')

    client = Firestore(Path(env_value), 'avidict-us')

    collections = client.get_all_collections()
    filtered_collections = list([collection for collection in collections if collection not in collections_exclude.split(',')])

    for collection in filtered_collections:
        process_collection(client,
                           Path(f'{output_dir}/{collection}.json'),
                           collection)


def calculate_sum():
    num1 = int(input('Enter the first number: '))
    num2 = int(input('Enter the second number: '))
    sum = num1 + num2
    print('The sum of the two numbers is:', sum)


def print_message():
    message = input('Enter the message you want to print: ')
    print(message)


def process_collection(client, file_path, collection):
    fields = client.get_all_properties(collection)
    docs = client.read_all(collection)

    str = json.dumps(docs)

    with open(file_path, 'w') as json_file:
        json_file.write(str)

    print(f'Wrote {len(docs)} documents from collection {collection}')


if __name__ == '__main__':
    print('Welcome to the Firestore Export and Import program!')

    print('Please select from the following options:')
    print('1. Export Firestore in native mode to json file')
    print('2. Calculate the sum of two numbers')
    print('3. Print a message')

    selection = int(input('Enter your selection: '))

    if selection == 1:
        export('airport', 'carrier', 'country', 'subdivision', 'token')
    elif selection == 2:
        calculate_sum()
    elif selection == 3:
        print_message()
    else:
        print('Invalid selection. Please enter a number between 1 and 3.')
