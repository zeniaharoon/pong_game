import pygame
import sys
import random
import yaml
import gym
from gym import spaces
import numpy as np

from agents.hardAgent import HardAgent
from agents.easyAgent import EasyAgent
from agents.medAgent import MediumAgent
from agents.imposAgent import ImpossibleAgent
hard = HardAgent()
easy = EasyAgent()
med = MediumAgent()
impos = ImpossibleAgent()

class PongEnvironment(gym.Env):
    def __init__(self, agent, score_limit=20, render_mode="human"):
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

        self.agent = agent

        
        # ---------------------------------------------------------
        # Set Gym fields
        # ---------------------------------------------------------
        self.observation_space = spaces.Dict(
            {
                'ball_y': spaces.Box(0, self.HEIGHT, shape=(1,), dtype=float),
                "player_y": spaces.Box(0, self.HEIGHT, shape=(1,), dtype=float)
            }
        )

        self.action_space = spaces.Discrete(3)
        self.render_mode = render_mode

    def _get_obs(self):
        return {
            'ball_y': np.array([self.ball.centery]),
            'player_y': np.array([self.player.centery])
        }


    def reset(self):
        self.reset_ball()
        self.player.center = (100, self.HEIGHT / 2)
        self.ai.center = (self.WIDTH - 100, self.HEIGHT / 2)
        self.player_score, self.opponent_score = 0, 0
        return self._get_obs()

    def reset_ball(self):
        self.ball.center = (self.WIDTH / 2, self.HEIGHT / 2)
        self.x_speed, self.y_speed = random.choice([1, -1]), random.choice([1, -1])

    def step(self, action):
        self.handle_events()
        if action == 1:
            self.player.y -= 5
        elif action == 2:
            self.player.y += 5
        #self.update_paddle(action)
        self.agent_action()
        self.update_ball()
        reward = self.check_ball_collision()
        self.check_paddle_collision()
        if self.render_mode == "human":
            self.render()

        observation = self._get_obs()
        done = True if self.player_score >= 20 or self.opponent_score >= 20 else False
    
        return observation, reward, done, {}

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
        
        if self.agent == "easy":
            ai_action = easy.get_action(self.ball.centery, self.ai.centery)
            if ai_action == "UP":
                self.ai.y -= easy.speed
            elif ai_action == "DOWN":
                self.ai.y += easy.speed

        elif self.agent == "med":
            ai_action = med.get_action(self.ball.centery, self.ai.centery)
            if ai_action == "UP":
                self.ai.y -= med.speed
            elif ai_action == "DOWN":
                self.ai.y += med.speed

        elif self.agent == "hard":
            ai_action = hard.get_action(self.ball.centery, self.ai.centery)
            if ai_action == "UP":
                self.ai.y -= hard.speed
            elif ai_action == "DOWN":
                self.ai.y += hard.speed

        elif self.agent == "impos":
            ai_action = impos.get_action(self.ball.centery, self.ai.centery)
            if ai_action == "UP":
                self.ai.y -= impos.speed
            elif ai_action == "DOWN":
                self.ai.y += impos.speed
        
    def update_ball(self):
        self.ball.x += self.x_speed * 7
        self.ball.y += self.y_speed * 7
    
    def check_ball_collision(self):
        """Compute ball collisions and return the reward

        Returns:
            float: reward signal for agent
        """
        reward = 0
        if self.ball.top <= 0 or self.ball.bottom >= self.HEIGHT:
            self.y_speed = -self.y_speed
        if self.ball.colliderect(self.player):
            self.x_speed = -self.x_speed
            reward += 0.25
        if self.ball.colliderect(self.ai):
            self.x_speed = -self.x_speed
            reward -= 0.01
        if self.ball.x <= 0:
            self.opponent_score += 1
            reward -= 1
            self.reset_ball()

        if self.ball.x >= self.WIDTH:
            self.player_score += 1
            reward += 1
            self.reset_ball()

        return reward

    def check_paddle_collision(self):
        self.player.y = min(max(self.player.y, 0), self.HEIGHT - self.player.height)
        self.ai.y = min(max(self.ai.y, 0), self.HEIGHT - self.ai.height)

    def render(self):
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
    
    def close():
        pygame.quit()






