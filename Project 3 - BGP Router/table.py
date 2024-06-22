
from typing import Any, Dict, List, Optional, Tuple
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
        Filter all next hop routers in this table that ip_addr belongs to.

        1. Check for longest prefix match
        2. If multiple longest prefixes exist, sort and return head
        """
        filtered_list: List[Tuple[str, Network]] = []
        for net_addr, networks in self.networkMap.items():
            for net in networks:
                if net.containsIP(ip_addr):
                    filtered_list.append((net_addr, net))
        # no route
        if len(filtered_list) == 0:
            return ""
        
        # find longest prefix match in filtered_list
        max_prefix = max(list(map(lambda x: x[1].netmask_length, filtered_list)))
        print(max_prefix)
        # filter only entries that are equal to max prefix
        filtered_list = list(filter(lambda x: x[1].netmask_length == max_prefix, filtered_list))
        print(filtered_list)
        # reverse sort and return next hop of head
        return sorted(filtered_list, key = lambda x: x[1], reverse=True)[0][0]
    
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

