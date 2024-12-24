import pygame
from utils     import load_sprite, wrap_position, get_random_position, print_text
from models    import Asteroid, Spaceship

class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250
    
    def __init__(self):
        self._init_pygame()
        self.screen     = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock      = pygame.time.Clock()
        self.font       = pygame.font.Font(None, 64)
        self.message    = ""
        self.bullets    = []
        
        # self.spaceship  = GameObject((400, 300), load_sprite("spaceship"), (0, 0))
        # self.spaceship  = Spaceship((400, 300))
        self.spaceship  = Spaceship((400, 300), self.bullets.append)

        # self.asteroids  = GameObject((400, 300), load_sprite("asteroid"), (0, 0))
        # self.asteroids  = [Asteroid((0, 0)) for _ in range(6)]
        # self.asteroids  = [Asteroid(get_random_position(self.screen)) for _ in range(6)]
        self.asteroids  = []
        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (position.distance_to(self.spaceship.position) > self.MIN_ASTEROID_DISTANCE):
                    break
            # self.asteroids.append(Asteroid(position))
            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            elif (self.spaceship and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    self.spaceship.shoot()
                
        # Dict: {k:v} = {arrow key:True or False}
        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
    
            # if is_key_pressed[pygame.K_UP]:
            #     self.spaceship.accelerate()
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate(forward=True)
            elif is_key_pressed[pygame.K_DOWN]:
                self.spaceship.accelerate(forward=False)

    def _process_game_logic(self):
        # self.spaceship.move()
        # self.asteroid.move()
        # self.spaceship.move(self.screen)
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        # Check for collision between asteroids and spaceship
        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost!"
                    break

        # Check if bullets hit asteroids
        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
                    
        # Check if bullet has left the screen
        for bullet in self.bullets[:]:                                    # "self.bullets[:]": create a copy of self.bullets
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        # Check if no asteroids left
        if not self.asteroids and self.spaceship:
            self.message = "You won!"
        
    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        
        # self.spaceship.draw(self.screen)
        # self.asteroid.draw(self.screen)
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
            
        if self.message:
            print_text(self.screen, self.message, self.font)
            
        pygame.display.flip()
        self.clock.tick(60)
        # print("Collides:", self.spaceship.collides_with(self.asteroid))

    def _get_game_objects(self):
        # return [*self.asteroids, self.spaceship]
        # game_objects = [*self.asteroids]
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)
    
        return game_objects




