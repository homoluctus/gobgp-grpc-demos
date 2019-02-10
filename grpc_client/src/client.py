import sys
import grpc
from gobgp import gobgp_pb2_grpc


class GoBGPClient(object):
    def __init__(self, server_address):
        """
        Support context manager

        :params server_address: gRPC server address included host and port
        """

        try:
            self.__channel = grpc.insecure_channel(server_address)
            self.stub = gobgp_pb2_grpc.GobgpApiStub(self.__channel)
        except grpc.RpcError:
            raise

    def __enter__(self):
        return self

    def __exit__(self, *exc_details):
        return self.__channel.close()

    @property
    def channel(self):
        return self.__channel


def run(server_address, callback, args=(), kwargs={}):
    """
    Run callback function

    :params server_address: gRPC serever address
    :params callback: executable function or class
                      (first argument must be 'stub')
    :params args,kwargs: arguments for callback
    """

    try:
        with GoBGPClient(server_address=server_address) as client:
            callback(client.stub, *args, **kwargs)
    except grpc.RpcError as err:
        print(err, file=sys.stderr)
    except Exception as err:
        print(err, file=sys.stderr)
