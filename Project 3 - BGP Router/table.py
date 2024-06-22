
from typing import Any, Dict, List, Optional
from network import Network



class Table:

    def __init__(self) -> None:
        self.networkMap : Dict[str , List[Network]] = {}
    
    def add_network(self, network_addr: str, network: Network) -> None:
        if network_addr in self.networkMap:
            self.networkMap[network_addr].append(network)
        else:
            self.networkMap[network_addr] = [network]
        print(f"Added new network: {network}")

    def remove_networks_from_peer(self, peer_ip: str, network_list : List[Dict[str, str]]):
        """
            Loops through all peers and when it finds peer that equals the src, it remove all networks from that peer that are advertised in the withdraw
            message
        """
        for peer_addr, networks in self.networkMap.items():
            if peer_addr == peer_ip:
                for network_to_remove in network_list:
                    n = Network(network=network_to_remove["network"], netmask=network_to_remove["netmask"])
                    if n in networks: networks.remove(n)
            
    
    def get_next_hop_router(self, ip_addr: str) -> str:
        """
        Filter all next hop routers in this table that ip_addr belongs to
        """
        filtered_list = []
        for net_addr, networks in self.networkMap.items():
            for net in networks:
                if net.containsIP(ip_addr):
                    filtered_list.append((net_addr, net))
        print(filtered_list)
        return sorted(filtered_list, key = lambda x: x[1], reverse=True)[0][0] if len(filtered_list) > 0 else ""
    
    def dump(self) -> List[Dict[str, Any]]:
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

