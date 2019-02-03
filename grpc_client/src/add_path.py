import binascii
from gobgp import gobgp_pb2, attribute_pb2
from google.protobuf import any_pb2
from client import run


def add_path(stub, table_type, path, vrf_id=None):
    request = gobgp_pb2.AddPathRequest(
                table_type=table_type,
                vrf_id=vrf_id,
                path=path)
    
    response = stub.AddPath(request)

    if response.uuid:
        print('SUCCESS')
    else:
        print('FAILURE')


def main():
    table_type = gobgp_pb2.GLOBAL

    nlri = any_pb2.Any()
    nlri.Pack(attribute_pb2.IPAddressPrefix(
        prefix_len=24,
        prefix='192.0.2.0'
    ))

    # attributes
    origin = any_pb2.Any()
    origin.Pack(attribute_pb2.OriginAttribute(origin=0))

    next_hop = any_pb2.Any()
    next_hop.Pack(attribute_pb2.NextHopAttribute(next_hop='0.0.0.1'))

    no_export = 4294967041
    communities = any_pb2.Any()
    communities.Pack(attribute_pb2.CommunitiesAttribute(communities=[no_export]))

    pattrs = [origin, next_hop, communities]

    path = gobgp_pb2.Path(
                nlri=nlri,
                pattrs=pattrs,
                family=gobgp_pb2.Family(afi=1, safi=1),
                is_nexthop_invalid=True,
            )

    run(server_address='198.51.100.1:50051',
        callback=add_path,
        args=(table_type, path))


if __name__ == '__main__':
    main()
