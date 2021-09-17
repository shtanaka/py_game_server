import json
import socketserver

from lib.services.input_handler import SocketDataResponse, SocketDataHandler


class GameUDPHandler(socketserver.BaseRequestHandler):
    def __get_decoded_data(self):
        return self.request[0].decode('utf-8').rstrip('\n')

    def __get_dict_data(self):
        decoded_data = self.__get_decoded_data()
        return json.loads(decoded_data)

    def __get_encoded_response(self, response: SocketDataResponse):
        str_dict = json.dumps(response.get_response_dict())
        return str_dict.encode('utf-8')

    def handle(self):
        try:
            socket = self.request[1]
            
            dict_data = self.__get_dict_data()
            client_address = self.client_address[0] 
            print(f'> received: {str(dict_data)} from {client_address}')
  
            socket_data_handler = SocketDataHandler(dict_data)
            response = socket_data_handler.get_response()
            encoded_response = self.__get_encoded_response(response)
            socket.sendto(encoded_response, self.client_address)
            print(f'> responded: {response.get_response_dict()} to {client_address}')
        except json.decoder.JSONDecodeError:
            print('> WARNING: Invalid input received! Discarding UDP request')


class GameSocketServer:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.socket_server = socketserver.UDPServer((self.host, self.port), GameUDPHandler)

