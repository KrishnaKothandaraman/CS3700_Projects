
from typing import List, Tuple


def tobin(ip_addr: str) -> str:
    quads = ip_addr.split(".")
    if len(quads) != 4:
        print(f"ERROR: Invalid ip addr provided to tobin {ip_addr}")
        return ""

    binary = '.'.join([str(bin(int(quad)))[2:].zfill(8) for quad in quads])
    return binary

def get_bin_prefix_len(ip_addr: str) -> int:
    bin_ip = tobin(ip_addr)

    bin_ip = bin_ip.replace(".", "")
    
    return len(bin_ip.split('0')[0])

def toip(bin_ip: str) -> str:
    quads = bin_ip.split(".")
    if len(quads) != 4:
        print(f"ERROR: Invalid bin addr provided to tobin {bin_ip}")
        return ""
    # I am so proud of this
    return ".".join([str(sum(map(lambda x: 2**(7-x[0])*int(x[1]), list(enumerate(quad))))) for quad in quads])

def summarize_ip(ip, netmask) -> Tuple[str, int]:
    netmask_length = get_bin_prefix_len(netmask)
    # Ugly function. Fix this crap
    ip_list = list(tobin(ip).replace(".",""))
    ip_list[netmask_length - 1] = '0'
    netmask_list = list(tobin(netmask).replace(".", ""))
    netmask_list[netmask_length - 1] = "0"

    ip_new = ""
    netmask_new = ""
    for i in range(4):
        ip_new += "".join(ip_list[(8*i):8*(i+1)]) + "."
        netmask_new += "".join(netmask_list[(8*i):8*(i+1)]) + "." 
    

    return (toip(ip_new[:-1]), toip(netmask_new[:-1]))

    