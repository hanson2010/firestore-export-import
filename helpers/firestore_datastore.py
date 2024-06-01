import os
from google.cloud import datastore


class Datastore:

    def __init__(self):
        self._client = self._connect()

    def get_batch(self, kind, order=(), batch=-1, offset=0):
        if not order:
            query = self._client.query(kind=kind)
        else:
            query = self._client.query(kind=kind, order=order)
        if batch == -1:
            query_iter = query.fetch(offset=offset)
        else:
            query_iter = query.fetch(limit=batch, offset=offset)
        return list(query_iter)

    def read_all(self, kind, order, batch, offset):
        entities = self.get_batch(kind, order, batch, offset)
        next_offset = offset + len(entities)
        if len(entities) == batch:
            print(f'Suggested next offset: {next_offset}')
        else:
            print('No more entities to read.')
        return [dict(e) for e in entities]

    def read_all_with_id(self, kind, order, batch, offset):
        entities = self.get_batch(kind, order, batch, offset)
        next_offset = offset + len(entities)
        if len(entities) == batch:
            print(f'Suggested next offset: {next_offset}')
        else:
            print('No more entities to read.')
        return [{'id': e.id, 'doc': dict(e)} for e in entities]

    def _connect(self):
        '''
        The datastore library primarily relies on Application Default Credentials (ADC) for authentication.
        It doesn't have a built-in from_service_account_json method.

        ADC searches for credentials in the following locations:

        GOOGLE_APPLICATION_CREDENTIALS environment variable
        User credentials set up by using the Google Cloud CLI
        The attached service account, returned by the metadata server
        '''

        env_name1 = 'GOOGLE_APPLICATION_CREDENTIALS'
        env_name2 = 'GOOGLE_CLOUD_PROJECT'
        # Check if the environment variable exists
        if env_name1 not in os.environ:
            print(f'Error: Environment variable "{env_name1}" is not defined.')
            exit(1)
        if env_name2 not in os.environ:
            print(f'Error: Environment variable "{env_name2}" is not defined.')
            exit(1)
        env_value1 = os.environ[env_name1]
        print(f'Datastore credential is at {env_value1}')
        env_value2 = os.environ[env_name2]
        print(f'Datastore project is {env_value2}')

        return datastore.Client(env_value2)
