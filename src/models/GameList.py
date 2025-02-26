from typing import List

from src.models.Game import Game


class GameList():
    def __init__(self):
        self.games:List[Game] = []

    def __init__(self, games:List[Game]):
        print("init with list")
        self.games:List[Game] = games

    def __len__(self):
        return self.games.__len__()