# getIP
The Home of the getIP python package.
---

# GetIP Module

This module provides functionality to retrieve local and public IP addresses (both IPv4 and IPv6) and the hostname of the machine.

## Classes

### `GetIPLogic`

#### Methods

- `get_ipv4(self)`: Retrieves the local IPv4 address of the machine.
- `get_ipv6(self)`: Retrieves the local IPv6 address of the machine (only works on Linux).
- `get_ipv4_public(self)`: Retrieves the public IPv4 address of the machine by connecting to `ipify.org`.
- `get_ipv6_public(self)`: Retrieves the public IPv6 address of the machine by connecting to `ipify.org`.

## Functions

- `local()`: Returns the local IPv4 address of the machine.
- `localv4()`: Returns the local IPv4 address of the machine.
- `localv6()`: Returns the local IPv6 address of the machine.
- `public()`: Returns the public IPv4 address of the machine.
- `publicv4()`: Returns the public IPv4 address of the machine.
- `publicv6()`: Returns the public IPv6 address of the machine.
- `hostname(pub=False)`: Returns the hostname of the machine.

## Usage

```python
from getIP import local, localv4, localv6, public, publicv4, publicv6, hostname

# Get local IPv4 address
local_ipv4 = local()

# Get local IPv6 address
local_ipv6 = localv6()

# Get public IPv4 address
public_ipv4 = public()

# Get public IPv6 address
public_ipv6 = publicv6()

# Get hostname
host_name = hostname()
```

