import pygame, sys, random
import utils, Scripts.entities as entities, Scripts.particle as particle

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('get da coins')

        self.screen = pygame.display.set_mode((960, 540))
        self.display = pygame.Surface((240, 135)) #480 270, 240 135

        self.clock = pygame.time.Clock()
        self.white_font = utils.Font('Images/medium-font.png', (255,255,255))
        self.yellow_font = utils.Font('Images/medium-font.png', (255,255,100))
        self.red_font = utils.Font('Images/medium-font.png', (255,0,50))
        self.blue_font = utils.Font('Images/medium-font.png', (0,100,255))

        self.assets = {
                }

        self.coins = 0
        self.display_coins = 0

        self.player = entities.Player((self.display.get_width()/2, self.display.get_height()/2), (8,1), 1, (255,255,255))
        self.hp = 100
        self.display_hp = 0
        self.move = [False, False, False, False]

        self.boulder = entities.Boulder((30, 30), (20,1), 0.5, (100,100,100))
        self.boulder.velocity[0] = random.randint(-100,100)/100
        self.boulder.velocity[1] = random.randint(-100,100)/100

        self.boulder_particles = []
        self.boulder_ticks = 0

        self.coin = entities.Coin((100,100), (4, 1), 1, (255,255,0))
        self.coin.random_pos((0, self.display.get_width(), 11, self.display.get_height()))
        self.coin_particles = []

        self.game_speed = 1
        self.hi_score = 0

        pygame.mixer.music.load('Assets/Sounds/CoolSong.wav')
        pygame.mixer.music.play(loops=-1)
        self.last_music_pos = 0
        self.paused_music_pos = 0

    def restart(self):
        self.game_speed = 1
        self.player = entities.Player((self.display.get_width()/2, self.display.get_height()/2), (8,1), 1, (255,255,255))
        self.hp = 100
        self.display_hp = 0
        self.coins = 0
        self.display_coins = 0
        self.coin_particles = []
        self.boulder_particles = []
        self.boulder_ticks = 0
        self.coin = entities.Coin((100,100), (4,1), 1, (255,255,0))
        self.coin.random_pos((0, self.display.get_width(), 11, self.display.get_height()))
        self.boulder = entities.Boulder((30, 30), (20,1), 0.5, (100,100,100))
        self.boulder.velocity[0] = random.randint(-100,100)/100
        self.boulder.velocity[1] = random.randint(-100,100)/100
        pygame.mixer.music.play()
        self.last_music_pos = 0
        self.paused_music_pos = 0

    def run(self):
        while True:
            self.display.fill((0,0,0))
            self.boulder_ticks += 1 * self.game_speed

            if self.game_speed == 0:
                if self.last_music_pos != pygame.mixer.music.get_pos():
                    pygame.mixer.music.pause()
                    self.paused_music_pos = pygame.mixer.music.get_pos()
            else:
                if self.last_music_pos == pygame.mixer.music.get_pos():
                    pygame.mixer.music.play()
                    #SET POSITION WHEN PAUSED NOT WORKING YET!!!
                    #pygame.mixer.music.set_pos(self.paused_music_pos)
            self.last_music_pos = pygame.mixer.music.get_pos()

            self.display_coins += (self.coins - self.display_coins)/2 * self.game_speed
            self.display_hp += (self.hp - self.display_hp)/2 * self.game_speed
            self.yellow_font.render(self.display, 'coins: '+str(int(self.display_coins)), (2, 0))
            self.red_font.render(self.display, 'health: '+str(int(self.display_hp)), (self.yellow_font.get_text_width('coins: '+str(int(self.display_coins)))+3, 0))

            self.white_font.render(self.display, 'Z: pause/restart Q: quit', (self.display.get_width() - self.white_font.get_text_width('Z: pause/restart Q: quit'), 0))

            pygame.draw.line(self.display, (255,255,255), (0, 10), (self.display.get_width(), 10))

            self.boulder.update((0,0), self.game_speed)
            self.boulder.render(self.display)
            self.boulder.check_borders((0, self.display.get_width(), 11, self.display.get_height()), 0.1, 100)

            self.coin.update((0,0), self.game_speed)
            self.coin.render(self.display)

            self.player.update((self.move[0] - self.move[1], self.move[2] - self.move[3]), self.game_speed)
            self.player.render(self.display)

            self.player.check_borders((0, self.display.get_width(), 11, self.display.get_height()))

            if self.player.rect().colliderect(self.boulder.rect()) and self.player.protected != True:
                self.player.survive_frames = 60
                self.hp = max(0, self.hp - 25)

            if self.player.rect().colliderect(self.coin.rect()):
                for i in range(random.randint(3,5)):
                    self.coin_particles.append(particle.Particle(self.coin.pos, (random.randint(-2,2), random.randint(-2,2)), (200,200,0), [random.randint(3,5), 1], 1, 0))

                self.coins += 100
                self.coin.random_pos((0, self.display.get_width(), 11, self.display.get_height()))

                self.boulder.velocity[0] += (self.player.pos[0] - self.boulder.pos[0])/300
                self.boulder.velocity[1] += (self.player.pos[1] - self.boulder.pos[1])/300

            if self.boulder_ticks >= 15:
                self.boulder_ticks = 0
                random_color = random.randint(100,150)
                self.boulder_particles.append(particle.Particle((random.randint(int(self.boulder.pos[0]), int(self.boulder.pos[0] + self.boulder.size[0])), random.randint(int(self.boulder.pos[1]), int(self.boulder.pos[1] + self.boulder.size[0]))), (self.boulder.velocity[0]/6, self.boulder.velocity[1]/6), (random_color,random_color,random_color), [random.randint(5,7),1], 1, 0.1))

            for part in self.boulder_particles:
                part.update(self.game_speed)
                part.render(self.display, (0, 0), (random.randint(-10,10), random.randint(-10,10), 0))
                if part.size[0] <= 0:
                    self.boulder_particles.remove(part)
                    part = None
                    del part

            for part in self.coin_particles:
                part.update(self.game_speed)
                part.render(self.display, (0, 0), (0,0,0))

                part.velocity[0] += (0 - part.velocity[0])/15 * self.game_speed
                part.velocity[1] += (0 - part.velocity[1])/15 * self.game_speed

                part.pos[0] += (2 - part.pos[0])/30 * self.game_speed
                part.pos[1] += (0 - part.pos[1])/30 * self.game_speed
                if part.size[0] <= 0 or abs(2 - part.pos[0]) <= 2 and abs(0 - part.pos[1]) <= 2:
                    self.coin_particles.remove(part)
                    part = None
                    del part
            
            self.hi_score = max(self.hi_score, self.coins)

            if self.hp <= 0:
                self.game_speed = 0
                self.display_hp = 0

                self.blue_font.render(self.display, 'You lost!', (self.display.get_width()/2 - self.blue_font.get_text_width('You lost!')/2, self.display.get_height()/2))
                self.blue_font.render(self.display, 'hi score: '+str(self.hi_score), (self.display.get_width()/2 - self.blue_font.get_text_width('hi score: '+str(self.hi_score))/2, self.display.get_height()/2 + 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_z:
                        if self.hp != 0:
                            if self.game_speed == 1:
                                self.game_speed = 0
                            elif self.game_speed == 0:
                                self.game_speed = 1
                        else:
                            self.restart()
                    if event.key == pygame.K_RIGHT:
                        self.move[0] = True
                    if event.key == pygame.K_LEFT:
                        self.move[1] = True
                    if event.key == pygame.K_DOWN:
                        self.move[2] = True
                    if event.key == pygame.K_UP:
                        self.move[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.move[0] = False
                    if event.key == pygame.K_LEFT:
                        self.move[1] = False
                    if event.key == pygame.K_DOWN:
                        self.move[2] = False
                    if event.key == pygame.K_UP:
                        self.move[3] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()
