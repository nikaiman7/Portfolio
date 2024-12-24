from pygame.image import load
from pygame.math  import Vector2
from pygame.mixer import Sound
from pygame       import Color
import random

def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

# Make obj reappears on the opposite edge of the screen
def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)   # Ensure GameObject's position never leaves the screen's surface

# Random set of coordinates
def get_random_position(surface):
    return Vector2(random.randrange(surface.get_width()),
                   random.randrange(surface.get_height()))

# Random velocity of asteroids
def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

# Load sounds
def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return Sound(path)

# Print text upon games end
def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, True, color)

    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2

    surface.blit(text_surface, rect)

