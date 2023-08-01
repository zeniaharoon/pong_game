class HardAgent:
    def __init__(self):
        self.ball_y = 0
        self.ai_y = 0
        self.speed = 4

    def get_action(self, ball_y, ai_y):
        self.ball_y, self.ai_y = ball_y, ai_y
        if self.ai_y < self.ball_y:
            return "DOWN"
        elif self.ai_y > self.ball_y:
            return "UP"
        else:
            return "STAY"