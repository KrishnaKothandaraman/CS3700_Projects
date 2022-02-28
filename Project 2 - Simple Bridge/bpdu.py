#!/usr/bin/env python3

# for a bridge, this class represents:
# a bpdu message it receives and the port it receives the message on
import datetime


class BPDU:
    def __init__(self, root, cost, bridge_id, port_sent_from):
        self.root = root
        self.cost = cost
        self.bridge_id = bridge_id
        self.port_sent_from = port_sent_from
        self.created_on = datetime.datetime.now()

    # returns the bpdu message dictionary of self
    def serialize(self):
        return {"id": self.bridge_id,
                "root": self.root,
                "cost": self.cost,
                "port": self.port_sent_from}

    # returns bool indicating whether a BPDU has expired
    def is_expired(self) -> bool:
        return (datetime.datetime.now() - self.created_on).total_seconds() > 0.8

    # returns the bpdu object given
    def unserialize(message):
        BPDU(message["root"], message["cost"],
             message["id"], message["port"])

    def __tuple__(self):
        return self.root, self.cost, self.bridge_id, self.port_sent_from

    def __lt__(self, other):
        return self.__tuple__() < other.__tuple__()

    def __le__(self, other):
        return self == other or self.__tuple__() < other.__tuple__()

    def __gt__(self, other):
        return self.__tuple__() > other.__tuple__()

    def __ge__(self, other):
        return self == other or self.__tuple__() > other.__tuple__()

    def __eq__(self, other):
        return self.root == other.root and self.cost == other.cost and \
               self.bridge_id == other.bridge_id and self.port_sent_from == other.port_sent_from

    def __str__(self):
        return "{root: %s, cost: %s, id: %s, port %s}" % \
               (self.root, self.cost, self.bridge_id, self.port_sent_from)
