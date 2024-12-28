import subprocess
from requests import get
import socket
import re

class getIP_logic:
    def getIPv4():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("69.69.69.69", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    
    # TODO: Only works on Linux
    # Credit: https://tech-bloggers.in/get-ipv6-info-using-python/
    def getIPv6():
 
        # Execute the ifconfig command
        output = subprocess.check_output(["ifconfig"])

        # Extract the IPv6 address using regular expressions
        ipv6_pattern = r"inet6 ([\da-fA-F:]+)"
        ipv6_address = re.findall(ipv6_pattern, str(output))

        # Print the IPv6 address
        print(ipv6_address[0])
    
    # Get public IPv4 address by connecting to ipify.org
    def getIPv4_public():
        return get('https://api.ipify.org').text

    # Get public IPv6 address by connecting to ipify.org
    def getIPv6_public():
        output = get('https://api64.ipify.org').text
        # Extract the IPv6 address using regular expressions
        ipv6_pattern = r"inet6 ([\da-fA-F:]+)"
        ipv6_address = re.findall(ipv6_pattern, str(output))
        return ipv6_address[0]

def local():
    return getIP_logic.getIPv4()

def localv4():
    return getIP_logic.getIPv4()

def localv6():
    return getIP_logic.getIPv6()

def Public():
    return getIP_logic.getIPv4_public()

def Publicv4():
    return getIP_logic.getIPv4_public()

def Publicv6():
    return getIP_logic.getIPv6_public()

def Hostname(pub=False):
    return socket.gethostname()

