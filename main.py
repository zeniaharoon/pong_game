from pong import PongEnvironment
import pygame

if __name__ == "__main__":
    env = PongEnvironment()

    terminated = False
    while not terminated:
        action = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
        env.step(action)