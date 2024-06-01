from export_lib import export_collections, export_kind
from import_lib import import_collections
from helpers import Firestore, Datastore


if __name__ == '__main__':
    print('Welcome to the Firestore Export and Import program!')

    print('Please select from the following options:')
    print('1. Export Firestore in Native mode to json file.')
    print('2. Export Firestore in Datastore mode to json file.')
    print('3. Import json file to Firestore in Native mode.')

    selection = int(input('Enter your selection: '))

    if selection == 1:
        client = Firestore()
        export_collections(client)
    elif selection == 2:
        kind = input('Please enter kind to export: ').strip()
        order_str = input('Please enter field to order: ').strip()
        order = (order_str, )
        batch_str = input('Please enter batch size: ').strip()
        batch = -1
        offset = 0
        if batch_str and batch_str != '-1':
            batch = int(batch_str)
            offset_str = input('Please enter offset: ').strip()
            if offset_str:
                offset = int(offset_str)
        client = Datastore()
        export_kind(client, kind, order, batch, offset)
    else:
        client = Firestore()
        import_collections(client)
