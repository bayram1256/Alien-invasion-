class GameStats:

    def __init__(self,ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False     #start game in an inactive state must be False
        self.take_high_score()
        self.level = 1

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0


    def take_high_score(self):
        with open("all_time_high_score.txt", "r") as hs:
            high = hs.readline()
        self.high_score = int(high)       











