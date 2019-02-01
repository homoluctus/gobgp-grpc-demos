import grpc
import gobgp_pb2_grpc


class Client(object):
    def __init__(self, address):
        """
        Support context manager
        
        :params address: Bind host address and port
        """

        try:
            self.__channel = grpc.insecure_channel(address)
            self.__stub = gobgp_pb2_grpc.GobgpApiStub(self.__channel)
        except grpc.RpcError:
            raise

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        return self.__channel.close()

    @property
    def channel(self):
        return self.__channel

    @property
    def stub(self):
        return self.__stub
