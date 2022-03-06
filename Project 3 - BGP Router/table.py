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

    def aggregate(self):
        """
        aggregate the routing_table if possible
        :return: None
        """
        for i in range(len(self.routing_table)):
            routi = self.routing_table[i]
            network1 = self.routing_table[i][0].network
            netmask1 = self.routing_table[i][0].netmask
            for j in range(i + 1, len(self.routing_table)):
                routj = self.routing_table[j]
                network2 = self.routing_table[j][0].network
                netmask2 = self.routing_table[j][0].netmask
                if self.routing_table[i][0] == self.routing_table[j][0] and ip.are_adjacent(network1, netmask1,
                                                                                            network2, netmask2):
                    self.routing_table.remove(routi)
                    self.routing_table.remove(routj)
                    aggregated_network = ip.aggregate_network(network1, netmask1)
                    aggregated_netmask = ip.aggregate_netmask(netmask1)
                    print("aggregating network: %s" % aggregated_network)
                    print("aggregating netmask: %s" % aggregated_netmask)
                    new_route1 = self.generate_route(routi, aggregated_network, aggregated_netmask)
                    new_route2 = self.generate_route(routj, aggregated_network, aggregated_netmask)
                    self.routing_table.append(new_route1)
                    self.routing_table.append(new_route2)

    def generate_route(self, net_messages: tuple[Network, str], network: str, netmask: str):
        """
        replace the given route with the given network and netmask
        :param net_messages:
        :param network: aggregated network
        :param netmask: aggregated netmask
        :return: the updated routing tuple
        """
        # print("aggregating network: %s" % network)
        # print("aggregating netmask: %s" % netmask)
        message = {"src": net_messages[1],
                   "msg": {"network": network,
                           "netmask": netmask,
                           "localpref": net_messages[0].localpref,
                           "selfOrigin": net_messages[0].selfOrigin,
                           "ASPath": net_messages[0].ASPath,
                           "origin": net_messages[0].origin}
                   }
        new_network = Network(message)
        new_route = [new_network, net_messages[1]]
        return new_route

    # remove the dead entry from the forwarding table
    def withdraw(self, message):
        networks_to_remove = message["msg"]
        for route in self.routing_table:
            if route[1] == message["src"]:
                for network in networks_to_remove:
                    if route[0].network == network["network"] and route[0].netmask == network["netmask"]:
                        self.routing_table.remove(route)
        self.aggregate()

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
