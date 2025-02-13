class Settings:

    def __init__ (self):
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #ship settings         
        self.ship_limit = 3
        #bullet settings        
        self.bullet_width = 3           #increase for op bullets try(300)/ base is 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3       #to little?????
        #alien settings        
        self.fleet_drop_speed = 10     #casual 10
        self.speedup_scale = 1.1
        self.score_scale = 1.5      #how much points you will get in next waves 
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):      #all "speed's" movet from __init__
        self.ship_speed = 1.5
        self.ship_speed_y = 1.3
        self.alien_speed = 1.0 
        self.bullet_speed = 3.0
        self.fleet_direction = 1    # 1 is right >> -1 is left <<
        self.alien_points = 50      #points per alien 


    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)

