

class Network:
    def __init__(self, network, netmask, localpref, selfOrigin, ASPath, origin):
        self.network = network
        self.netmask = netmask
        self.localpref = localpref
        self.selfOrigin = selfOrigin
        self.ASPath = ASPath
        self.origin = origin