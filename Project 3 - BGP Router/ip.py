
class InvalidIPException(Exception):
    def __init__(self, ip: str, message: str) -> None:
        self.ip = ip
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        print(f"{self.ip}: {self.message}")


class InvalidCIDRException(Exception):
    def __init__(self, netmask: str, message: str) -> None:
        self.ip = netmask
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        print(f"{self.ip}: {self.message}")


def validIP(ip: str) -> bool:
    """
    Returns True if IP is valid and False otherwise
    :param ip: IPv4 address as string
    :return: bool
    """
    ip_split = ip.split(".")

    return len(ip_split) == 4 and all(map(lambda x: x.isdecimal() and 0 <= int(x) <= 255, ip_split))


def tobin(ip: str) -> str:
    """
    Returns the string representation of the IP address in binary

    :return: continuous string representation of 32 bit ipv4 address
    """

    if not validIP(ip):
        raise InvalidIPException(ip, "Invalid ipv4 address")

    return "".join(map(str, ["{0:08b}".format(int(ip)) for ip in ip.split(".")]))


def validNetmask(netmask: str) -> bool:
    """
    Returns bool representing validity of this netmask
    :param netmask: netmask as an ipv4 address
    :return: bool
    """
    netmask_bin_split = tobin(netmask).split('0')

    return all(map(lambda x: len(x) == 0, netmask_bin_split[1:]))


def cidr_length(netmask: str) -> int:
    """
    returns CIDR length
    :return: integer
    """

    if not validIP(netmask) or not validNetmask(netmask):
        raise InvalidCIDRException(netmask, "Invalid CIDR mask")

    return max(map(len, tobin(netmask).split('0')))


def compareIP(ip1: str, ip2: str) -> bool:
    """
    True if ip1 < ip2
    :param ip1: ipv4 address in dotted notation
    :param ip2: ipv4 address in dotted notation
    :return: boolean
    """

    if not validIP(ip1):
        raise InvalidIPException(ip1, "Not a valid IP")
    if not validIP(ip2):
        raise InvalidIPException(ip2, "Not a valid IP")

    return ip1.split(".") < ip2.split(".")


def are_adjacent(ip1: str, netmask1: str, ip2: str, netmask2: str) -> bool:
    """
    Returns a boolean True if ip1, netmask1 and ip2, netmask2 are adjacent
    :param ip1: ipv4 as string
    :param netmask1: netmask as string
    :param ip2: ipv4 as string
    :param netmask2: netmask as string
    :return: bool
    """

    if not validIP(ip1) or not validIP(ip2):
        raise InvalidIPException(ip1, "Not valid IP")
    if not validNetmask(netmask2) or not validNetmask(netmask1):
        raise InvalidCIDRException(netmask1, "Not valid netmask")

    cidr1 = cidr_length(netmask1)
    cidr2 = cidr_length(netmask2)

    if cidr1 != cidr2:
        return False
    if tobin(ip1)[:cidr1 - 1] != tobin(ip2)[:cidr2 - 1]:
        return False
    return True


def aggregate_network(ip: str, netmask: str) -> str:
    """
    generates the aggregated network with given ip and netmask
    :param ip: the ip needed to me aggregated
    :param netmask: the ip's netmask
    :return: a tuple of aggregated network ip and netmask
    """
    CIDR = cidr_length(netmask) - 1
    binary_ip = tobin(ip)[:CIDR]
    num_of_zero_to_bind = 32 - len(binary_ip)
    binary_ip += "0" * num_of_zero_to_bind
    return binary_to_dot_ip(binary_ip)


def aggregate_netmask(netmask: str):
    """
    generating the netmask of aggregation
    :param netmask: the current netmask
    :return: the netmask for aggregated networks
    """
    new_netmask = ""
    CIDR = cidr_length(netmask) - 1
    num_of_zero_to_bind = 32 - CIDR
    new_netmask += "1" * CIDR
    new_netmask += "0" * num_of_zero_to_bind
    return binary_to_dot_ip(new_netmask)


def binary_to_dot_ip(binary_ip: str):
    """
    convert the given binary_ip to a doted ip:
    "11111111000000001111111100000000"  ->  "255.0.255.0"
    :param binary_ip:
    :return:
    """
    result = ""
    accu_num = 0  # keep track of the number in base 10
    accu_str = ""  # keep track of str in bytes
    for i in range(4):
        for j in range(8):
            accu_str += binary_ip[j + i * 8]
        # int("01010101", 2): converting binary to integer
        accu_num += int(accu_str, 2)
        if i == 3:
            result += str(accu_num)
        else:
            result += str(accu_num) + "."
        accu_str = ""
        accu_num = 0
    return result


if __name__ == "__main__":
    ip1 = "192.168.2.0"
    netmask = "255.255.255.0"
    ip2 = "192.168.3.0"
    print(are_adjacent(ip1, netmask, ip2, netmask))
    print(aggregate_network(ip1, netmask))
    print(aggregate_netmask(netmask))

    # print(compareIP(ip1, ip2))
    # ip3 = tobin("128.a.0.982")
    CIDR = cidr_length("255.128.0.0")
