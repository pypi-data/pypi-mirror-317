from . import helper as u
import math


def get_done_reward(done_info, reward_info):
    total_reward = 0
    if "is_max_steps_reach" in done_info:
        r = -200
        # self.reward_flag["max_steps_reached_r"] = self.reward_flag.get("max_steps_reached_r", 0) + r
        reward_info["max_steps_reached_r"] = {"r": r, "t_r": r}
        total_reward += r
    # 边界判断
    if "is_out_of_bounds" in done_info:
        r = -200
        # self.reward_info["out_of_bounds_r"] = self.reward_info.get("out_of_bounds_r", 0) + r
        reward_info["out_of_bounds_r"] = {"r": r, "t_r": r}
        total_reward += r
    # 路点判断
    if "is_reach_waypoint" in done_info:
        r = 500
        # self.reward_info["waypoint_reached_r"] = self.reward_info.get("waypoint_reached_r", 0) + r
        reward_info["reach_waypoint_r"] = {"r": r, "t_r": r}
        total_reward += r

    return total_reward


def get_step_reward(reward_info):
    r = -0.1
    reward_info.setdefault("step_r", {"r": 0, "t_r": 0})
    reward_info["step_r"]["r"] = r
    reward_info["step_r"]["t_r"] += r

    return r


# 获取滚转角奖励 [-pi, pi]

def get_velocities_reward(obs, reward_info):

    v = u.get_velocities(obs) * 0.01
    if v <= 10:
        r = (-1 + math.exp(0.7 * (v - 6.5))) * 0.01
    else:
        r = -0.5
    reward_info.setdefault("v_r", {"r": 0, "t_r": 0})
    reward_info["v_r"]["r"] = r
    reward_info["v_r"]["t_r"] += r
    return r


def get_attitude_roll_reward(obs, reward_info):
    r = 0
    roll = obs['attitude/roll-rad']
    if abs(roll) > (1 / 3) * math.pi:
        r = -0.2

        reward_info.setdefault("attitude_roll_r", {"r": 0, "t_r": 0})
        reward_info["attitude_roll_r"]["r"] = r
        reward_info["attitude_roll_r"]["t_r"] += r
    return r

def get_distance_to_target_reward(obs, reward_info):
    r = 0
    distance = u.get_distance_to_target(obs)
    if distance < 700:
        r = 600
    if distance < 1000:
        r = 300
    if distance < 2000.0:
        r = 150
    if distance < 5000.0:
        r = 100
    if distance < 10000.0:
        r = 10
    if distance < 20000.0:
        r = 5
    reward_info.setdefault("distance_to_target_r", {"r": 0, "t_r": 0})
    reward_info["distance_to_target_r"]["r"] = r
    reward_info["distance_to_target_r"]["t_r"] += r
    return r


 # def _get_distance_reward(self):
    #     reward = 0
    #     cur_long = self.origin_obs["position/long-gc-deg"]
    #     cur_lat = self.origin_obs["position/lat-geod-deg"]
    #     cur_h = self.origin_obs["position/h-sl-ft"]
    #
    #     x1 = abs(cur_long)
    #     y1 = abs(cur_lat)
    #     z1 = abs(cur_h / 100000)
    #     distance_now = math.sqrt((x1 - 0) ** 2 + (y1 - 0) ** 2 + (z1 - 0.2) ** 2)
    #
    #     last_long = self.last["long"]
    #     last_lat = self.last["lat"]
    #     last_h = self.last["h"]
    #     x2 = abs(last_long)
    #     y2 = abs(last_lat)
    #     z2 = abs(last_h / 100000)
    #     distance_ago = math.sqrt((x2 - 0) ** 2 + (y2 - 0) ** 2 + (z2 - 0.2) ** 2)
    #
    #     if abs(cur_long) < 0.05 and abs(cur_lat) < 0.05:
    #         print(f"distance {distance_now}")
    #     if distance_now < distance_ago:
    #         reward += 0.02
    #         self.reward_flag["distance_positive_reward"] = self.reward_flag.get("distance_positive_reward", 0) + 0.02
    #     else:
    #         reward -= 0.01
    #         self.reward_flag["distance_negative_reward"] = self.reward_flag.get("distance_negative_reward", 0) - 0.01
    #
    #     self.last["long"] = cur_long
    #     self.last["lat"] = cur_lat
    #     self.last["h"] = cur_h
    #     return reward

