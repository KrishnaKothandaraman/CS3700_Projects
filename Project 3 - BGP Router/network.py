from ip import tobin, get_bin_prefix_len

class Network:
    def __init__(self, network, netmask, localpref, selfOrigin, ASPath, origin):
        self.network = network
        self.netmask = netmask
        self.netmask_length = get_bin_prefix_len(netmask)
        self.localpref = localpref
        self.selfOrigin = selfOrigin
        self.ASPath = ASPath
        self.origin = origin
        self.network_bin = tobin(network).replace(".","")
    
    def __str__(self):
        return f"network={self.network},netmask={self.netmask},localpref={self.localpref},selfOrigin={self.selfOrigin},ASPath={self.ASPath},origin={self.origin},networkBin={self.network_bin}"
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
        
