
from typing import Dict, List
from network import Network



class Table:

    def __init__(self):
        self.networkMap : Dict[str , List[Network]] = {}
    
    def add_network(self, network_addr: str, network: Network):
        if network_addr in self.networkMap:
            self.networkMap[network_addr].append(network)
        else:
            self.networkMap[network_addr] = [network]
