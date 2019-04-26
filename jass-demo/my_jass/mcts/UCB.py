import math
import sys
from my_jass.mcts.node import Node
import logging
import random
from my_jass.mcts.action import Action


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('MyLogger')

class UCB:
    def ucbValue(self, totalVisits: int, nodeWinScore: float, nodeVisit: int)-> float:
        if nodeVisit == 0:
            return sys.maxsize

        return (nodeWinScore / nodeVisit) + math.sqrt(math.log(totalVisits) / nodeVisit)

    def findBestNoteUCB(self, node: Node):
        parentVisit = node.getAction().getVisitCount()

        bestchildren = []
        bestScore = 0.0
        for c in node.getChilds(): #type; State
            score = self.ucbValue(parentVisit, c.getAction().getWinScore(), c.getAction().getVisitCount())
            if score == bestScore:
                bestchildren.append(c)

            if score > bestScore:
                bestchildren = [c]
                bestScore = score

        if len(bestchildren) == 0:
            logger.warning("No best Children Found")

        return random.choice(bestchildren)
