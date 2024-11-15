import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from env_for_test import AlphaBaseEnv
import numpy as np
from matplotlib.widgets import Button, Slider
from matplotlib.widgets import TextBox
from ipywidgets import interact

def get_quaternion_from_euler(roll,yaw=0, pitch=0):
    """
    Convert an Euler angle to a quaternion.
    
    Input
      :param roll: The roll (rotation around x-axis) angle in radians.
      :param pitch: The pitch (rotation around y-axis) angle in radians.
      :param yaw: The yaw (rotation around z-axis) angle in radians.
  
    Output
      :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
    """
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  
    return np.array([qx, qy, qz, qw])


Aloha_class = AlphaBaseEnv()
fig, ax = plt.subplots()
#fig = plt.figure()
fig.subplots_adjust(bottom=0.2)
ax = fig.add_subplot(111, projection='3d')  # параметры контейнера для вывода графика



class Index:
    def __init__(self):
        self.event = 0
        self.reward_mode = 0
        self.current_orientation = 0
        self.local_reward_mode = 0
        self.show_rewards = 0

        return

    def submit_event(self, text):
        self.event = eval(text)
    def submit_rm(self, text):
        self.reward_mode = eval(text)
    # def submit_orient(self, text):
    #     self.reward_mode = eval(text)
    def submit_lrm(self, text):
        self.local_reward_mode = eval(text)
    def submit_show_rew(self, text):
        self.show_rewards = eval(text)
        
        
    def next(self, z):
        self.orientation = slider_orientation.val

        ax.cla() 
        # Подготовка данных
        X = np.arange(-1, 7, 0.1)
        Y = np.array(X)
        Z = np.zeros((len(X), len(Y)))
        if self.event == 0:
            t = np.random.rand()
            gy = 5.3 + 0.6 * t
            gx = 4 - 0.6 * t
        elif self.event == 1:
            gy = 0.5 * np.random.rand() + 4.5
            gx = 1
        else:
            gy = 7.1
            gx = 2 + 0.4 * np.random.rand()

        for i in np.arange(len(X)):
            for j in np.arange(len(Y)):
                x = X[i]
                y = Y[j]
                debug_obs = {
                    "event":self.event,
                    "goal_world_position": np.array([gx,gy,0]), 
                    "current_jetbot_position": np.array([x,y,0]), 
                    "current_jetbot_orientation":np.array(get_quaternion_from_euler(self.current_orientation)),
                    "jetbot_linear_velocity": np.array([0,0,0.0]),
                    "jetbot_angular_velocity": np.array([ -0.16904, 0.048418, -1.1452])
                }
                gt_observations = Aloha_class.get_gt_observations(previous_jetbot_position=np.array([x,y,0]),previous_jetbot_orientation=np.array([5,5,5,0]), debug_obs=debug_obs)
                reward, terminated, truncated, rewards = Aloha_class.get_reward(obs=gt_observations, reward_mode=self.reward_mode, local_reward_mode = self.local_reward_mode)
                if self.show_rewards == 0:
                    Z[i][j] = reward
                elif self.show_rewards == 1:
                    Z[i][j] = rewards["dir_to_goal"]
                elif self.show_rewards == 2:
                    Z[i][j] = rewards["dist_to_goal"]
                elif self.show_rewards == 3:
                    Z[i][j] = rewards["dir_orient_to_goal"]

        # # Построение графика
        X, Y = np.meshgrid(X, Y)    # расширение векторов X,Y в матрицы
        ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')    # метод для отрисовки графиков с параметрами по умолчанию
        plt.draw()

callback = Index()
axnext = fig.add_axes([0.8, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)

axbox_event = fig.add_axes([0.04, 0.05, 0.1, 0.075])
text_box_event = TextBox(axbox_event, 'event')
text_box_event.on_submit(callback.submit_event)

axbox_rm = fig.add_axes([0.16, 0.05, 0.1, 0.075])
text_box_rm = TextBox(axbox_rm, 'rm')
text_box_rm.on_submit(callback.submit_rm)

# axbox_or = fig.add_axes([0.28, 0.05, 0.1, 0.075])
# text_box_or = TextBox(axbox_or, 'orient')
# text_box_or.on_submit(callback.submit_orient)

axbox_lrm = fig.add_axes([0.4, 0.05, 0.1, 0.075])
text_box_lrm = TextBox(axbox_lrm, 'lrm')
text_box_lrm.on_submit(callback.submit_lrm)

axbox_sr = fig.add_axes([0.52, 0.05, 0.1, 0.075])
text_box_sr = TextBox(axbox_sr, 'show')
#text_box_sr.on_submit(callback.submit_show_rew)

axes_orientation = plt.axes([0.05, 0.0, 0.85, 0.04])
slider_orientation = Slider(axes_orientation,
                        label='orientation',
                        valmin=-180,
                        valmax=180,
                        valinit=0.5,
                        valfmt='%1.2f')

plt.show()

