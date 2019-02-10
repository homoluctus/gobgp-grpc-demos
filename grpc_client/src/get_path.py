from gobgp import gobgp_pb2
from client import GoBGPClient
from path import PathHandler


if __name__ == '__main__':
    with GoBGPClient(server_address='198.51.100.1:50051') as client:
        path_handler = PathHandler(client.stub,
                                   table_type=gobgp_pb2.GLOBAL,
                                   family=gobgp_pb2.Family(afi=1, safi=1))

        print(path_handler.get_path())
