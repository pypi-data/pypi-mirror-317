import math
import random
import numpy as np

def get_distance_to_target(obs, target=(0.0 ,0.0, 20000)):

    # 输入数据：中心点(0, 0, 20000)，当前位置(long, lat, h)
    t_long, t_lat, t_h = target

    cur_long, cur_lat, cur_h = obs["position/long-gc-deg"], obs["position/lat-geod-deg"], obs["position/h-sl-ft"]

    # 计算经度和纬度的差值（以度为单位）
    delta_long = cur_long - t_long
    delta_lat = cur_lat - t_lat

    # 假设我们在赤道附近，每度经度和纬度大约对应 111公里
    distance_long = delta_long * 111319.49  # 经度方向的实际距离（单位：米）
    distance_lat = delta_lat * 111319.49  # 纬度方向的实际距离（单位：米）

    # 计算高度差
    delta_h = cur_h - t_h
    distance_h = delta_h * 0.3048  # 高度差（单位：米）

    # 计算三维空间距离
    distance = math.sqrt(distance_long ** 2 + distance_lat ** 2 + distance_h ** 2)

    # 判断距离是否小于x米
    if distance < 500.0:
        print(f"当前位置在500m范围内,{distance}")
    # else:
        # print(f"当前位置不在500m范围内,{distance}")

    return distance


def obs_scale(feature):
    # 定义特征的最小值和最大值
    min_vals = np.array([0, 1000, -0.3, -0.3, -0.5 * np.pi, -np.pi, 0, -10, -900, -900, -900, -10, -10, -10, -0.3, -0.3, 1000, 0], dtype=np.float32)
    max_vals = np.array([200, 31000, 0.3, 0.3, 0.5 * np.pi, np.pi, 360, 10, 900, 900, 900, 10, 10, 10, 0.3, 0.3, 31000, 2], dtype=np.float32)

    # 检查输入和最小值/最大值的形状是否一致
    assert feature.shape[-1] == min_vals.shape[0], "Feature dimensions do not match min_vals/max_vals."

    # 归一化公式: feature_scaled = (2 * (feature - min) / (max - min)) - 1
    feature_scaled = 2 * (feature - min_vals) / (max_vals - min_vals) - 1

    return feature_scaled

def get_init_pos():
    max_range = 0.3
    red_y = 2 * max_range * np.random.random() - max_range
    blue_y = 2 * max_range * np.random.random() - max_range
    initial_pos_set = [[max_range, -max_range, -90, 90],
                       [-max_range, max_range, 90, -90]]
    initial_pos = random.choice(initial_pos_set)
    r1 = 0.2 * np.random.random() + 0.8
    r2 = 0.2 * np.random.random() + 0.8
    r3 = 0.5 * np.random.random() + 0.5
    r4 = 0.5 * np.random.random() + 0.5
    red_x, blue_x, red_psi, blue_psi = r1 * initial_pos[0], r2 * initial_pos[1], initial_pos[2], initial_pos[3]

    red_v, blue_v = 900 * r3, 900 * r4

    return red_x, red_y, red_psi, red_v, blue_x, blue_y, blue_psi, blue_v

def get_init_data(initial, render=0):
    # 固定位置范围
    initial_data = {
        "red": {
            "red_0": {
                "ic/h-sl-ft": 22000,
                "ic/terrain-elevation-ft": 1e-08,
                "ic/long-gc-deg": 0.2703,
                "ic/lat-geod-deg": 0.2703,
                "ic/u-fps": 900,
                "ic/v-fps": 0,
                "ic/w-fps": 0,
                "ic/p-rad_sec": 0,
                "ic/q-rad_sec": 0,
                "ic/r-rad_sec": 0,
                "ic/roc-fpm": 0,
                "ic/psi-true-deg": -100,
                "ic/phi-deg": 0,
                "ic/theta-deg": 0
                # , "model": 16, "mode": 1.0,"target_longdeg":0.3,"target_latdeg":0.3,"target_altitude_ft":28000.0
            }
        }
    }
    if initial:
        initial_data.update({"flag": {"init": {"save": 0, "SplitScreen": 0, "render": render}}})
    else:
        initial_data.update({"flag": {"reset": {"save": 0, "SplitScreen": 0}}})

    return initial_data


def get_velocities(obs):
    return math.sqrt(obs['velocities/u-fps'] ** 2 + obs['velocities/v-fps'] ** 2 + obs['velocities/w-fps'] ** 2)

# ===============================================done===============================================
def is_reach_waypoint(obs, done_info):
    # # 判断是否到达下一个路点:
    cur_long = obs['position/long-gc-deg']
    cur_lat = obs['position/lat-geod-deg']
    cur_h = obs['position/h-sl-ft']
    cur_v = get_velocities(obs)
    #
    # # print(f"当前经纬度{cur_long} {cur_lat}+++++++===================")
    # # 这个范围内视为到达目标点 已经验证的值: 0.05
    # geo_delta = 0.03
    # h_delta = 100  # 单位ft
    # target_h = 20000  # 单位ft
    # if abs(cur_long) < geo_delta and abs(cur_lat) < geo_delta and abs(cur_h - target_h) < h_delta:
    #     print(f"到达目标点 当前经纬度{cur_long} {cur_lat} 高度{cur_h}++++++++++++++++++++++++")
    #     return True
    if get_distance_to_target(obs) < 500:
        done_info["is_reach_waypoint"] = True
        done_info["cur_long"] = cur_long
        done_info["cur_lat"] = cur_lat
        done_info["cur_h"] = cur_h
        done_info["cur_v"] = cur_v
        # print(f"到达目标点 当前经纬度{cur_long} {cur_lat} 高度{cur_h}++++++++++++++++++++++++")
        return True
    return False


def is_out_of_bounds(obs, done_info):
    # 边界判断
    cur_long = obs['position/long-gc-deg']
    cur_lat = obs['position/lat-geod-deg']
    cur_h = obs['position/h-sl-ft']
    cur_v = get_velocities(obs)
    if abs(cur_long) > 0.3 or abs(cur_lat) > 0.3 or cur_h < 1000 or cur_h > 30500:
        done_info["is_out_of_bounds"] = True
        done_info["cur_long"] = cur_long
        done_info["cur_lat"] = cur_lat
        done_info["cur_h"] = cur_h
        done_info["cur_v"] = cur_v
        return True

    return False

def is_max_steps_reach(step_num, done_info):
    if step_num >= 2000:
        done_info["is_max_steps_reach"] = True
        return True

    return False
