import numpy as np
from typing import Optional
import gymnasium as gym

from .connection import Connection
from . import helper as u
from . import reward_helper as r_helper


class ZK_Env(gym.Env):
    def __init__(self, env_args, render_mode = None):
        # 顺序不能交换
        self.args = env_args
        self._set_render_mode(render_mode)
        self.connection = Connection(self.args)
        self._set_s_a_space()
        # 是否环境第一次启动
        self.initial = True
        # need to reset in reset()
        self.origin_obs = None
        # need to reset in reset_var()
        self.is_done = False
        self.step_num = 0
        self.reward_info = {}
        self.last = {}
        self.last_action = [0.0, 0.0, 0.0]
        self.first_action_flag = True

    def _set_render_mode(self, render_mode):

        if render_mode == 1:
            self.args.play_mode = 1

        if render_mode == 2:
            self.args.render = 1


    def _set_s_a_space(self):
        """
        define observation space and action space
        """

        # 使用 Box 定义连续的动作空间
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(self.args.action_dim,))

        self.observation_space = gym.spaces.Box(low=-10, high=10, shape=(self.args.obs_dim,))

    def _reset_var(self):

        # 回合是否结束重置
        self.is_done = False
        # 回合步数重置
        self.step_num = 0
        # 重置
        self.reward_info = {}
        self.last = {}
        self.last_action = [0.0, 0.0, 0.0]
        self.first_action_flag = True

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        super().reset(seed=seed)
        self._reset_var()
        # 初始化
        single_init_data = u.get_init_data(self.initial, self.args.render)
        self.initial = False
        self.connection.send_condition(single_init_data)
        # 返回 red obs {"":"", .....}
        self.origin_obs = self._get_obs(self.connection.accept_from_socket())
        # 返回处理之后需要的 obs [, , , ]
        obs = self._postprocess_obs()
        return obs, {}

    def step(self, action_index):
        action = self._postprocess_action(action_index)
        self.connection.send_condition(action)
        self.origin_obs = self._get_obs(self.connection.accept_from_socket())
        done_info = self._is_done()
        self.is_done = len(done_info) != 0
        # obs reward 都需要根据is_done来判断
        next_obs = self._postprocess_obs()
        reward = self._get_reward(done_info=done_info)
        self.step_num += 1
        info = {"done_info": done_info, "reward_info": self.reward_info}
        return next_obs, reward, self.is_done, self.is_done, info



    def _is_done(self, ):
        done_info = {}
        # 坠毁判断
        # TODO 最大步数判断或者时间
        u.is_max_steps_reach(self.step_num, done_info)

        # 到达路点判断
        u.is_reach_waypoint(self.origin_obs, done_info)

        # 边界判断
        u.is_out_of_bounds(self.origin_obs, done_info)


        return done_info

    # ============================================================ reward related ============================================================
    def _get_reward(self, done_info=None):
        """
        Returns:
            calculated reward
        """
        total_reward = 0
        # =======================稀疏奖励=======================
        total_reward += r_helper.get_done_reward(done_info=done_info, reward_info=self.reward_info)

        # =======================稠密奖励=======================
        total_reward += r_helper.get_step_reward(reward_info=self.reward_info)

        total_reward += r_helper.get_distance_to_target_reward(obs=self.origin_obs, reward_info=self.reward_info)
        total_reward += r_helper.get_attitude_roll_reward(obs=self.origin_obs, reward_info=self.reward_info)
        total_reward += r_helper.get_velocities_reward(obs=self.origin_obs, reward_info=self.reward_info)

        return total_reward

    # ============================================================ action related ============================================================
    def _postprocess_action(self, origin_action):
        origin_action = np.array(origin_action, dtype=np.float64)
        ca = origin_action[0]
        cr = origin_action[1]
        ce = origin_action[2]
        ct = (origin_action[3] + 1) * 0.5

        control_side = self.args.control_side
        action = dict()
        action[control_side] = {
            f'{control_side}_0': {
                'mode': 0,
                # 副翼
                "fcs/aileron-cmd-norm": ca,
                # 方向舵
                "fcs/rudder-cmd-norm": cr,
                # 升降舵
                "fcs/elevator-cmd-norm": ce,
                # 油门
                "fcs/throttle-cmd-norm": ct,
            }}

        # print(f"ca {ca} -- cr {cr} -- ce {ce} -- ct {ct} ")
        return action

    # ============================================================ obs related ============================================================
    def _get_obs(self, origin_obs):
        control_side = self.args.control_side
        return origin_obs[control_side][f'{control_side}_0']

    def _postprocess_obs(self):
        # 我方的观测  14 维度 obs
        post_process_obs = self._state_process()

        # 没死 分别值都为 2
        death_event = self._death_event()
        # 在上面14维度的基础上各自加上1维
        post_process_obs.append(death_event)
        # post_process_obs = np.array(post_process_obs).clip(-10, 10)
        np.set_printoptions(precision=6, suppress=True, linewidth=100)
        post_process_obs = np.array(post_process_obs, dtype=np.float32)
        # post_process_obs = np.round(post_process_obs, 6)
        # print(f"origin obs {post_process_obs}")
        post_process_obs = u.obs_scale(post_process_obs)
        # print(f"scale obs {post_process_obs}")
        return post_process_obs

    def _death_event(self):
        """
        [2,0,1---2,0,1]
        return [2,2]
        """
        death_event = self.origin_obs['DeathEvent']

        if death_event == 99:
            return 2
        elif death_event == 0:
            return 0
        else:
            return 1

    def _state_process(self):
        #  结束时返回的最后一个 obs
        if self.is_done:
            return [0] * (self.args.obs_dim - 1)
        else:
            post_process_obs = []
            obs = self.origin_obs
            # 生命值和高度
            post_process_obs.append(obs['LifeCurrent'])
            post_process_obs.append(obs['position/h-sl-ft'])
            # 经纬度
            post_process_obs.append(obs['position/long-gc-deg'])
            post_process_obs.append(obs['position/lat-geod-deg'])
            # 姿态

            post_process_obs.append(obs['attitude/pitch-rad'])  # 俯仰角 -π/2 π/2
            post_process_obs.append(obs['attitude/roll-rad'])  # 翻滚角 -π π
            post_process_obs.append(obs['attitude/psi-deg'])  # 航向角 [0,360)
            post_process_obs.append(obs['aero/beta-deg'])  # 侧滑角 [-180,180]
            # 速度
            post_process_obs.append(obs['velocities/u-fps'])
            post_process_obs.append(obs['velocities/v-fps'])
            post_process_obs.append(obs['velocities/w-fps'])
            # 角速度
            post_process_obs.append(obs['velocities/p-rad_sec'])  # 翻滚速率 rad/s  视角:机尾到机头 右翼下倾 为正
            post_process_obs.append(obs['velocities/q-rad_sec'])  # 俯仰速率 rad/s  机头上仰 为正
            post_process_obs.append(obs['velocities/r-rad_sec'])  # 偏航速率 rad/s  视角:俯视 机头右偏 为正

            post_process_obs.append(0.0)  # 目标经度
            post_process_obs.append(0.0)  # 目标纬度
            post_process_obs.append(20000) # 目标航向

            # target_longdeg = obs['target_longdeg']
            # target_latdeg = obs['target_latdeg']
            # target_altitude_ft = obs['target_altitude_ft']
            # target_velocity = obs['target_velocity']
            # target_track_deg = obs['target_track_deg']
            # altitude_error_ft = obs['altitude_error_ft']
            # track_error_deg = obs['track_error_deg']
            # delta_velocity = obs['delta_velocity']
            # max_pitch_rad = 0

            return post_process_obs
