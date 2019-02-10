from gobgp import gobgp_pb2, attribute_pb2
from google.protobuf import any_pb2
from client import GoBGPClient
from path import PathHandler


def main():
    with GoBGPClient(server_address='198.51.100.1:50051') as client:
        path_handler = PathHandler(client.stub, table_type=gobgp_pb2.GLOBAL,
                                   family=gobgp_pb2.Family(afi=1, safi=1))

        nlri = any_pb2.Any()
        nlri.Pack(attribute_pb2.IPAddressPrefix(
            prefix_len=24,
            prefix='192.0.3.0'
        ))

        # attributes
        origin = any_pb2.Any()
        origin.Pack(attribute_pb2.OriginAttribute(origin=0))

        next_hop = any_pb2.Any()
        next_hop.Pack(
            attribute_pb2.NextHopAttribute(next_hop='0.0.0.3')
        )

        no_export = 4294967041
        communities = any_pb2.Any()
        communities.Pack(
            attribute_pb2.CommunitiesAttribute(communities=[no_export])
        )

        pattrs = [origin, next_hop, communities]

        ret = path_handler.add_path(
            nlri=nlri,
            path_attributes=pattrs,
            is_nexthop_invalid=True,
            source_asn=1,
            source_id='1.1.1.1'
        )

        if ret:
            print('SUCESS\n')
        else:
            print('FAILURE')


if __name__ == '__main__':
    main()
