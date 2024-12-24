import logging
from dataclasses import dataclass

import grpc

log = logging.getLogger()


@dataclass
class Response(object):
    code: int
    message: str
    data: any


class BaseGRPClient(object):
    _default_options = [
        ("grpc.max_send_message_length", 5 * 100 * 1024 * 1024),
        ("grpc.max_receive_message_length", 5 * 100 * 1024 * 1024),
    ]

    def __init__(self, address):
        self._channel = None
        self._stub = None
        self._address = address

    def initialize(self):
        self._register_conn()

    def finish(self):
        if self._channel:
            self._channel.close()

    def _register_conn(self):
        self._channel = grpc.insecure_channel(self._address, options=self._default_options)
        self._stub = self.stub_define(channel=self._channel)

    @property
    def stub_define(self):
        raise NotImplementedError

    @property
    def stub(self):
        return self._stub

    @classmethod
    def build_response(cls, code, message="", data=None):
        return Response(code=code, message=message, data=data)
