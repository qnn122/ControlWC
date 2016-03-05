import math

PI = math.pi


class WheelchairModel:
    """ Model of the wheel chair. Store the description of WC at any given time

    Attributes:
        wc_wheel_base, wc_left_base, wc_right_radius, wc_encoder_revolution (float): constant
        wc_x, wc_y, wc_theta (float): current position
        wc_left_travel_distance: travelled distance
        wc_vel_distance: velocity
    """
    def __init__(self):
        self.L = 0.52           # Distance between wheels
        self.R_left = 0.165     # Radius of left wheels
        self.R_right = 0.165
        self.encoder_revolution = 3200  # WTF?

        global LEFT_M_PER_TICK, RIGHT_M_PER_TICK
        LEFT_M_PER_TICK = 2 * PI * self.R_left / self.encoder_revolution
        RIGHT_M_PER_TICK = 2 * PI * self.R_right / self.encoder_revolution

        # TODO: The following part is repeated in wip_wc() method. Must be a more elegant way to tackle this.
        # wc position
        self.x = 0
        self.y = 0

        # wc angle
        self.theta = 0
        self.theta_sum = 0  # cumulative theta angle

        # wc travel distance
        self.d_left = 0
        self.d_right = 0
        self.d_delta = 0

        # wheel velocity
        self.vel_left = 0
        self.vel_right = 0
        self.vel_dt = 0

        self.delta_t = 0

    def get_distance(self):
        return self.d_left, self.d_right

    def get_angle(self):
        return self.theta

    def get_d_delta(self):
        return self.d_delta

    def get_velocity(self):
        return self.vel_left, self.vel_right

    def update_wc_info(self, buffer):
        """Get TOTAL distance travelled
        """
        # Get latest (previous) distance
        p_d_left = self.d_left
        p_d_right = self.d_right

        # Update distance
        for x in range(len(buffer)):
            if x % 2 == 0:      # left encoders
                self.d_left += ord(buffer[x]) * LEFT_M_PER_TICK
            else:               # right encoders
                self.d_right += ord(buffer[x]) * RIGHT_M_PER_TICK

        # Average distance
        self.d_delta = (self.d_left + self.d_right) / 2

        # Update angle
        # TODO: theta_sum does not match real angle (way smaller than real)
        self.theta = (self.d_left - self.d_right) / self.L
        self.theta_sum += self.theta

        # Update velocity
        self.vel_left = (self.d_left - p_d_left) / self.delta_t
        self.vel_right = (self.d_right - p_d_right) / self.delta_t

    def wipe_wc(self):
        """Reset all information of wheelchair model
        """
        # wc position
        self.x = 0
        self.y = 0
        self.theta = 0
        self.theta_sum = 0  # cumulative theta angle

        # wc travel distance
        self.d_left = 0
        self.d_right = 0
        self.d_delta = 0

        # wheel velocity
        self.vel_left = 0
        self.vel_right = 0
        self.vel_dt = 0