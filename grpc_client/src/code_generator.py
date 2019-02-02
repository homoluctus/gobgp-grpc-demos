from grpc_tools import protoc


protoc.main((
    '',
    '-I../protobuf/',
    '-I../proto',
    '--python_out=.',
    '--grpc_python_out=.',
    '../proto/gobgp.proto',
    '../proto/attribute.proto',
    '../proto/capability.proto',
    '../protobuf/google/protobuf/any.proto',
    '../protobuf/google/protobuf/empty.proto',
    '../protobuf/google/protobuf/timestamp.proto',
))