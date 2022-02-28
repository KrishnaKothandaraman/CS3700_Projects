#!/usr/bin/env python3


# Definition of a port
import json
import socket

# Enumeration of various Port states
from enum import Enum

from bpdu import BPDU


class PortStatus(Enum):
    DISABLED = 0
    ROOT = 1
    DESIGNATED = 2


class Port:
    def __init__(self, id, lan_port):
        """
        This class represents a port on a bridge
        :param id: 0-indexed id of the port
        :param lan_port: UDP port number of the LAN
        """
        self.id = id
        self.lan_port = lan_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('localhost', 0))
        # list of bpdus received by this port
        self.bpdus_received = []
        # status of this port. Either designated, root or disabled
        self.status = PortStatus.DESIGNATED

    # returns a bool indicating if this port is active or not d
    def is_active(self) -> bool:
        return self.status != PortStatus.DISABLED

    # returns True if bpdu has not expired and False if it has
    def is_valid_bpdu(self, bpdu: BPDU) -> bool:
        return not bpdu.is_expired()

    # cleans list of bpdus heard to remove expired ones
    def clean_bpdus(self):
        self.bpdus_received = list(filter(self.is_valid_bpdu, self.bpdus_received))

    # return the best bpdu that this port heard
    def get_best_bpdu(self):
        if len(self.bpdus_received) > 0:
            return sorted(self.bpdus_received)[0]
        else:
            return BPDU(args.bridge_id, 0, args.bridge_id, self.id)

    # convenience method that returns list of serialized BPDUs for debugging
    def return_serialized_list(self):
        return list(map(lambda p: p.serialize(), self.bpdus_received))

    def has_received_bpdu(self):
        """
        Return bool indicating if this port has received a BPDU

        :return: True if port has heard a bpdu, False otherwise
        """
        return len(self.bpdus_received) == 0

    # This method sends a BPDU on this port.  Right now, it only sends a
    # BPDU that says this bridge believes its the root; obviously, this
    # will need to be updated.
    def send_bpdu(self, bpdu):
        self.send(json.dumps({"source": bpdu["id"],
                              "dest": "ffff",
                              "msg_id": 0,
                              "type": "bpdu",
                              "message": bpdu
                              }).encode('utf-8'))

    # This method sends the provided byte array "data" to the LAN, using the
    # UDP connection.
    def send(self, data):
        print("Sending message on port %d" % self.id, flush=True)
        self.socket.sendto(data, ('localhost', self.lan_port))

    def try_to_add_new_bpdu(self, bpdu: dict) -> bool:
        """
        This function checks if a BPDU received is already seen before. If so, it returns False.
        Otherwise, it returns True and adds it to the list of already seen BPDUs

        :param bpdu: BPDU object to be added to the port
        :return: Boolean True if BPDU has never been seen before, False if BPDU has been seen before
        """
        self.clean_bpdus()
        BPDU_obj = BPDU(bpdu["root"], bpdu["cost"], bpdu["id"], bpdu["port"])
        if BPDU_obj in self.bpdus_received:
            # remove old one
            self.bpdus_received.remove(BPDU_obj)
            # add new one with new time
            self.bpdus_received.append(BPDU_obj)
            return False
        else:
            self.bpdus_received.append(BPDU_obj)
            return True
