import sys
from typing import List

# max number of entries sent at a time. To Prevent packet drop for being too big

MAX_ENTRIES_IN_NETWORK = 15


class LogEntry:
    """Contains information of log entries along with useful getters and setters"""
    key: str
    value: str
    term: int
    source: str
    MID: str

    def __init__(self, key: str, value: str, term: int, source: str, MID: str):
        self.key = key
        self.value = value
        self.term = term
        self.source = source
        self.MID = MID

    def getKey(self) -> str:
        return self.key

    def getValue(self) -> str:
        return self.value

    def getTerm(self) -> int:
        return self.term

    def getSource(self) -> str:
        return self.source

    def getMID(self) -> str:
        return self.MID


class StateMachine:
    def __init__(self):
        self.lastCommitIndex = -1
        self.lastApplied = -1
        self.log: List[LogEntry] = []
        self.kvstore = {}

    # src MID
    def appendToLog(self, logEntry: LogEntry):
        """Adds new Put to log"""
        self.log.append(logEntry)

    def commit(self, key: str, value: str) -> None:
        """
        store the given command to the log, and key-value pair to the kvstore
        :param key: Key to be added
        :param value: Value to be added
        :return: None
        """
        # this commit is done only after a quorum is achieved
        self.kvstore[key] = value
        self.lastApplied += 1

    def commitEntry(self, idx: int) -> None:
        """Committs entry at given index"""
        key = self.log[idx].getKey()
        value = self.log[idx].getValue()
        self.commit(key, value)

    def get(self, key: str) -> str:
        """
        get the value associated with the given key
        :param key:
        :return:
        """
        if key in self.kvstore:
            return self.kvstore[key]
        else:
            return ""

    def logLength(self) -> int:
        """
        :return: the number of elements in the log
        """
        return len(self.log)

    def getLog(self) -> list:
        """Returns the log"""
        return self.log

    def getPreviousLogTerm(self, index: int) -> int:
        """Gets the log term at the given index"""
        if index == -1:
            return -1
        return self.log[index].getTerm()

    def appendLog(self, index: int, newEntries) -> None:
        """Commit all entries after index of leader"""
        newEntriesObjects = []
        for entry in newEntries:
            obj = LogEntry(entry[0], entry[1], entry[2], entry[3], entry[4])
            newEntriesObjects.append(obj)
        self.log = self.log[:index + 1] + newEntriesObjects

    def matchesLogAtIndex(self, prevLogIndex: int, term: int) -> bool:
        """Returns a bool representing whether the log matches at the given index"""
        return prevLogIndex == -1 or (len(self.log) > prevLogIndex and self.log[prevLogIndex].getTerm() == term)

    def getEntriesFromIndex(self, followerNextIndex: int) -> List:
        """Returns all entries from a given index till the end of the log(max 40 entries)"""
        if followerNextIndex >= self.logLength():
            return []

        lastIdx = min(followerNextIndex + MAX_ENTRIES_IN_NETWORK, self.logLength())
        returnList = []
        for entry in self.log[followerNextIndex:lastIdx]:
            returnList.append((entry.getKey(), entry.getValue(), entry.getTerm(), entry.getSource(), entry.getMID()))
        return returnList

    def getTermOfLastEntry(self) -> int:
        """Returns term of last entry in the log"""
        if self.logLength() == 0:
            return -1
        # return term of last entry
        return self.log[self.logLength() - 1].getTerm()

    def getTermFromIndex(self, index) -> int:
        """Returns term residing in param index"""
        if index >= self.logLength():
            raise Exception

        return self.log[index].getTerm()

    def getConflictingTerm(self, index) -> int:
        """Returns conflicting term that led to appendEntries reject"""
        if not self.log:
            return -1
        idx = min(self.logLength() - 1, index)
        return self.log[idx].getTerm()

    def getFirstIndexOfTerm(self, targetTerm) -> int:
        """Gets first index of a particular term"""
        numberOfEntriesInTargetTerm = 0
        firstIndex = float('inf')
        for i, logObj in enumerate(self.log):
            if logObj.getTerm() == targetTerm:
                numberOfEntriesInTargetTerm += 1
                firstIndex = min(firstIndex, i)

        if numberOfEntriesInTargetTerm > MAX_ENTRIES_IN_NETWORK:
            firstIndex = (firstIndex + numberOfEntriesInTargetTerm) - MAX_ENTRIES_IN_NETWORK

        return firstIndex if firstIndex != float('inf') else -1

    def keyInUncommittedEntries(self, target: str) -> bool:
        """If key is in uncommitted entries, returns True"""
        for logObj in self.log[self.lastApplied + 1:]:
            if logObj.getKey() == target:
                return True
        return False

    def commitUpToDate(self) -> bool:
        """
        :return: True if everything is commited
        """
        return self.lastCommitIndex == self.logLength() - 1