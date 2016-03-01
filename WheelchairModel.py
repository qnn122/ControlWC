class WheelchairModel:
    def __init__(self):
        self.wc_wheel_base = 0.52
        self.wc_left_base = 0.165
        self.wc_right_radius = 0.165
        self.wc_encoder_revolution = 3200

        # wc position
        self.wc_x = 0
        self.wc_y = 0
        self.wc_theta = 0

        # wc travel distance
        self.wc_left_travel_distance = 0
        self.wc_right_travel_distance = 0

        # wheel velocity
        self.wc_vel_distance_left = 0
        self.wc_vel_distance_right = 0
        self.wc_vel_dt = 0
        