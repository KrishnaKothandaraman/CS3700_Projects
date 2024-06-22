from ip import tobin, get_bin_prefix_len, summarize_ip

class Network:
    def __init__(self, peer_ip = "", network = "", netmask = "", localpref = 0, selfOrigin = False, ASPath = [], origin = False):
        self.peer_ip = peer_ip
        self.network = network
        self.netmask = netmask
        self.netmask_length = get_bin_prefix_len(netmask)
        self.localpref = localpref
        self.selfOrigin = selfOrigin
        self.ASPath = ASPath
        self.origin = origin
        self.network_bin = tobin(network).replace(".","")
    
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return f"network=\"{self.network}\",netmask=\"{self.netmask}\",localpref={self.localpref},selfOrigin={self.selfOrigin},ASPath={self.ASPath},origin=\"{self.origin}\""

    def __eq__(self, other):
        return self.network == other.network and self.netmask == other.netmask

    def __lt__(self, other):
        if self.localpref < other.localpref:
            return True
        elif (self.localpref == other.localpref) and (not self.selfOrigin and other.selfOrigin):
            return True
        elif (self.localpref == other.localpref) and (self.selfOrigin == other.selfOrigin) and (len(self.ASPath) > len(other.ASPath)):
            return True
        elif (self.localpref == other.localpref) and (self.selfOrigin == other.selfOrigin) and (len(self.ASPath) == len(other.ASPath)) and (self.origin == "UNK" and other.origin in ("IGP", "EGP")) or (self.origin == "EGP" and other.origin == "IGP"):
            return True
        elif (self.localpref == other.localpref) and (self.selfOrigin == other.selfOrigin) and (len(self.ASPath) == len(other.ASPath)) and (self.origin == other.origin) and self.peer_ip > other.peer_ip:
            return True
        else:
            return False

    def are_adjacent(self, other):
        return self.netmask_length == other.netmask_length \
            and tobin(self.network).replace(".", "")[:self.netmask_length - 1] == tobin(other.network).replace(".", "")[:other.netmask_length - 1]

    def is_summarizable(self, other):
        return self.ASPath == other.ASPath and self.localpref == other.localpref and self.origin == other.origin and self.selfOrigin == other.selfOrigin
    
    def summarize_self(self):
        self.network, self.netmask = summarize_ip(self.network, self.netmask)
        self.netmask_length = get_bin_prefix_len(self.netmask)

    def containsIP(self, ip_addr):
        """
        Check if the given ip addr is inside this network.
        bin(network[:netmask]) == bin(ip_addr)
        """
        ip_dest_bin = tobin(ip_addr).replace(".", "")
        # only possible if they give a buggy ip
        if len(ip_dest_bin) != 32:
            print(f"WARINING: Received potentially invalid ip {ip_addr}")
            return False
        return self.network_bin[:self.netmask_length] == ip_dest_bin[:self.netmask_length] 
        
