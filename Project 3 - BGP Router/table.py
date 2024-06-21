
from typing import Dict, List, Optional
from network import Network



class Table:

    def __init__(self):
        self.networkMap : Dict[str , List[Network]] = {}
    
    def add_network(self, network_addr: str, network: Network):
        if network_addr in self.networkMap:
            self.networkMap[network_addr].append(network)
        else:
            self.networkMap[network_addr] = [network]
        print(f"Added new network: {network}")

    
    def get_next_hop_router(self, ip_addr) -> Optional[str]:
        """
        Filter all next hop routers in this table that ip_addr belongs to
        """
        filtered_list = []
        for net_addr, networks in self.networkMap.items():
            for net in networks:
                if net.containsIP(ip_addr):
                    filtered_list.append((net_addr, net))

        assert len(filtered_list) <= 1, "No support for multiple next hop routers yet"
        return filtered_list[0][0] if len(filtered_list) == 1 else ""
    
    def dump(self):
        """
            Returns table dump
        """
        network_list = []
        for peer_addr, networks in self.networkMap.items():
            for network in networks:
                network_entry = {
                    'peer': peer_addr,
                    "network": network.network,
                    "netmask": network.netmask,
                    "localpref": network.localpref,
                    "ASPath": network.ASPath,
                    "selfOrigin": network.selfOrigin,
                    "origin": network.origin
                }
                network_list.append(network_entry)
        return network_list

