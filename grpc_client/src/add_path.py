import binascii
from gobgp import gobgp_pb2, attribute_pb2
from google.protobuf import any_pb2

import client


class PathHandler(client.GoBGPClient):
    def __init__(self, server_address, table_type, family, vrf_id=None):
        super().__init__(server_address)
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
        for response in self.stub.ListPath(request):
            list_path.append(response.destination)

        return list_path

    def add_path(self, nlri, path_attributes=None, is_nexthop_invalid=False):
        request = gobgp_pb2.AddPathRequest(
            table_type=self.table_type,
            vrf_id=self.vrf_id,
            path=gobgp_pb2.Path(
                nlri=nlri,
                pattrs=path_attributes,
                family=self.family,
                is_nexthop_invalid=is_nexthop_invalid,
            )
        )

        if self.stub.AddPath(request):
            return True
        else:
            return False


if __name__ == '__main__':
    with PathHandler(server_address='198.51.100.1:50051',
                     table_type=gobgp_pb2.GLOBAL,
                     family=gobgp_pb2.Family(afi=1, safi=1)) as client:

        nlri = any_pb2.Any()
        nlri.Pack(attribute_pb2.IPAddressPrefix(
            prefix_len=24,
            prefix='192.0.2.0'
        ))

        # attributes
        origin = any_pb2.Any()
        origin.Pack(attribute_pb2.OriginAttribute(origin=0))

        next_hop = any_pb2.Any()
        next_hop.Pack(attribute_pb2.NextHopAttribute(next_hop='0.0.0.2'))

        no_export = 4294967041
        communities = any_pb2.Any()
        communities.Pack(attribute_pb2.CommunitiesAttribute(communities=[no_export]))

        pattrs = [origin, next_hop, communities]
        
        ret = client.add_path(
            nlri=nlri,
            path_attributes=pattrs,
            is_nexthop_invalid=True,
        )

        if ret:
            print('SUCESS\n')
            print(client.get_path())
        else:
            print('FAILURE')
