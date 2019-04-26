from my_jass.mcts.node import Node
class Tree:
    def __init__(self) -> None:
        self._rootNode = Node()

    def getRootNode(self)-> Node:
        return self._rootNode