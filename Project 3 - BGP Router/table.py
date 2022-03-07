from network import Network
from typing import Dict, List, Tuple, Optional
import ip


# represents the routing table
class Table:
    routing_table: List[Tuple[Network, str]]

    def __init__(self):
        self.routing_table = []

    # add an entry to the table with given message
    def add_entry(self, message):
        neighbor_ip = message["src"]
        network = Network(message)

        # just in case the neighbor changes its "network-netmask" fields in msg
        self.routing_table.append((network, neighbor_ip))
        self.aggregate()

    def get_adjacent_networks(self, other: Network, aggregation_map: Dict[int, int]) -> Optional[int]:
        """
        Return list of indices of networks from routing table that are adjacent to a given network
        :param aggregation_map: Dictionary of already processed networks
        :param other: Network instance
        :return: List[int]
        """
        for i, (network, neighbour) in enumerate(self.routing_table):
            if i in aggregation_map or network == other:
                continue
            if ip.are_adjacent(other.network, other.netmask, network.network, network.netmask):
                return i

    def aggregate(self) -> None:
        """
        aggregate the routing_table if possible
        :return: None
        """
        aggregation_map: Dict[int, int] = {}
        for i, (network, neighbour) in enumerate(self.routing_table):
            adjacent_network = self.get_adjacent_networks(network, aggregation_map)
            if not adjacent_network:
                continue
            aggregate_network = self.get_aggregate_networks(network, adjacent_network)
            if not aggregate_network:
                continue
            aggregation_map[i] = aggregate_network
            print(
                f"{network.serialize()} Aggregatable networks: {self.routing_table[aggregate_network][0].serialize()}")

        for network, adjacent_network in aggregation_map.items():
            if not adjacent_network:
                continue
            self.routing_table.pop(adjacent_network)

            self.routing_table[network][0].network = ip.aggregate_network(self.routing_table[network][0].network,
                                                                          self.routing_table[network][0].netmask)
            self.routing_table[network][0].netmask = ip.aggregate_netmask(self.routing_table[network][0].netmask)

        if len(aggregation_map) > 0:
            self.aggregate()

    def get_aggregate_networks(self, network, adjacent_network) -> Optional[int]:
        """
        Removes adjacent networks that cannot be aggregated with network
        :param network: Base network
        :param adjacent_network: index of adjacent network from routing table
        :return: List[int]
        """
        for i, (peer_network, neighbour) in enumerate(self.routing_table):
            if i != adjacent_network:
                continue
            if not network.have_same_attributes(peer_network):
                return None
        return adjacent_network

    # remove the dead entry from the forwarding table
    def withdraw(self, message):
        networks_to_remove = message["msg"]
        for route in self.routing_table:
            if route[1] == message["src"]:
                for network in networks_to_remove:
                    if route[0].network == network["network"] and route[0].netmask == network["netmask"]:
                        self.routing_table.remove(route)

    def find_route(self, destination: str) -> List[Network]:
        """
        checking if the given destination is in the table or not;
        if it is returns the corresponding neighbor's IP.
        :param destination: IP
        :return: neighbor's IP
        """
        valid_networks = []
        for network, neighbour in self.routing_table:
            can_route = network.prefix_match(destination)
            if can_route:
                valid_networks.append(network)
        return valid_networks

    def get_serialized_table(self) -> List:
        """
        Returns serialized representation of forwarding table
        :return: List of dictionaries of the forwarding table
        """
        return list(map(lambda x: x[0].serialize(), self.routing_table))
