import gobgp_pb2
from client import Client


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
    with Client(server_address='198.51.100.1:50051') as client:
        peers_list = get_peers_by_address(
            client.stub, address='198.51.100.2')

        print(peers_list)
