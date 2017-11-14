import unittest

import blockchain


class TestBlockchain(unittest.TestCase):
    def test_blockchain(self):
        blockchain_file = 'blockchain_db/test_blockchain.json'
        bchain = blockchain.Blockchain(blockchain_file)

        blocks_amount = bchain.blocks_amount

        bchain.add_item('item')
        bchain.add_item('item')

        self.assertTrue(blocks_amount != bchain.blocks_amount)


if __name__ == '__main__':
    unittest.main()

