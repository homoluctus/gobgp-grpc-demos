import sys
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


def run(server_address, callback, args=(), kwargs={}):
    """
    Returns values returned by callback function

    :params server_address: gRPC serever address
    :params callback: executable function or class
    :params args,kwargs: arguments for callback
    """
    
    with Client(server_address=server_address) as client:
        try:
            ret = callback(client.stub, *args, **kwargs)
        except grpc.RpcError as err:
            print(err, file=sys.stderr)
        except Exception as err:
            print(err, file=sys.stderr)

    return ret
