from gobgp import gobgp_pb2
from google.protobuf import any_pb2
from client import run


def get_path(stub, table_type, family,
             name=None, prefixes=None, sort=True):
    request = gobgp_pb2.ListPathRequest(
                table_type=table_type,
                name=name,
                family=family,
                prefixes=prefixes,
                sort_type=sort)

    for response in stub.ListPath(request):
        print(response.destination)


def main():
    table_type = gobgp_pb2.GLOBAL
    family = gobgp_pb2.Family(afi=1, safi=1)

    run(server_address='198.51.100.1:50051',
        callback=get_path,
        args=(table_type, family))


if __name__ == '__main__':
    main()