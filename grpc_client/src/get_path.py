from gobgp import gobgp_pb2
from client import run
from path import PathHandler


def get_path(stub, table_type, family):
    path_handler = PathHandler(stub,
                               table_type=table_type,
                               family=family)

    for destination in path_handler.get_path():
        print(destination)


if __name__ == '__main__':
    run(server_address='198.51.100.1:50051',
        callback=get_path,
        args=(gobgp_pb2.GLOBAL, gobgp_pb2.Family(afi=1, safi=1)))
