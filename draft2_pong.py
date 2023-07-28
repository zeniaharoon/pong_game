import pygame
import sys
import random

class PongGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1280, 720
        self.FONT = pygame.font.SysFont("Consolas", int(self.WIDTH / 20))

        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong!")

        self.CLOCK = pygame.time.Clock()

        self.player = pygame.Rect(0, 0, 10, 100)
        self.player.center = (self.WIDTH - 100, self.HEIGHT / 2)

        self.opponent = pygame.Rect(0, 0, 10, 100)
        self.opponent.center = (100, self.HEIGHT / 2)

        self.ball = pygame.Rect(0, 0, 20, 20)
        self.ball.center = (self.WIDTH / 2, self.HEIGHT / 2)

        self.x_speed, self.y_speed = 1, 1

        self.player_score, self.opponent_score = 0, 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update_paddles(self):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_UP] and self.player.top > 0:
            self.player.top -= 2
        if keys_pressed[pygame.K_DOWN] and self.player.bottom < self.HEIGHT:
            self.player.bottom += 2

    def update_ball(self):
        self.ball.x += self.x_speed * 2
        self.ball.y += self.y_speed * 2

    def check_ball_collision(self):
        if self.ball.y >= self.HEIGHT or self.ball.y <= 0:
            self.y_speed *= -1

        if self.ball.x <= 0:
            self.opponent_score += 1
            self.reset_ball()

        if self.ball.x >= self.WIDTH:
            self.player_score += 1
            self.reset_ball()

    def check_paddle_collision(self):
        if self.player.x - self.ball.width <= self.ball.x <= self.player.right and self.ball.y in range(self.player.top - self.ball.width, self.player.bottom + self.ball.width):
            self.x_speed *= -1

        if self.opponent.x - self.ball.width <= self.ball.x <= self.opponent.right and self.ball.y in range(self.opponent.top - self.ball.width, self.opponent.bottom + self.ball.width):
            self.x_speed *= -1

    def update_opponent_paddle(self):
        if self.opponent.y < self.ball.y:
            self.opponent.top += 1
        if self.opponent.bottom > self.ball.y:
            self.opponent.bottom -= 1

    def reset_ball(self):
        self.ball.center = (self.WIDTH / 2, self.HEIGHT / 2)
        self.x_speed, self.y_speed = random.choice([1, -1]), random.choice([1, -1])

    def draw_screen(self):
        self.SCREEN.fill("Black")
        pygame.draw.rect(self.SCREEN, "red", self.player)
        pygame.draw.rect(self.SCREEN, "blue", self.opponent)
        pygame.draw.circle(self.SCREEN, "white", self.ball.center, 10)

        #switched colors
        player_score_text = self.FONT.render(str(self.opponent_score), True, "red")
        opponent_score_text = self.FONT.render(str(self.player_score), True, "blue")
        self.SCREEN.blit(player_score_text, (self.WIDTH / 2 + 50, 50))
        self.SCREEN.blit(opponent_score_text, (self.WIDTH / 2 - 50, 50))

        pygame.display.update()
        self.CLOCK.tick(300)

    def run(self):
        while True:
            self.handle_events()
            self.update_paddles()
            self.update_ball()
            self.check_ball_collision()
            self.check_paddle_collision()
            self.update_opponent_paddle()
            self.draw_screen()

if __name__ == "__main__":
    game = PongGame()
    game.run()
