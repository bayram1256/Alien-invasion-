import pygame

from pygame.sprite import Sprite

class Alien(Sprite):


    def __init__(self,ai_game):
        super(). __init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width       #spawn new alien on top LEFT corner of the screeen
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)     #horizontal pos


    def check_edges(self): #return true if alien is at edge
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True



    def update(self): #move to rught >> or left <<
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x













