import rospkg
path = rospkg.RosPack().get_path('rl_nav')

# Environment related
maze_id = 1
deterministic = False
continuous = True  # if the action space is continuous. True for PPO, DDPG and False for DQN
# image
input_dim = (48, 64, 3)
# reward parameter
r_arrive = 100
r_collision = -50  # -100
Cr = 100
Cp = -0.05  # time step penalty
# goal
goal_space = []
start_space = []
test_space = []
goal_space_nav0 = [[-2.8, -4.0]]
test_space_nav0 = [goal_space_nav0[-1]]
goal_space_nav1 = [[-3.8, -3.8], [-1.5, -4], [-3, -2.2]]
test_space_nav1 = [goal_space_nav1[-1]]
goal_space_nav2 = [[-1.8, -3.2], [-2, -2.6], [-3, -3.2], [-0.8, -3.5], [-0.4, -2.6], [-2.5, -3], [-3, -3], [-2, -1.9],
                   [-1.3, -3.8], [-3.3, -4], [-3, -3.8], [-1.2, -3.2]]
test_space_nav2 = [goal_space_nav2[-1], goal_space_nav2[-2]]
start_space_nav0 = [[1., -3.], [1., -4.], [0, -4.], [0, -1.8], [-1, -3], [-1.8, -1.9], [-1.7, -3.8]]
start_space_nav1 = [[-0.4, -2.6]]   # ,4.0/3*math.pi
start_space_nav2 = [[0.65, -3.0]]  # ,1.0/2*math.pi
start_space_nav3 = [[-3.8, -3.5], [-3.8, -4.1], [0, -3], [-1, -4.1], [-2, -4.1], [-3, -4.1], [-3, -2.5], [-1.2, -3.2],
                    [-1.2, -2.5], [-2, -3.2], [0, -2.5], [0, -3.5], [0, -4], [-2.5, -4.1], [-2.5, -3.2], [-3, -2.5],
                    [-3.5, -2.8], [-3.5, -2.5]]
goal_space.append(goal_space_nav0)
goal_space.append(goal_space_nav1)
goal_space.append(goal_space_nav2)
test_space.append(test_space_nav0)
test_space.append(test_space_nav1)
test_space.append(test_space_nav2)

start_space.append(start_space_nav0)
start_space.append(start_space_nav1)
start_space.append(start_space_nav2)
start_space.append(start_space_nav3)
Cd = 0.354/2   # = r when testing
# max linear velocity
v_max = 0.3  # 0.5  # m/s
# max angular velocity
w_max = 1.0  # 1.2  # rad/s

# VAE related
latent_vector_dim = 32
vae_weight = path + '/scripts/worldModels/models/vae_weights.h5'

# RNN related
dir_name = 'maze1_rnn_data'  # which dir to save the rnn data
rnn_weight = path + '/scripts/worldModels/models/rnn_weights.h5'
episode = 2  # < 1000, for testing RNN
frame = 25  # < 50, for testing RNN
