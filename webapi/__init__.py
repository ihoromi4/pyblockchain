from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config


class WebAPI:
    def __init__(self, blockchain):
        self.blockchain = blockchain

        self.create_routes()


    def create_routes(self):
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

            config.add_route('validate_blockchain', '/api/v1/valid')
            config.add_view(self.validate_blockchain, route_name='validate_blockchain')

            self.app = config.make_wsgi_app()

    def test_server(self, ip, port):
        server = make_server(ip, port, self.app)
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
        state = self.blockchain.get_state()
        return Response(str(state))

    def add_item(self, request):
        item = request.params.get('item', None)

        self.blockchain.add_item(item)
        msg = 'Success!'
        return Response(msg)

    def validate_blockchain(self, request):
        if self.blockchain.is_valid:
            msg = 'Blockchain agreed!'
        else:
            msg = 'Blockchain damaged!'
        return Response(msg)
        

