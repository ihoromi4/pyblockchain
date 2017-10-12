from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

import blockchain


class App:
    def __init__(self):
        filepath = 'blockchain.json'
        self.chain = blockchain.Blockchain(filepath)

        with Configurator() as config:
            config.add_route('', '/')
            config.add_view(self.index, route_name='')

            config.add_route('api', '/api')
            config.add_view(self.api, route_name='api')

            config.add_route('api_v1', '/api/v1')
            config.add_view(self.api_v1, route_name='api_v1')

            config.add_route('blockchain_state', '/api/v1/state')
            config.add_view(self.get_blockchain_state, route_name='blockchain_state')

            config.add_route('add_item', '/api/v1/add')
            config.add_view(self.add_item, route_name='add_item')

            self.app = config.make_wsgi_app()

    def test_server(self):
        server = make_server('0.0.0.0', 6543, self.app)
        server.serve_forever()

    #@view_config(route_name='')
    def index(self, request):
        text = 'Please, use /api endpoint'
        return Response(text)

    #@view_config(route_name='api')
    def api(self, request):
        text = 'This is "Blockchain Knows" API root'
        return Response(text)

    #@view_config(route_name='api_v1')
    def api_v1(self, request):
        text = 'API version 1'
        return Response(text)

    def get_blockchain_state(self, request):
        state = self.chain.get_state()
        return Response(str(state))

    def add_item(self, request):
        item = request.params.get('item', None)

        self.chain.add_item(item)
        msg = 'Success!'
        return Response(msg)


if __name__ == '__main__':
    app = App()
    app.test_server()

