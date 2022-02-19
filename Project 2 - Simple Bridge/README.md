# Project 2 - Simple Bridge

## Code Design and Structure

The code has been designed in a fully object oriented manner with 3 main classes to represent
the components in the bridge.

#### Class BPDU

The Bridge Protocol Data Unit stores all information that is required in a BPDU
message for configuration of the spanning tree. Some of its main features are
- Definitions of less than, greater than and equals object methods to make comparison and sorting of BPDUS simple. These methods also add a layer of abstraction as the Ports can compare BPDUs using basic logical operations without worrying about the details of the comparison implementations.
- Storage of time data to calculate if a BPDU has expired or not. The implementation of this method allows flexibility in the design of the protocol as expiry times are not rigid and provide a single point where changes reflect in all usages of the BPDU class.
- Methods to serialize and unserialize BPDUs for cleaner code.

#### Class Port

This class encapsulates all the data and methods required to implement a Port on a bridge. All logic with regard to BPDU storage and comparison take place in this class. Some of its main features are
- Storage of Port status as either DESIGNATED,DISABLED or ROOT. This data is stored as an enumeration of another Class PortStatus. This design allows for a single point of change and flexibility to add more types of Port status.
- Stores a list of all BPDUs that the Port has heard and performs logic on the list such as
  - Filtering out expired BPDUs
  - Returning the best BPDU that the Port has ever heard
  - Managing timestamps of the BPDU when the same BPDU has been heard multiple times.
- Sending messages through UDP connection in JSON format.

#### Class Bridge

This is the highest level class that contains all the data and logic required for the functioning of the Bridge. It contains a list of all Ports on it as well as a forwarding table. Some of its main features are
- Message processing
  - If the message received is a BPDU, the Bridge executes the algorithm to reconfigure its Ports based on the spanning tree protocol through the "update" method.
  - If the message received is data, the Bridge executes the algorithm to forward the message through the "process_message" method.
- Sending BPDUs only when they are needed. The Bridge sends BPDUs only in the following cases
  - When it first starts up
  - When it has been more than half a second since the last one was sent
  - When there is a change to the Bridge's root or path to the root
  - When the Bridge hears a BPDU it has never heard before
- The bridge also builds a forwarding table by storing the port where the source of he message was heard
  - The bridge then forwards the message to the destination port if it is saved or forwards it out on all non-dsiabled ports apart from which it received it on
  - It flushes/clears the forwarding table when it detects a change to the spanning tree


## Features of good design

- Creating classes for all the major objects in the Bridge with each class containing only the data and methods that it requires
- Creating helper functions in a generic manner that help reduce code repetition.
- Clean and concise code using higher order functions such as filters and lambdas to remove verbose code.
- Creation of single points of change wherever we could to ensure that code remains flexible and robust
- Good goodput and 100% packet delivery on performance-3 tests

## Challenges faced

- The first and biggest challenged we face was definitely understanding the requirements completely. We thought we had understood it but realized a mistake only once we started writing the code. Since our first few designs were not properly thought through, we decide to rewrite the entire thing again

- We found the comparison of BPDUs extremely difficult as there are several levels to the comparison. In our first instance where we had not created a BPDU class, we could not figure out the comparison correctly and this led to hair bending bugs. Once we created comparison methods however, it became trivial.

- Figuring out the spanning tree in general is chalenging. We did not store all the BPDUs heard on each port which theoratically can pass the milestone2 but would cause us problems for improving the performance. Once we figured out a good method of storing the Bridge's own best BPDU, this issue became easier to solve.

### Tests that casued us issues and how we resolved them
- __simple-7.conf__ caused a lot of issues for us especially because of our initial code design. The fact that the root port was connected to the same LAN multiple times was a difficult thing to solve and to fix this issue, we had to redesign the entire Bridge class again.

- __intermediate-3.conf__ had a very particular bug that stopped the spanning tree from reconfiguring itself quickly when a new bridge was added. Initially, we checked if our last BPDU was sent less than half a second ago only when we received BPDUs and not when we received data messages. Therefore, when the bridge received data messages for more than a few seconds, it was never sending BPDUs even if the half second threshold was met. We found this error by painstakingly going through each line in the output.

- __advanced-3.conf__ had a similar issue as intermediate-3 but here we were not rebroadcasting our own BPDU when the Bridge heard a BPDU it has never seen before. This stopped the spanning tree from being reconfigured quickly enough and led to a low goodput.

### Code Testing Process

- Since we designed the code as objects, we tested each object first to make sure they are working as expected.
- Randomized seeds in all test cases to stress test the bridge under different circumstances
- We also deleted and added a few extra bridges and LANs to the test configurations and checked the behaviour of our code against the expected behaviour which we solved on paper.
