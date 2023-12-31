import pygame
import sys
import random

class PongEnvironment:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.FONT = pygame.font.SysFont("Consolas", int(self.WIDTH / 20))

        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong!")

        self.CLOCK = pygame.time.Clock()

        self.player = pygame.Rect(0, 0, 10, 100)
        self.player.center = (100, self.HEIGHT / 2)

        self.ai = pygame.Rect(0, 0, 10, 100)
        self.ai.center = (self.WIDTH - 100, self.HEIGHT / 2)

        self.ball = pygame.Rect(0, 0, 20, 20)
        self.ball.center = (self.WIDTH / 2, self.HEIGHT / 2)

        self.x_speed, self.y_speed = 1, 1
        self.player_score, self.opponent_score = 0, 0

    def reset_ball(self):
        self.ball.center = (self.WIDTH / 2, self.HEIGHT / 2)
        self.x_speed, self.y_speed = random.choice([1, -1]), random.choice([1, -1])

    def step(self, action):
        self.handle_events()
        self.update_paddle(action)
        self.agent_action()
        self.update_ball()
        self.check_ball_collision()
        self.check_paddle_collision()
        self.draw_screen()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update_paddle(self, action):
        if action[pygame.K_UP]:
            self.player.y -= 5
        if action[pygame.K_DOWN]:
            self.player.y += 5

    def agent_action(self):
        ai_action = Agent.get_action((self.ball.centery, self.ai.centery))
        if ai_action == "UP":
            self.ai.y -= 5
        elif ai_action == "DOWN":
            self.ai.y += 5

    def update_ball(self):
        self.ball.x += self.x_speed * 5
        self.ball.y += self.y_speed * 5
    
    def check_ball_collision(self):
        if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT:
            self.y_speed = -self.y_speed
        if self.ball.colliderect(self.player) or self.ball.colliderect(self.ai):
            self.x_speed = -self.x_speed
        if self.ball.x <= 0:
            self.opponent_score += 1
            self.reset_ball()

        if self.ball.x >= self.WIDTH:
            self.player_score += 1
            self.reset_ball()

    def check_paddle_collision(self):
        self.player.y = min(max(self.player.y, 0), self.HEIGHT - self.player.height)
        self.ai.y = min(max(self.ai.y, 0), self.HEIGHT - self.ai.height)

    def draw_screen(self):
        self.SCREEN.fill("Black")
        pygame.draw.rect(self.SCREEN, "red", self.player)
        pygame.draw.rect(self.SCREEN, "blue", self.ai)
        pygame.draw.circle(self.SCREEN, "white", self.ball.center, 10)

        #switched colors
        opponent_score_text = self.FONT.render(str(self.opponent_score), True, "blue")
        player_score_text = self.FONT.render(str(self.player_score), True, "red")
        self.SCREEN.blit(opponent_score_text, (self.WIDTH / 2 + 50, 50))
        self.SCREEN.blit(player_score_text, (self.WIDTH / 2 - 50, 50))

        pygame.draw.aaline(self.SCREEN, (255, 255, 255), (self.WIDTH / 2, 0), (self.WIDTH / 2, self.HEIGHT))
        pygame.display.flip()
        pygame.display.update()
        self.CLOCK.tick(300)

    
class Agent:
    @staticmethod
    def get_action(element):
        ball_y, ai_y = element[0], element[1] 
        if ai_y < ball_y:
            return "DOWN"
        elif ai_y > ball_y:
            return "UP"
        else:
            return "STAY"


if __name__ == "__main__":
    env = PongEnvironment()

    terminated = False
    while not terminated:
        action = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
        env.step(action)

