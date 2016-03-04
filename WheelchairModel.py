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

        # wc position
        self.x = 0
        self.y = 0
        self.theta = 0

        # wc travel distance
        self.d_left = 0
        self.d_right= 0
        self.d_delta = 0

        #wc latest distance
        self.p_d_left = 0
        self.p_d_right = 0

        # wheel velocity
        self.vel_left = 0
        self.vel_right = 0
        self.vel_dt = 0

        self.delta_t = 0
