class Move:
    def __init__(self, card: int, payoff: int) -> None:
        super().__init__()
        self._card = card
        self._payoff = payoff

    def __lt__(self, other: 'Move') -> bool:
        return self.get_payoff() < other.get_payoff()

    def __le__(self, other: 'Move') -> bool:
        return self.get_payoff() <= other.get_payoff()

    def __gt__(self, other: 'Move') -> bool:
        return self.get_payoff() > other.get_payoff()

    def __ge__(self, other: 'Move') -> bool:
        return self.get_payoff() >= other.get_payoff()

    def get_card(self):
        return self._card

    def get_payoff(self):
        return self._payoff
