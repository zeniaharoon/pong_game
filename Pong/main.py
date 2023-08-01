from pong import PongEnvironment
import pygame
import yaml

if __name__ == "__main__":
    with open('agents.yaml', 'r') as file:
        stream = yaml.safe_load(file)
    env = PongEnvironment(stream['agent'])

    terminated = False
    while not terminated:
        action = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
        env.step(action)
