import pygame

from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self,ai_game):
        super(). __init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load("ship.bmp")
        self.rect = self.image.get_rect()
        self.settings = ai_game.settings   
        self.rect.midbottom = self.screen_rect.midbottom    # Start each new ship at the bottom center of the
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False   #moving flags left/right 
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
     
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:    #second IF(not elif) to case when both keys are used
            self.x -= self.settings.ship_speed
        if self.moving_up:
            self.y -= self.settings.ship_speed_y
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed_y
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image,self.rect)


    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)




