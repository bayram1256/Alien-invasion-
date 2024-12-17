import sys

from time import sleep

import pygame

from settings import Settings

from game_stats import GameStats

from ship import Ship

from bullet import Bullet

from alien import Alien

from button import Button

from scoreboard import Scoreboard

class AlienInvasion:
    
    def __init__(self):         #Overall class to manage game assets and behavioR
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Play")

    def run_game(self): #starts main loop for the game   
        while True: 
            self._check_events()
            self._update_screen()           #erase if it does not work, makes game slower(cause of weak processor?)
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                #self._update_screen()  original place of instance of this method(not the upper one),
                #game become more "smooth" while both active!!!!!


    def _check_events(self):   #responds to key and mouse events
        for event in pygame.event.get():            #watch for keyboard and mouse events
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()      #returns a tupple of cursors x and y coordinates
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
        


    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)   
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings() #reset settings
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)


    def _check_keydown_events(self,event):  #key press
        if event.key == pygame.K_RIGHT:    #Move the ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q: #q to quite
            sys.exit()
        elif event.key == pygame.K_SPACE: #FIRE!!!1!1
            self._fire_bullet()
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True

    
    def _check_keyup_events(self,event):    #key release
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self): #Create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                #print(len(self.bullets))    to check is "old" bullets delited (if need for future)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self): #respodn to collisont alien and bullet
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True,True)   #nested for loop(two times), returns dict
        if collisions:
            for aliens in collisions.values():     #collisions is a dict, where each value is a list of aliens hit by a single bullet 
                 self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):#check if the fleet is at an edge, then update the positions of all aliens in the fleet (from book)  
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()


    def _check_aliens_bottom(self):         #check for aliens who have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):        #may place it before update screen???
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1      #decrements ships left(stats >> settings)
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()    #delete all bullets and aliens 
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5) #pause orig 0.5
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        avaliable_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = avaliable_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height     #determine the number of rows of aliens that fit on the screen
        avaliable_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = avaliable_space_y // (2 * alien_height)
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x): #first row of aliens
                self._create_alien(alien_number,row_number)


    def _create_alien(self,alien_number,row_number):       #create an alien and place in a row
            alien = Alien(self)
            alien_width,alien_height = alien.rect.size
            alien.x = alien_width + (2 * alien_width * alien_number)
            alien.rect.x = alien.x
            alien.rect.y = alien_height + (2 * alien.rect.height * row_number)
            self.aliens.add(alien)


    def _check_fleet_edges(self):       #is an alien reched an edge? >> respond
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    
    def _change_fleet_direction(self):     #drop the fleet and change it direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= (-1)




    def _update_screen(self):   #update images on the screen, and flip to the new screen
        self.screen.fill(self.settings.bg_color) #redraws the screen    
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()            #draws the score info
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip() 





if __name__ == "__main__":          #instance of a game :)
    ai = AlienInvasion()
    ai.run_game()
