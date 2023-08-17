from envs.pong import PongEnvironment
import yaml
import stable_baselines3 as sb3
from stable_baselines3.common.env_checker import check_env

if __name__ == "__main__":
    with open('config/agents.yaml', 'r') as file:
        stream = yaml.safe_load(file)
    env = PongEnvironment(stream['agent'])
    check_env(env)

    # Set up model
    model = sb3.PPO("MultiInputPolicy", env, verbose=1)
    model.learn(total_timesteps=250)
    model.save("ppo_pong")

    del model
    #Load and evaluate agent
    model = sb3.PPO.load("ppo_pong")
    obs, _ = env.reset()

    done = False
    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, truncated, info = env.step(action)
        env.render()

    env.close()