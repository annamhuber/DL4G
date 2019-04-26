from jass.base.round import Round

class Action(object):
    def __init__(self) -> None:
        self._playerNr = 0
        self._winScore = 0.0
        self._visitCount = 0
        self._round = None
        self._card = None

    def getVisitCount(self)-> int:
        return self._visitCount

    def getWinScore(self)-> float:
        return self._winScore

    def setPlayerNr(self, player:int):
        self._playerNr = player

    def getPlayerNr(self) -> int:
        return self._playerNr

    def setRound(self, rnd: Round):
        self._round = rnd

    def getRound(self)->Round:
        return self._round

    def setCard(self, card: int):
        self._card = card

    def getCard(self)->int:
        return self._card

    def incrementVisit(self):
        self._visitCount += 1

    def setWinScore(self, winScore: int):
        self._winScore = winScore