import grpc
import gobgp_pb2_grpc


class Client(object):
    def __init__(self, server_address):
        """
        Support context manager
        
        :params server_address: gRPC server address included host and port
        """

        try:
            self.__channel = grpc.insecure_channel(server_address)
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
