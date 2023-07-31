
class ImpossibleAgent:
    def __init__(self):
        self.ball_y = 0
        self.ai_y = 0

    def get_action(self, element):
        self.ball_y, self.ai_y = element[0], element[1] 
        if self.ai_y < self.ball_y:
            return "DOWN"
        elif self.ai_y > self.ball_y:
            return "UP"
        else:
            return "STAY"