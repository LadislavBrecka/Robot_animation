import numpy as np


class Robot:

    def __init__(self, r, l):
        self.R = r
        self.L = l
        self.center_coord = {'x': 0.0, 'y': 0.0}
        self.left_wheel_cord = {'x': 0.0, 'y': 0.0}
        self.right_wheel_cord = {'x': 0.0, 'y': 0.0}
        self.phi = np.pi / 2
        self.omega = 0.0
        self.vr = 0.0
        self.vl = 0.0
        self.trajectory_center = []
        self.trajectory_left_wheel = []
        self.trajectory_right_wheel = []

    def run(self, step):

        v_t_x = self.get_vel_center() * np.cos(self.phi)
        v_t_y = self.get_vel_center() * np.sin(self.phi)

        self.center_coord['x'] = self.center_coord['x'] + v_t_x * step
        self.center_coord['y'] = self.center_coord['y'] + v_t_y * step

        self.get_omega()

        self.phi = self.phi + self.omega * step

        self.trajectory_center.append([self.center_coord['x'], self.center_coord['y']])

        d_x, d_y = self.get_wheel_offset()

        self.left_wheel_cord['x'] = self.center_coord['x'] - d_x
        self.left_wheel_cord['y'] = self.center_coord['y'] + d_y

        self.right_wheel_cord['x'] = self.center_coord['x'] + d_x
        self.right_wheel_cord['y'] = self.center_coord['y'] - d_y

        self.trajectory_left_wheel.append([self.left_wheel_cord['x'], self.left_wheel_cord['y']])
        self.trajectory_right_wheel.append([self.right_wheel_cord['x'], self.right_wheel_cord['y']])

    def get_omega(self):
        self.omega = (self.vl - self.vr) / self.L

    def get_vel_center(self):
        return (self.vl + self.vr) / 2

    def get_wheel_offset(self):
        return (self.L/2)*np.cos(np.pi/2 - self.phi), (self.L/2)*np.sin(np.pi/2 - self.phi)
