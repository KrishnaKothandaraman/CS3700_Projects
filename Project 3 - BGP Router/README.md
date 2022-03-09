# Project 3 - BGP Router

## Code Design and Structure

The code was designed in a modular and object oriented manner such that each individual component can be tested
individually.

### The main classes

#### Router

- This class represents our main router and is the highest level class.
- It is responsible for initialization, communication and data filtering and processing.
- The router performs basic data validation and then filters the message based on their type. Once filtered, the 
message is handed of to the agent responsible for processing it. This could be another class or another method in the 
router class.
- This class also contains all logic regarding sending the message over the socket.

#### Table

- This class represents the forwarding table of the router.
- The table is stored as a mapping of a Network object to a peer IP where the Network
object contains all necessary route related information to make routing decisions.
- The table is responsible for finding the entries from the routing table that match a given destination IP.
- The table also contains methods for aggregation and disaggregation.

#### Network

- This class is mainly used to store data related to route announcements. Each instance of this class represents a
network that our router can forward to.
- The class also contains serialization methods that make the response to the "dump" message easy.
- The definition of a __lt__ dunder method makes sorting the networks easy so the best network can be found by the router
without the router having to worry about the implementation details of the network itself adding a layer of abstraction.

#### ip.py

- Even though this is not a class, this file contains all the helper methods we wrote related to processing of IP
addresses such as
  - Converting from dotted string notation to binary
  - Converting binary notation back to string notation
  - Getting the length of the CIDR mask
  - Validating the netmask and the IP
- These are only a few examples of the functions we implemented


## Challenges we faced

#### Sorting Networks
- To pass the level 2 tests, we decided not to take the easy way out and decided to implement a sorting function into our networks
from the start. This was a non-trivial task as comparisons of different attributes required different logic and sometimes needed
helper methods. E.g. comparison of the peer IP required the definition of the compare_IPs function in ip.py. There were quite 
a few bugs we had to solve and this step was rather time-consuming.
#### Aggregation
- The logic for aggregation was rather convoluted and required some good design to have it done in a reliable manner. This again
took some time and clever design
#### Disaggregation
- This was the hardest problem we faced as we tried at the very start to design an algorithm that is performant. We quickly descended
into a difficult situation as we had to keep adding data structures and it soon got out of hand. In the end, we settled for a
functional approach over an overoptimistic one.

## Features of good design
### Learning from our mistakes

- After the last BPDU project, we decided that this time we will not write a line of code until we know the design of our 
project. So we sat down and planned the entire layout and all the classes we would need.
- The result of this planning was that for every new feature we added, we never had to redesign the codebase - something that happened
a few times with the bridge project.
- The modularity of our classes makes for clear distinction of responsibilities and also allowed each class to be tested 
individually.
- Defining the __lt__ dunder method in Networks allowed for a very simple method of picking the best Network if there were multiple
ties. We can see a universe where we did not implement this and wrote a bunch of confusing if checks to break ties.
- All the functions in ip.py are quite well written and provide us with all the functionality we would need to do this project without
relying on any external tools.
- The serialize methods in Table also make for clean code in the router class

## How we tested the code

- Aside from running the tests given to us, we also tested each class individually to ensure that functionality was maintained.
- This involved creating instances of the class with mock data and testing the various methods to ensure correctness.
