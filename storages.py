import json
from pymongo import MongoClient
from utils import read_configuration

config = read_configuration()

class AbstractBackend:
    def list_quotes(self):
        raise NotImplemented

    def add_quote(self, quote):
        raise NotImplemented

    def on_start(self):
        pass

    def on_exit(self):
        pass


class InMemoryBackend(AbstractBackend):
    quotes = []

    def list_quotes(self):
        return self.quotes

    def add_quote(self, quote):
        self.quotes.append(quote)


class FileBackend(AbstractBackend):

    def add_quote(self, quote):
        with open('data.json', 'r') as f:
            content = json.loads(f.read())
            content.append(quote)

        with open('data.json', 'w') as f:
            f.write(json.dumps(content))

    def list_quotes(self):
        with open('data.json', 'r') as f:
            return json.loads(f.read())


class DatabaseBackend(AbstractBackend):
    conn = None
    db = None

    def on_start(self):

        host = config['mongodb_host']
        port = int(config['mongodb_port'])

        self.conn = MongoClient(host, port)
        self.db = self.conn[config['mongodb_database']]

    def on_exit(self):
        self.conn.close()

    def list_quotes(self):
        collection = self.db['quotes']
        cursor = collection.find({})
        return list(cursor)

    def add_quote(self, quote):
        collection = self.db['quotes']
        collection.insert_one(quote)
