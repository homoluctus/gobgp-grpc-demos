import binascii
from gobgp import gobgp_pb2, attribute_pb2
from google.protobuf import any_pb2

from client import GoBGPClient


class PathHandler:
    def __init__(self, stub, table_type, family, vrf_id=None):
        self.__stub = stub
        self.table_type = table_type
        self.family = family
        self.vrf_id = vrf_id

    def get_path(self, neighbor_ip=None, prefixes=None, sort=True):
        request = gobgp_pb2.ListPathRequest(
            table_type=self.table_type,
            name=neighbor_ip,
            family=self.family,
            prefixes=prefixes,
            sort_type=sort
        )

        list_path = []
        for response in self.__stub.ListPath(request):
            list_path.append(response)

        return list_path

    def add_path(self, nlri, path_attributes=None, is_nexthop_invalid=False,
                 source_asn=None, source_id=None):
        request = gobgp_pb2.AddPathRequest(
            table_type=self.table_type,
            vrf_id=self.vrf_id,
            path=gobgp_pb2.Path(
                nlri=nlri,
                pattrs=path_attributes,
                family=self.family,
                is_nexthop_invalid=is_nexthop_invalid,
                source_asn=source_asn,
                source_id=source_id
            )
        )

        if self.__stub.AddPath(request):
            return True
        else:
            return False


if __name__ == '__main__':
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
        next_hop.Pack(attribute_pb2.NextHopAttribute(next_hop='0.0.0.3'))

        no_export = 4294967041
        communities = any_pb2.Any()
        communities.Pack(attribute_pb2.CommunitiesAttribute(communities=[no_export]))

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
            print(path_handler.get_path())
        else:
            print('FAILURE')
