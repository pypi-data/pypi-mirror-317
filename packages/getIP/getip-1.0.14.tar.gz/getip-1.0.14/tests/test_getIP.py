import pytest
from getIP import local, public


def test_local_ipv4():
    local_ip = local()
    assert local_ip is not None, "Local IPv4 address could not be fetched"
    assert "." in local_ip, "Local IP does not look like an IPv4 address"


def test_public_ipv4():
    public_ip = public()
    assert public_ip is not None, "Public IPv4 address could not be fetched"
    assert "." in public_ip, "Public IP does not look like an IPv4 address"
