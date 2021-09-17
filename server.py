from lib.services.socket import GameSocketServer
        
if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999
    game_socket_server = GameSocketServer(HOST, PORT)
    print('> Server is started')
    game_socket_server.socket_server.serve_forever()