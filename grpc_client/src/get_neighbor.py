from gobgp import gobgp_pb2
from client import run


def get_peers_by_address(stub, address):
    """
    Returns grpc peer message as a sequence.
    """

    if not isinstance(address, str):
        raise TypeError('str object is required')

    request = gobgp_pb2.ListPeerRequest(
                address=address,
                enableAdvertised=False)

    for response in stub.ListPeer(request):
        print(response)


if __name__ == '__main__':
    run(server_address='198.51.100.1:50051',
        callback=get_peers_by_address,
        args=('198.51.100.2',))
