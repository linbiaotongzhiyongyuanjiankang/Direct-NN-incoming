import math
from typing import Optional, Union
import numpy as np

import gym
from gym import logger, spaces
from gym.error import DependencyNotInstalled


class CartPoleEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}

    def __init__(self):
        self.surf = None
        self.gravity = 9.8  # 重力加速度
        self.masscart = 1.0  # 小车质量
        self.masspole = 0.1  # 杆质量
        self.total_mass = self.masspole + self.masscart  # 总质量
        self.length = 0.5  # actually half the pole's length # 默认杆长1个单位，以杆的形心为杆重心
        self.polemass_length = self.masspole * self.length  # 杆的最大力矩
        self.force_mag = 10.0  # 小车推力
        self.tau = 0.02  # seconds between state updates，通过小车推力更新运动状态的间隔τ量
        self.kinematics_integrator = "euler"  # 运动状态积分器，默认为欧拉运动学积分器

        # Angle at which to fail the episode
        self.theta_threshold_radians = 12 * 2 * math.pi / 360  # 人为指定的杆转动刻画阈值的正值区限值
        self.x_threshold = 2.4  # 人为指定的杆平动刻画阈值的正值区限值

        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.
        high = np.array(
            [
                self.x_threshold * 2,
                np.finfo(np.float32).max,
                self.theta_threshold_radians * 2,
                np.finfo(np.float32).max,
            ],
            dtype=np.float32,
        )  # 运动学刻画阈值方程，（平动，转动），这个阈值是用来刻画车杆的观察空间的，和运动状态中止条件阈值是不同的

        self.action_space = spaces.Discrete(2)  # 利用gym.space.discrete()创建一个1维离散空间，可以认为它是1维数组（0, ..., 0 + n - 1）
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)  # 创建一系列2维数组，每个2维数组刻画一个空间

        self.screen = None  # 屏幕刻画
        self.clock = None  # 自身时计
        self.isopen = True  # 自身接口
        self.state = None  # 自身运动状态

        self.steps_beyond_done = None  # done前步进

    def step(self, action):  # 定义步进
        err_msg = f"{action!r} ({type(action)}) invalid"  # 报错信息，format(...)
        assert self.action_space.contains(action), err_msg  # assert(条件， false时返回值)，利用断言函数回报返回值
        assert self.state is not None, "Call reset before using step method."
        x, x_dot, theta, theta_dot = self.state  # 经典运动学描述 (x, x', θ, θ')
        force = self.force_mag if action == 1 else -self.force_mag  # action的值∈{0, 1}，分别是负向、正向运动
        costheta = math.cos(theta)  # 保守场分量
        sintheta = math.sin(theta)

        # For the interested reader:
        # https://coneural.org/florian/papers/05_cart_pole.pdf
        temp = (
                       force + self.polemass_length * theta_dot ** 2 * sintheta
               ) / self.total_mass  # 计算整体的加速度，值存储在temp中用于随自身时计积分
        thetaacc = (self.gravity * sintheta - costheta * temp) / (
                self.length * (4.0 / 3.0 - self.masspole * costheta ** 2 / self.total_mass)
        )  # 杆的角加速度
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass
        # 车的线加速度
        if self.kinematics_integrator == "euler":   # 欧拉显式积分器，运动学积分方法
            x = x + self.tau * x_dot
            x_dot = x_dot + self.tau * xacc
            theta = theta + self.tau * theta_dot
            theta_dot = theta_dot + self.tau * thetaacc
        else:  # semi-implicit euler                # 半-隐式积分器，虚功-虚位移方法，先算加速度再用τ乘以加速度反推位移
            x_dot = x_dot + self.tau * xacc
            x = x + self.tau * x_dot
            theta_dot = theta_dot + self.tau * thetaacc
            theta = theta + self.tau * theta_dot

        self.state = (x, x_dot, theta, theta_dot)   # 四个参数刻画运动状态

        done = bool(                                # 奖励器
            x < -self.x_threshold                   # 与刻画空间的阈值比较
            or x > self.x_threshold
            or theta < -self.theta_threshold_radians
            or theta > self.theta_threshold_radians
        )

        if not done:                                # 运动参数超出刻画阈值即判断 Bool(done) == True，此时运动过程中止
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0                            # done前各步进次数统计，每 1步 奖励 1分
        else:
            if self.steps_beyond_done == 0:
                logger.warn(
                    "You are calling 'step()' even though this "
                    "environment has already returned done = True. You "
                    "should always call 'reset()' once you receive 'done = "
                    "True' -- any further steps are undefined behavior."
                )
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state, dtype=np.float32), reward, done, {}

    def reset(
            self,
            *,
            seed: Optional[int] = None,
            return_info: bool = False,
            options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        self.steps_beyond_done = None
        if not return_info:
            return np.array(self.state, dtype=np.float32)
        else:
            return np.array(self.state, dtype=np.float32), {}

    def render(self, mode="human"):                  # 渲染器
        try:
            import pygame
            from pygame import gfxdraw
        except ImportError:
            raise DependencyNotInstalled(
                "pygame is not installed, run `pip install gym[classic_control]`"
            )

        screen_width = 600
        screen_height = 400

        world_width = self.x_threshold * 2
        scale = screen_width / world_width
        polewidth = 10.0
        polelen = scale * (2 * self.length)
        cartwidth = 50.0
        cartheight = 30.0

        if self.state is None:
            return None

        x = self.state

        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode((screen_width, screen_height))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        self.surf = pygame.Surface((screen_width, screen_height))
        self.surf.fill((255, 255, 255))

        l, r, t, b = -cartwidth / 2, cartwidth / 2, cartheight / 2, -cartheight / 2
        axleoffset = cartheight / 4.0
        cartx = x[0] * scale + screen_width / 2.0  # MIDDLE OF CART
        carty = 100  # TOP OF CART
        cart_coords = [(l, b), (l, t), (r, t), (r, b)]
        cart_coords = [(c[0] + cartx, c[1] + carty) for c in cart_coords]
        gfxdraw.aapolygon(self.surf, cart_coords, (0, 0, 0))
        gfxdraw.filled_polygon(self.surf, cart_coords, (0, 0, 0))

        l, r, t, b = (
            -polewidth / 2,
            polewidth / 2,
            polelen - polewidth / 2,
            -polewidth / 2,
        )

        pole_coords = []
        for coord in [(l, b), (l, t), (r, t), (r, b)]:
            coord = pygame.math.Vector2(coord).rotate_rad(-x[2])
            coord = (coord[0] + cartx, coord[1] + carty + axleoffset)
            pole_coords.append(coord)
        gfxdraw.aapolygon(self.surf, pole_coords, (202, 152, 101))
        gfxdraw.filled_polygon(self.surf, pole_coords, (202, 152, 101))

        gfxdraw.aacircle(
            self.surf,
            int(cartx),
            int(carty + axleoffset),
            int(polewidth / 2),
            (129, 132, 203),
        )
        gfxdraw.filled_circle(
            self.surf,
            int(cartx),
            int(carty + axleoffset),
            int(polewidth / 2),
            (129, 132, 203),
        )

        gfxdraw.hline(self.surf, 0, screen_width, carty, (0, 0, 0))

        self.surf = pygame.transform.flip(self.surf, False, True)
        self.screen.blit(self.surf, (0, 0))
        if mode == "human":
            pygame.event.pump()
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()

        if mode == "rgb_array":
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
            )
        else:
            return self.isopen

    def close(self):
        if self.screen is not None:
            import pygame

            pygame.display.quit()
            pygame.quit()
            self.isopen = False
