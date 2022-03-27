# Project 4 - Reliable Transport Protocol

## Code Design and Structure

### Main Classes

### Sender

- This class contains the main logic to mimic a sender during TCP data exchange.
- The sender is responsible for processing acks and data read from stdin
- The sender is also responsible for keeping track of packet timeouts and 
adjusting the RTT estimates.
- For this project I used both steps of Karn's algorithm for RTT sampling.
- The sender also detects acks that have been dropped by the network by 
looking at the "sack" field of the response. This ensures that packets received do not get retransmitted.
- The sender class is also able to adjust timeouts of packets sent during bad network conditions using
the reset_expiry function.
- This class controls the window and adjusts it based on the network conditions.

### SenderWindow

- This class is the implementation of a sender side memory buffer
- It has methods to add data and retrieve data to be sent from the buffer.
- The window also contains logic to increase and decrease the maximum transmission window size.

### Receiver

- This class contains the logic for a receiver during TCP data exchange.
- The receiver validates the message received using the checksum. If it is valid, it adds it to the
receiver side buffer and responds with an ack.
- This class is also responsible for printing data in an ordered fashion

### ReceiverWindow

- This class mimics a TCP buffer on the receiver side.
- The main methods in this class are the add and flush methods which add data to the buffer and return
ordered data from the buffer respectively.

## Challenges faced

- At the start, I was a bit too ambitious and tried to implement selective acknowledgment. This was not a good decision
as I got overwhelmed with the different cases possible and began writing bad code. I decided to simplify my process and
implement the methods suggested in the project spec. This made the implementation easier to handle.
- The sender side window was complicated to implement for the case where packets get reordered by the network. Since
sliding of the window depended on the acks, it took me some time to come up with logic that was capable of handling network
scenarios in the future tests.
- One major challenge I faced was the 8-3 test. My code was not adjusting past increased packet timeouts when the network condition
became better. I fixed this issue by writing the reset_expiry method in Sender.

## Features of good design.
- One feature of good design that I always judge my code with is : How much old code do I need to rewrite to implement a new feature?
Because of my rather robust and scalable window implementations, I did not have to rewrite any old code to pass higher level tests.
The implementation of the receiver window did not change after the implementation of the second level test.
- Since I implemented both features of Karn's algorithm, my code is able to quickly improve when network conditions get better
and also slow down when network conditions get worse.
- The implementations of the Window allowed for unit testing, and I was able to catch bugs even before running the whole code.

## How I tested my code
- Apart from using the tests given to me, I tested my code by changing some seeds to make sure it works in all
possible conditions.
- I wrote unit tests for my window classes and made sure that they work in a number of different scenarios.