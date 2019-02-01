import grpc
import gobgp_pb2
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


def get_peers_by_address(stub, address):
    """
    Returns grpc peer message as a sequence.
    """

    if not isinstance(address, str):
        raise TypeError('str object is required')

    request = gobgp_pb2.ListPeerRequest(
                address=address,
                enableAdvertised=False)

    peers = []
    for response in stub.ListPeer(request):
        peers.append(response)

    return peers


if __name__ == '__main__':
    with Client(address='198.51.100.1:50051') as client:
        peers_list = get_peers_by_address(
            client.stub, address='198.51.100.2')

        print(peers_list)
