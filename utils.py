import pygame

BASE_PATH = 'Assets/'

def load_image(path):
    img = pygame.image.load(BASE_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img

def load_sound(path):
    sound = pygame.mixer.Sound(BASE_PATH + path)
    return sound

def clip(surface, position, size):
    surface_2 = surface.copy()
    clip_rect = pygame.Rect(position[0], position[1], size[0], size[1])
    surface_2.set_clip(clip_rect)
    img = surface.subsurface(surface_2.get_clip())
    return img.copy()

def swap_pallette(surface, old_color, new_color):
    img_copy = surface.copy()
    img_copy.fill(new_color)
    surface.set_colorkey(old_color)
    img_copy.blit(surface, (0, 0))
    return img_copy

#ORDER : ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.',',',':',';','-','+',"'",'"','!','?','0','1','2','3','4','5','6','7','8','9','(',')','[',']','<','>','/','\\','_','=','*']
class Font:
    def __init__(self, font_path, color=(255,255,255)):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.',',',':',';','-','+',"'",'"','!','?','0','1','2','3','4','5','6','7','8','9','(',')','[',']','<','>','/','\\','_','=','*']
        font_img = load_image(font_path)
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 255 and c[1] != 255:
                char_img = swap_pallette(clip(font_img, (x - current_char_width, 0), (current_char_width, font_img.get_height())), (255,255,255), color)
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['+'].get_width()

    def render(self, surface, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surface.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing
    
    def get_text_width(self, text):
        x_offset = 0
        for char in text:
            if char != ' ':
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing
        return x_offset + self.space_width
