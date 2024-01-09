import json
from pathlib import Path


def default(obj):
    """Default JSON serializer."""
    import calendar, datetime

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
        millis = int(
            calendar.timegm(obj.timetuple()) * 1000 +
            obj.microsecond / 1000
        )
        return millis
    raise TypeError('Not sure how to serialize %s' % (obj,))


def export_collections(client, collections_exclude='', output_dir='./json'):
    collections = client.get_all_collections()
    filtered_collections = list([collection for collection in collections if collection not in collections_exclude])

    for collection in filtered_collections:
        process_collection(client,
                           collection,
                           Path(f'{output_dir}/{collection}.json'))


def process_collection(client, collection, file_path, file_type='json'):
    docs = client.read_all_with_id(collection)

    str = json.dumps(docs, ensure_ascii=False, default=default)

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json_file.write(str)

    print(f'Wrote {len(docs)} documents from collection {collection}')
