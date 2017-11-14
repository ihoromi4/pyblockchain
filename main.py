import blockchain
import webapi


class App:
    def __init__(self):
        filepath = 'blockchain_db/blockchain.json'
        self.blockchain = blockchain.Blockchain(filepath)
        self.webapi = webapi.WebAPI(self.blockchain)

    def test_server(self, ip, port):
        print('Start test server')
        self.webapi.test_server(ip, port)


if __name__ == '__main__':
    app = App()
    app.test_server('0.0.0.0', 6543)

