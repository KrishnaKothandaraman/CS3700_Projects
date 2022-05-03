# CS3700_Projects

This is a documentation of the assignments I did for CS3700 at Northeastern University. The course homepage can be found [here](https://3700.network/).

Detailed README and source code for each individual project can be found in their respective subdirectories.

All the code here is built to be elegant, concise and readable.

### Projects Summary

#### Project 1 - Wordle Bot
- Implemented a Client to play the game of Wordle with a Server using a TCP connection with support for TLS encryption
- Developed a guessing strategy capable of guessing the answer in under 6 tries on average.

#### Project 2 - Simple Bridge
- Implemented a Bridge that is capable of executing the spanning tree algorithm and building a forwarding table to be able to 
forward frames between its various ports.
- Robust implementation that can handle changes to the network like failure of bridges and creation of bridges by automatically reconfiguring the spanning tree.
- Scalable with the addition of extra LANs and Bridges.

#### Project 3 - BGP router
- Created a Router that implements the Border Gateway Protocol that builds and maintains a forwarding table capable of
forwarding packets to their destination IP.
- Router is capable of longest prefix matching, aggregation of IPs and disaggregation of IPs
- Router is smart enough to handle relationships with peers, providers and customers and only forwards data when it is
economically feasible for the router.

#### Project 4 - Reliable Transport Protocol
- Implemented my own version of TCP that guarantees reliable inorder transmission of packets.
- Protocol can detect and recover from
  - Reordered packets
  - Dropped packets
  - Corrupted packets
  - High/low network latency
  - High/low network bandwidth
- Network latency is sampled using both steps of Karn's algorithm to adjust transmission speed
- Additive increase and multiplicative decrease are used to handle high/low bandwidth.

#### Project 5 - Web Crawler
- Implemented a Web Crawler and a HTML parser to crawl a website of over 100,000 pages to find hidden flags.
- Network stack used was HTTP over TLS
- Implemented HTTP communication without the usage of requests library and developed a HTML response parser to parse
server responses.


#### Project 6 - Distributed Key Value store(Raft implementation)
- Implemented the raft consensus protocol for distributed systems that builds and maintains a distributed key value store
- Implementation is able to handle and recover from
  - Lossy networks
  - Leader failures
  - Network partitions(major and minor partitions)
- Strong consistency guarantees and high availability.
- Implementation is based on the original raft paper found [here](https://raft.github.io/raft.pdf).