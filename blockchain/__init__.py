import time
import json
import hashlib
import copy
import threading
from json.decoder import JSONDecodeError

from . import errors


class Blockchain:
    def __init__(self, filepath):
        self.filepath = filepath
        if not type(filepath) is str:
            raise TypeError('type of filepath must be str')

        self.__prepare_items = []
        self.load()
        self.start_block_mining()

    @property
    def blocks_amount(self):
        return self.__data['blocks_amount']

    def get_block(self, block_index):
        if not type(block_index) is int:
            raise TypeError('type of block_index must be int')

        return copy.deepcopy(self.__chain[block_index])

    @property
    def last_block(self):
        return copy.deepcopy(self.__chain[-1])

    @property
    def is_valid(self):
        result = self.validate_blockchain()
        return result['valid']

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
        if not self.is_valid:
            raise ValueError('Blockchain is invalid!')

        with open(self.filepath, 'w') as f:
            json.dump(self.__data, f)

    def get_state(self):
        return copy.deepcopy(self.__data)

    def get_block(self, block_number):
        if block_number >= len(self.__chain):
            raise IndexError('block_number > len of chain')

        return copy.deepcopy(self.__chain[block_number])

    def add_item(self, item):
        self.__prepare_items.append(item)

    def start_block_mining(self):
        self.thread = threading.Thread(target=self.thread_miner)
        self.thread.daemon = True
        self.thread.start()

    def thread_miner(self):
        print('Start block mining')

        while True:
            if self.make_new_block():
                print('Block was mined!')
                self.save()
            time.sleep(1)

    def make_new_block(self):
        if len(self.__prepare_items) == 0:
            return False

        if not self.is_valid:
            raise ValueError('Blockchain is invalid!')

        if len(self.__chain) > 0:
            last_block = self.__chain[-1]
        else:
            last_block = None

        items = self.__prepare_items.copy()

        block = self.generate_block(last_block, items)

        self.__chain.append(block)
        self.__data['blocks_amount'] += 1

        self.__prepare_items.clear()

        return True

    def mine_block_hash(self, hashing_input_part):
        number = 0
        complexity = 5

        while True:
            salt = hex(number)[2:]

            hashing_input = hashing_input_part + salt
            hashing = hashlib.sha256(hashing_input.encode('utf-8'))
            block_hash = hashing.hexdigest()

            if int(block_hash[:complexity], 16) == 0:
                break

            number += 1

        return (block_hash, salt)

    def generate_block(self, prev_block, items, salt=None):
        if prev_block:
            prev_block_hash = prev_block['hash']
        else:
            hashing = hashlib.sha256(b'')
            prev_block_hash = hashing.hexdigest()

        rawjson = json.dumps(items)
        hashing = hashlib.sha256(rawjson.encode('utf-8'))
        items_hash = hashing.hexdigest()

        hashing_input_part = prev_block_hash + items_hash

        if not salt:
            block_hash, salt = self.mine_block_hash(hashing_input_part)
        else:
            hashing_input = hashing_input_part + salt
            hashing = hashlib.sha256(hashing_input.encode('utf-8'))
            block_hash = hashing.hexdigest()

        if prev_block:
            block_number = prev_block['block_number'] + 1
        else:
            block_number = 0

        block = {
            'hash': block_hash,
            'items': items,
            'block_number': block_number,
            'salt': salt
        }

        return block

    def validate_couple(self, prev_block, block):
        items = block['items']
        salt = block['salt']
        valid_block = self.generate_block(prev_block, items, salt)

        return (valid_block['hash'] == block['hash'])

    def validate_blockchain(self):
        blocks_couples = zip([None]+self.__chain[:-1], self.__chain)
        for i, (prev_block, block) in enumerate(blocks_couples):
            if not self.validate_couple(prev_block, block):
                return {'valid': False, 'invalid_block': i}
        return {'valid':True}

