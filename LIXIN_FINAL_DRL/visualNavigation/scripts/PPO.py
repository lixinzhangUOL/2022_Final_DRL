from tensorforce.agents import PPOAgent

import os
import itertools

import config
import env
import VAE

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

maze_id = config.maze_id
restore = False

GazeboMaze = env.GazeboMaze(maze_id=maze_id, continuous=True)

record_dir = 'results'
if not os.path.exists(record_dir):
    os.makedirs(record_dir)

saver_dir = './models/nav{}'.format(maze_id)
if not os.path.exists(saver_dir):
    os.makedirs(saver_dir)

summarizer_dir = './results/PPO/nav{}'.format(maze_id)
if not os.path.exists(summarizer_dir):
    os.makedirs(summarizer_dir)

vae = VAE.VAE()
vae.set_weights(config.vae_weight)


# Network as list of layers
# reference: https://github.com/Unity-Technologies/ml-agents/blob/master/docs/Training-PPO.md
network_spec = [
    dict(type='dense', size=512, activation='relu'),  # 'none'
    # dict(type='tf_layer', layer='batch_normalization', center=True, scale=True),
    # dict(type="nonlinearity", name='relu'),
    dict(type='dense', size=512, activation='relu'),
    # dict(type='tf_layer', layer='batch_normalization', center=True, scale=True),
    # dict(type="nonlinearity", name='relu'),
    dict(type='dense', size=512, activation='relu'),
    # dict(type='tf_layer', layer='batch_normalization', center=True, scale=True),
    # dict(type="nonlinearity", name='relu')
]


memory = dict(
    type='replay',
    include_next_states=False,
    capacity=10000
)

exploration = dict(
    type='epsilon_decay',
    initial_epsilon=0.1,
    final_epsilon=0.01,
    timesteps=100000,
    start_timestep=0
)


optimizer = dict(
    type='adam',
    learning_rate=0.0001
)

# Instantiate a Tensorforce agent
agent = PPOAgent(
    states=dict(shape=(36,), type='float'),  # GazeboMaze.states,
    actions=GazeboMaze.actions,
    network=network_spec,
    # memory=memory,
    # actions_exploration=exploration,
    saver=dict(directory=saver_dir, basename='PPO_model.ckpt', load=restore, seconds=10800),
    summarizer=dict(directory=summarizer_dir, labels=["graph", "losses", "reward", "entropy"], seconds=10800),
    step_optimizer=optimizer
)


episode = 0
total_timestep = 0
max_timesteps = 1000
max_episodes = 10000
episode_rewards = []
successes = []

while True:
    agent.reset()
    observation = GazeboMaze.reset()
    observation = observation / 255.0  # normalize

    timestep = 0
    episode_reward = 0
    success = False

    while True:
        latent_vector = vae.get_vector(observation.reshape(1, 48, 64, 3))
        latent_vector = list(itertools.chain(*latent_vector))  # [[ ]]  ->  [ ]
        relative_pos = GazeboMaze.p
        previous_act = GazeboMaze.vel_cmd
        print(previous_act)
        state = latent_vector + relative_pos + previous_act
        # print(state)

        # Query the agent for its action decision
        action = agent.act(state)
        # Execute the decision and retrieve the current information
        observation, terminal, reward = GazeboMaze.execute(action)
        observation = observation / 255.0  # normalize
        # print(reward)
        # Pass feedback about performance (and termination) to the agent
        agent.observe(terminal=terminal, reward=reward)
        timestep += 1
        episode_reward += reward
        if terminal or timestep == max_timesteps:
            success = GazeboMaze.success
            break

    episode += 1
    total_timestep += timestep
    # avg_reward = float(episode_reward)/timestep
    successes.append(success)
    episode_rewards.append([episode_reward, timestep, success])

    # if total_timestep > 100000:
    #     print('{}th episode reward: {}'.format(episode, episode_reward))

    if episode % 100 == 0:
        f = open(record_dir + '/PPO_nav' + str(maze_id) + '.txt', 'a+')
        for i in episode_rewards:
            f.write(str(i))
            f.write('\n')
        f.close()
        episode_rewards = []
        agent.save_model('./models/')

    if len(successes) > 100:
        if sum(successes[-100:]) > 80:
            GazeboMaze.close()
            agent.save_model('./models/')
            f = open(record_dir + '/PPO_nav' + str(maze_id) + '.txt', 'a+')
            for i in episode_rewards:       # store the episode_rewards
                f.write(str(i))
                f.write('\n')
            f.close()
            print("Training End!")
            break

    # if episode == max_episodes:
    #     break

