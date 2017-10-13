import json
from json.decoder import JSONDecodeError
import hashlib


class Blockchain:
    def __init__(self, filepath):
        self.filepath = filepath
        self.__prepare_items = []
        self.load()

    def set_default(self):
        self.__data = {
                'blockchain':[],
                'blocks_amount': 0,
            }
        self.__chain = self.__data['blockchain']

    def load(self):
        try:
            with open(self.filepath) as f:
                self.__data = json.load(f)
                self.__chain = self.__data['blockchain']
        except FileNotFoundError:
            self.set_default()
        except JSONDecodeError:
            self.set_default()

    def save(self):
        if not self.validate_chain():
            raise TypeError('Chain is invalid!')

        with open(self.filepath, 'w') as f:
            json.dump(self.__data, f)

    def validate_chain(self):
        return True

    def get_state(self):
        return self.__data.copy()

    def get_block(self, block_number):
        if block_number >= len(self.__chain):
            raise IndexError('block_number > len of chain')

        return self.__chain[block_number].copy()

    def add_item(self, item):
        self.__prepare_items.append(item)

        if len(self.__prepare_items) >= 2:
            self.make_block()
            self.save()

    def make_block(self):
        items = self.__prepare_items.copy()
        self.__prepare_items.clear()

        rawjson = json.dumps(items)
        hashing = hashlib.sha256(rawjson.encode('utf-8'))
        items_hash = hashing.hexdigest()

        if len(self.__chain) > 0:
            prevblock = self.__chain[-1]
            prevblock_hash = prevblock['hash']
        else:
            hashing = hashlib.sha256(b'')
            prevblock_hash = hashing.hexdigest()

        hashing_input = prevblock_hash + items_hash
        hashing = hashlib.sha256(hashing_input.encode('utf-8'))
        hash = hashing.hexdigest()

        block_number = self.__data['blocks_amount']

        block = {
            'hash': hash,
            'items': items,
            'block_number': block_number
        }

        self.__chain.append(block)
        self.__data['blocks_amount'] += 1

