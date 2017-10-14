import json
import io
import abc
from json.decoder import JSONDecodeError


class BlockchainStorage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self):
        pass

    @abc.abstractmethod
    def save(self, data):
        pass


class BlockchainFileStorage(BlockchainStorage):
    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            pass
        except JSONDecodeError:
            pass

        return None

    def save(self, data):
        with open(self.filepath, 'w') as f:
                json.dump(data, f)
                return True
        return False


class BlockchainIOStorage(BlockchainStorage):
    def __init__(self, io_stream):
        if isinstance(io_stream, io.IOBase):
            self.io_stream = io_stream


__all__ = [
    'BlockchainStorage',
    'BlockchainFileStorage',
    'BlockchainIOStorage'
]


