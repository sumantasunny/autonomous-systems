from src.environment import worm
from src.agent.a2c import A2CAgent

def episode(env, agent, nr_episode, hyperparams):
    state = env.reset()
    discounted_return = 0
    done = False
    time_step = 0
    while not done:
        # 1. Select action according to policy
        action = agent.policy(state)
        # 2. Execute selected action
        next_state, reward, done, _ = env.step(action)
        # 3. Integrate new experience into agent
        agent.update(state, action, reward, next_state, done)
        state = next_state
        discounted_return += (hyperparams["discount_factor"]**time_step)*reward
        time_step += 1
    print(nr_episode, ":", discounted_return)
    return discounted_return


if __name__ == "__main__":

    # define parameter
    params = {
        "episodes": 100,
        "no_graphics": True,
    }

    # load environment
    env = worm.load_env(no_graphics=params["no_graphics"])

    # define hyperparameter
    hyperparams = {
        "gamma": 0.99,
        "alpha": 0.001,
        "discount_factor": 0.99,
        "nr_hidden_units": 64,
        "nr_input_features": env.observation_space.shape[0],
        "nr_actions": env.action_space.shape[0]
    }

    # create agent
    agent = A2CAgent(hyperparams)

    # define 
    results = [episode(env, agent, i, hyperparams) for i in range(params["episodes"])]

    # close environment
    env.close()
