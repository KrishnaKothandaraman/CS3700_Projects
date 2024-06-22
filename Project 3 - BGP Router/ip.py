
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
