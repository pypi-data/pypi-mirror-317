import subprocess
from requests import get
import socket
import re

class GetIPLogic:
    def get_ipv4(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("69.69.69.69", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip
    
    # TODO: Only works on Linux
    # Credit: https://tech-bloggers.in/get-ipv6-info-using-python/
    def get_ipv6(self):
        try:
            # Execute the ifconfig command
            output = subprocess.check_output(["ifconfig"])

            # Extract the IPv6 address using regular expressions
            ipv6_pattern = r"inet6 ([\da-fA-F:]+)"
            ipv6_address = re.findall(ipv6_pattern, str(output))

            if ipv6_address:
                return ipv6_address[0]
            else:
                return None
        except subprocess.CalledProcessError as e:
            return None
    
    # Get public IPv4 address by connecting to ipify.org
    def get_ipv4_public(self):
        try:
            return get('https://api.ipify.org').text
        except Exception as e:
            return None

    # Get public IPv6 address by connecting to ipify.org
    def get_ipv6_public(self):
        try:
            return get('https://api64.ipify.org').text
        except Exception as e:
            return None

def local():
    return GetIPLogic().get_ipv4()

def localv4():
    return GetIPLogic().get_ipv4()

def localv6():
    return GetIPLogic().get_ipv6()

def public():
    return GetIPLogic().get_ipv4_public()

def publicv4():
    return GetIPLogic().get_ipv4_public()

def publicv6():
    return GetIPLogic().get_ipv6_public()

def hostname(pub=False):
    return socket.gethostname()

