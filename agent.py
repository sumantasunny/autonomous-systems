from abc import ABC

import torch
import numpy as np

class Agent(ABC):
    def __init__(self, args):
        self.args = args 

        self.mse = torch.nn.MSELoss()
    
    def get_action(self, state):
        #return action, log_prob
        raise NotImplementedError

    def policy(self, state):
        return self.get_action(state)[0]
    
    def update(self, state, action, reward, next_state, done):
        pass

    def rollout(self):
        
        # Batch data
        states      = []
        next_states = []
        actions     = []
        log_probs   = []
        rewards     = []
        dones       = []

        # Number of timesteps run so far in this batch
        t = 0

        # Sum of rewards achieved so far
        sum_rewards = []

        # default 4800
        while t < self.args.batch_size:
            
            state = self.args.env.reset()
            done = False

            ep_t = 0
            ep_reward = 0
            while True:

                # Increment timesteps for this batch
                t += 1
                ep_t += 1
                self.args.episode += 1
                
                # Get action 
                action, log_prob = self.model.get_action(state)
                
                # Execute step
                next_state, reward, done, _ = self.args.env.step(action)

                # Accumulate reward
                ep_reward += reward

                # Collect observation (state), reward, action, and log prob
                states.append(state)
                next_states.append(next_state)
                rewards.append(reward)
                actions.append(action)
                log_probs.append(log_prob)

                state = next_state

                if done or (self.args.max_step > 0 and ep_t >= self.args.max_step):
                    dones.append(True)
                    # Add summed rewards to list
                    sum_rewards.append(ep_reward)
                    break
                else:
                    dones.append(False)
        
        # calculate discounted return
        discounted_return = self.compute_discounted_rewards(rewards, dones)

        # Reshape data as tensors
        states      = torch.tensor(states,      dtype=torch.float, device=self.args.device)
        next_states = torch.tensor(next_states, dtype=torch.float, device=self.args.device)
        actions     = torch.tensor(actions,     dtype=torch.float, device=self.args.device)
        log_probs   = torch.tensor(log_probs,   dtype=torch.float, device=self.args.device)
        rewards     = torch.tensor(rewards,     dtype=torch.float, device=self.args.device)
        dones       = torch.tensor(dones,       dtype=torch.float, device=self.args.device)

        # Return batch data
        return states, next_states, actions, log_probs, rewards, dones, sum_rewards, discounted_return

    def compute_discounted_rewards(self, rewards, dones):
        discounted_rewards = []
        discounted_reward = 0
        for reward, done in zip(reversed(rewards), reversed(dones)):
            if done:
                discounted_reward = 0
            discounted_reward = reward + self.args.gamma * discounted_reward
            discounted_rewards.insert(0, discounted_reward)

        discounted_rewards = torch.tensor(discounted_rewards, dtype=torch.float, device=self.args.device)

        # Normalizing the rewards:
        if self.args.normalize == "reward":
            discounted_rewards = (discounted_rewards - discounted_rewards.mean()) / (discounted_rewards.std() + 1e-5)
        
        return discounted_rewards