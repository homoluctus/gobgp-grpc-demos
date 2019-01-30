# gobgp-grpc-demos
Python client gets information from GoBGP grpc server.

## Feature
- Get neighbor

## Usage

```
$ docker-compose exec client python3 get_neighbor.py
peer {
  apply_policy {
    export_policy {
      direction: EXPORT
      default_action: -1
    }
    import_policy {
      direction: IMPORT
      default_action: -1
    }
  }
  conf {
    local_as: 1
    neighbor_address: "198.51.100.2"
    peer_as: 2
    peer_type: 1
  }
  ...
```
