import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt

# Initialize the environment
env = gym.make("LunarLander-v3")  # v2 works for discrete actions

# Parameters
alpha = 0.1  # Learning rate
gamma = 0.99  # Discount factor
epsilon = 1.0  # Initial exploration rate
epsilon_min = 0.1  # Minimum exploration rate
epsilon_decay = 0.995  # Exploration decay rate
num_episodes = 2000  # Total episodes
max_steps = 500  # Maximum steps per episode
bins = 10  # Discretization bins for state space

# Discretize the state space
state_bins = [np.linspace(-1, 1, bins) for _ in range(8)]  # 8 state features


def discretize_state(state):
    """Discretize the continuous state into discrete bins."""
    state_idx = [np.digitize(s, state_bins[i]) - 1 for i, s in enumerate(state)]
    return tuple(state_idx)


# Initialize Q-table
q_table = np.zeros([bins] * 8 + [env.action_space.n])

# Q-learning algorithm
rewards = []
for episode in range(num_episodes):
    state = discretize_state(env.reset()[0])  # Reset environment
    total_reward = 0
    for step in range(max_steps):
        # Choose an action using epsilon-greedy policy
        if np.random.rand() < epsilon:
            action = env.action_space.sample()  # Explore
        else:
            action = np.argmax(q_table[state])  # Exploit

        # Take action and observe the next state and reward
        next_state, reward, done, truncated, _ = env.step(action)
        next_state = discretize_state(next_state)
        total_reward += reward

        delta = gamma * np.max(q_table[next_state]) - q_table[state][action]
        # Q-value update
        q_table[state][action] += alpha * (reward + delta)

        # Transition to the next state
        state = next_state

        if done:
            break

    # Decay epsilon to reduce exploration over time
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    # Store total reward for this episode
    rewards.append(total_reward)

    # Print progress
    if (episode + 1) % 100 == 0:
        print(f"Episode {episode + 1}/{num_episodes}, Total Reward: {total_reward}")

# Close environment
env.close()

# Visualization of learning progress
plt.plot(np.arange(num_episodes), rewards)
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.title("Learning Progress of Q-Learning Agent")
plt.show()


if __name__ == '__main__':
    state = discretize_state(env.reset()[0])
    done = False
    total_reward = 0

    env = gym.make("LunarLander-v3", render_mode="human")
    env.reset()
    while not done:
        action = np.argmax(q_table[state])  # Use the learned policy
        next_state, reward, done, _, _ = env.step(action)
        state = discretize_state(next_state)
        total_reward += reward

    print(done)
    print(f"Total Reward of Trained Agent: {total_reward}")
    env.close()
