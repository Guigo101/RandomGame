import pygame, random

class Entity:
    def __init__(self, position, size=(8,8), speed=1, color=(255,255,255)):
        self.pos = list(position)
        self.size = size
        self.speed = speed
        self.color = color

        self.velocity = [0, 0]

    def update(self, input=(0,0), game_speed=1):
        movement = [(self.velocity[0] + input[0] * self.speed) * game_speed, (self.velocity[1] + input[1] * self.speed) * game_speed]

        self.pos[0] += movement[0]
        self.pos[1] += movement[1]

    def render(self, surface, offset=(0, 0)):
        pygame.draw.circle(surface, self.color, (self.pos[0] + self.size[0]/2 - offset[0], self.pos[1] + self.size[0]/2 - offset[1]), self.size[0]/2, self.size[1])
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[0])

class Boulder(Entity):
    def __init__(self, position, size=(8, 8), speed=1, color=(255,255,255)):
        super().__init__(position, size, speed, color)

    def check_borders(self, borders=(0,100,0,100), speed_increase=0, max_speed=3, sound=None):
        if self.pos[0] < borders[0]:
            self.velocity[0] *= -1
            self.speed = min(max_speed, self.speed + speed_increase)
            if sound:
                sound.play()
        if self.pos[0] > borders[1] - self.size[0]:
            self.velocity[0] *= -1
            self.speed = min(max_speed, self.speed + speed_increase)
            if sound:
                sound.play()
        if self.pos[1] < borders[2]:
            self.velocity[1] *= -1
            self.speed = min(max_speed, self.speed + speed_increase)
            if sound:
                sound.play()
        if self.pos[1] > borders[3] - self.size[0]:
            self.velocity[1] *= -1
            self.speed = min(max_speed, self.speed + speed_increase)
            if sound:
                sound.play()

class Player(Entity):
    def __init__(self, position, size=(8, 8), speed=1, color=(255, 255, 255)):
        super().__init__(position, size, speed, color)
        self.survive_frames = 60
        self.protected = False

    def update(self, input=(0,0), game_speed=1):
        super().update(input, game_speed)
        self.survive_frames = max(0, self.survive_frames - 1 * game_speed)
        if self.survive_frames > 0:
            self.protected = True
        else:
            self.protected = False
    
    def render(self, surface, offset=(0, 0)):
        defined_color = self.color
        if self.protected:
                defined_color = (100,100,200)

        pygame.draw.rect(surface, defined_color, (self.pos[0] - offset[0], self.pos[1] - offset[1], self.size[0], self.size[0]), self.size[1])
    
    def check_borders(self, borders=(0,100,0,100)):
        if self.pos[0] < borders[0] + 1:
            self.pos[0] = borders[0] + 1
        if self.pos[0] > borders[1] - self.size[0] - 1:
            self.pos[0] = borders[1] - self.size[0] - 1
        if self.pos[1] < borders[2] + 1:
            self.pos[1] = borders[2] + 1
        if self.pos[1] > borders[3] - self.size[0] - 1:
            self.pos[1] = borders[3] - self.size[0] - 1

class Coin(Entity):
    def __init__(self, position, size=(8,8), speed=1, color=(255,255,255)):
        super().__init__(position, size, speed, color)
    
    def render(self, surface, offset=(0, 0)):
        pygame.draw.circle(surface, self.color, (self.pos[0] + self.size[0]/2 - offset[0], self.pos[1] + self.size[0]/2 - offset[1]), self.size[0]/2, self.size[1])
    
    def random_pos(self, borders=(0,100,0,100)):
        self.pos[0] = random.randint(borders[0], borders[1] - self.size[0])
        self.pos[1] = random.randint(borders[2], borders[3] - self.size[0])



