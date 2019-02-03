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


protoc.main((
    '',
    '-I../protobuf/google/protobuf',
    '--python_out=./google/protobuf',
    '--grpc_python_out=./google/protobuf',
    '../protobuf/google/protobuf/any.proto',
    '../protobuf/google/protobuf/empty.proto',
    '../protobuf/google/protobuf/timestamp.proto',
))
