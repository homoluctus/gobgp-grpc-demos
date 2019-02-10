from grpc_tools import protoc


protoc.main((
    '',
    '-I../protobuf/',
    '-I../proto',
    '--python_out=./gobgp',
    '--grpc_python_out=./gobgp',
    '../proto/gobgp.proto',
    '../proto/attribute.proto',
    '../proto/capability.proto'
))
