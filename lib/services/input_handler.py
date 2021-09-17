from enum import Enum
from lib.services.commands import CommandsExecution

class ResponseStatus(str, Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'


class SocketDataResponse:
    def __init__(self, status: ResponseStatus, response: dict) -> None:
        self.status = status
        self.response = response
    
    def get_response_dict(self):
        return { 'status': self.status.value , 'response': self.response }

class SocketBodyData:
    def __init__(self, data: bytes) -> None:
        self.data = data   
        self.key = data.get('inputKey', None)

    def get_decoded_data(self):
        return self.data.decode('utf-8').rstrip('\n')


class SocketDataHandler:
    def __init__(self, data: dict) -> None:
        self.data = SocketBodyData(data)

    def get_response(self) -> SocketDataResponse:
        command_callback = getattr(CommandsExecution, self.data.key)
        if command_callback is None: 
            return SocketDataResponse(status=ResponseStatus.ERROR, response='Invalid command')
        return SocketDataResponse(status=ResponseStatus.SUCCESS, response=command_callback())
        
