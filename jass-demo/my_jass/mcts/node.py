import numpy as np
from my_jass.mcts.action import Action
from my_jass.mcts.const import Status
from operator import methodcaller


class Node:
    def __init__(self) -> None:
        self._parent = None
        self._action = Action()     #type:  Action
        self._childs = []         #type:  List[Nodes]
        self._status = Status.NEW

    def setParent(self, parent):
        self._parent = parent

    def getAction(self)-> Action:
        return self._action

    def getChilds(self)->[]:
        return self._childs

    def getStatus(self)->Status:
        return self._status

    def getRandomChild(self)-> 'Node':
        return np.random.choice(self._childs)

    def setAction(self, state: Action):
        self._action = state

    def setStatus(self, status: Status):
        self._status = status

    def addChild(self, node: 'Node'):
        self._childs.append(node)

    def getParent(self):
        return self._parent

    def getChildWithMaxScore(self)-> 'Node':
        bestChild = self._childs[0]
        for child in self._childs:
            if child.getAction().getWinScore() > bestChild.getAction().getWinScore():
                bestChild = child
        return bestChild

    def getChildWithMaxVisitCount(self)-> 'Node':
        bestChild = self._childs[0]
        for child in self._childs:
            if child.getAction().getWinScore() > bestChild.getAction().getVisitCount():
                bestChild = child
        return bestChild