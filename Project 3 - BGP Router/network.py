import copy
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Tuple
import ip


class Network:
    peer: str
    network: str
    netmask: str
    localpref: int
    selfOrigin: bool
    ASPath: List[int]
    origin: str

    def __init__(self, update_message):
        object.__setattr__(self, 'peer', (update_message["src"]))
        object.__setattr__(self, 'network', (update_message["msg"]["network"]))
        object.__setattr__(self, 'netmask', (update_message["msg"]["netmask"]))
        object.__setattr__(self, 'localpref', update_message["msg"]["localpref"])
        object.__setattr__(self, 'selfOrigin', update_message["msg"]["selfOrigin"])
        object.__setattr__(self, 'ASPath', update_message["msg"]["ASPath"])
        object.__setattr__(self, 'origin', update_message["msg"]["origin"])

    def __lt__(self, other):
        if ip.cidr_length(self.netmask) > ip.cidr_length(other.netmask):
            return True
        elif ip.cidr_length(self.netmask) == ip.cidr_length(other.netmask) and self.localpref > other.localpref:
            return True
        elif ip.cidr_length(self.netmask) == ip.cidr_length(other.netmask) and self.localpref == other.localpref \
                and (self.selfOrigin is True and other.selfOrigin is not True):
            return True
        elif ip.cidr_length(self.netmask) == ip.cidr_length(other.netmask) and self.localpref == other.localpref \
                and (self.selfOrigin == other.selfOrigin) and len(self.ASPath) < len(other.ASPath):
            return True
        elif ip.cidr_length(self.netmask) == ip.cidr_length(other.netmask) and self.localpref == other.localpref \
                and (self.selfOrigin == other.selfOrigin) and len(self.ASPath) == len(other.ASPath) \
                and self.compareOrigins(other) == 1:
            return True
        elif ip.cidr_length(self.netmask) == ip.cidr_length(other.netmask) and self.localpref == other.localpref \
                and (self.selfOrigin == other.selfOrigin) and len(self.ASPath) == len(other.ASPath) \
                and self.compareOrigins(other) == 0 and ip.compareIP(self.peer, other.peer):
            return True
        else:
            return False

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"{self.__dict__}"

    def have_same_attributes(self, other) -> bool:
        """
        Returns True if two networks have same attributes
        :param other: Other network
        :return:
        """
        return self.peer == other.peer and self.netmask == other.netmask and self.localpref == other.localpref \
            and (self.selfOrigin == other.selfOrigin) and len(self.ASPath) == len(other.ASPath) \
            and self.compareOrigins(other) == 0

    def serialize(self) -> dict:
        """
        Method returns a dictionary representation of the entire class. Useful for dump message
        :return: dictionary representation of this class
        """
        return self.__dict__

    def serialize_for_forwarding(self, asn: int) -> dict:
        """
        Call this method to return dictionary for forwarding update message to neighbours
        :return: dictionary representation of non private fields of this network
        """
        return {"network": self.network, "netmask": self.netmask, "ASPath": [asn] + self.ASPath}

    def prefix_match(self, ipaddr) -> bool:
        """
        Call this method to check if an IPaddress is in a network
        :param ipaddr: str representation of IP Address
        :return: boolean representing whether this network has this IP address
        """
        CIDR = ip.cidr_length(self.netmask)
        return ip.tobin(self.network)[:CIDR] == ip.tobin(ipaddr)[:CIDR]

    def compareOrigins(self, other) -> int:
        """
        C-style comparison operator. 0 implies equals, 1 implies self > other and -1 implies self < other
        :param other: Instance of type Network
        :return: int
        """
        if self.origin == other.origin:
            return 0
        elif self.origin == "IGP" and other.origin != "IGP":
            return 1
        elif self.origin == "EGP" and other.origin == "UNK":
            return 1
        return -1