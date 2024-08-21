import pygame

class Particle:
    def __init__(self, position, velocity, color, size, speed, reducement):
        self.pos = list(position)
        self.velocity = list(velocity)
        self.color = color
        self.size = size
        self.speed = speed
        self.reducement = reducement
    
    def update(self, game_speed=1):
        self.size[0] -= self.reducement * game_speed

        movement = [(self.velocity[0] * self.speed) * game_speed, (self.velocity[1] * self.speed) * game_speed]

        self.pos[0] += movement[0]
        self.pos[1] += movement[1]
    
    def render(self, surface, offset=(0, 0), color_offset=(0,0,0)):
        pygame.draw.circle(surface, (self.color[0] + color_offset[0], self.color[1] + color_offset[1], self.color[2] + color_offset[2]), self.pos, self.size[0]/2, self.size[1])
