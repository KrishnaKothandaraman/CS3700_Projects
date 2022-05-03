# Project 6 Distributed Key Value Store(Raft implementation)

## Code Structure and high level approach

There are three main classes that handle all the function required in this project. Replica and Statemachine and LogEntry

### Replica

- This class is a representation of a replica in the raft consensus protocol
- Using an enum of ServerState, we are able to extract differential behaviour based on the state of a server
- All the logic to perform elections, generate and process RPCs and maintain log consistency are handled in this class
- This class also performs the logic to handle client get and put requests

### StateMachine

- This class is an implementation of the StateMachine described in the Raft paper
- It contains a log, which is a list of LogEntries and pointers to keep track of what has been committed and what has been applied
to the local statemachine.
- It also contains convenience methods that are used by the replica to extract useful information from the log

### Log Entry
- This class(more a dataclass) stores the information regarding a log entry.
- It contains useful getters and setters that are used by the other classes


## Challenges faced

- Honestly speaking, this entire project was a challenge. We had to rewrite our code 3 different times and every new test case
seemed to bring up new errors that required us to rethink our entire approach.
- The unreliable network tests exposed a flaw in how we were counting majorities. Retransmitted requests and duplicated messages
were double counted
- The crash tests showed us a fundamental flaw in our election procedure.
- The partition tests required the implementation of new features just to pass them such as the leader detecting a minority
partition.

## Features of good design

- We implemented several features including a couple outside what was in the Raft paper.
- Get message safety: Do not respond to a get message if the key that is asked is currently uncommitted in your log
- Leader minority partition detection: Leader in hard partition detects it and can respond with a fail to the client.


## Code testing

- Apart from the suite of test cases provided, we also played around with the parameters in the config files
to test our code under various different environments.