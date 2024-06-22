
from typing import Any, Dict, List, Optional, Tuple
from typing_extensions import TypeAlias
from network import Network

class Table:

    def __init__(self) -> None:
        self.networkMap : Dict[str , List[Network]] = {}
        self.updateMessageMap: Dict[str, List[Network]] = {}

    def add_network(self, network_addr: str, network: Network) -> None:
        if network_addr in self.networkMap:
            self.networkMap[network_addr].append(network)
            self.updateMessageMap[network_addr].append(network)
        else:
            self.networkMap[network_addr] = [network]
            self.updateMessageMap[network_addr] = [network]

        self.aggregateNetworks(network_addr)
        print(f"Added new network: {network}")

    def aggregateNetworks(self, ip):
        """
        1. Group them by localpref, selfOrigin, aspath, origin
        2. Perform route aggregation on the groups
        """
        hasSummarized = True
        # keep looping while there are more to summarize
        while hasSummarized:
            hasSummarized = False
            networks = self.networkMap[ip]
            isSummarized = set()
            aggregated_networks = []
            for i in range(len(networks)):
                if i in isSummarized:
                    continue
                for j in range(i + 1, len(networks)):
                    if networks[i].is_summarizable(networks[j]) and networks[i].are_adjacent(networks[j]):
                        print('Summarizing!')
                        new_network = Network(ip, networks[i].network, networks[i].netmask, networks[i].localpref, networks[i].selfOrigin, networks[i].ASPath, networks[i].origin)
                        new_network.summarize_self()
                        aggregated_networks.append(new_network)
                        isSummarized.add(j)
                        hasSummarized = True
                        break
                else:
                    aggregated_networks.append(networks[i])
            self.networkMap[ip] = aggregated_networks

    def rebuildNetworkMap(self, ip: str):

        self.networkMap[ip] = []
        for net in self.updateMessageMap[ip]:
            self.networkMap[ip].append(net)
        
        self.aggregateNetworks(ip)

    def remove_networks_from_peer(self, peer_ip: str, network_list : List[Dict[str, str]]):
        """
            Loops through all peers and when it finds peer that equals the src, it remove all networks from that peer that are advertised in the withdraw
            message
        """
        new_updates = []
        for network_to_remove in network_list:
            for network in self.updateMessageMap[peer_ip]:
                if network_to_remove['network'] == network.network and network_to_remove['netmask'] == network.netmask:
                    continue
                new_updates.append(network)
        
        self.updateMessageMap[peer_ip] = new_updates
        self.rebuildNetworkMap(peer_ip)

    
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

