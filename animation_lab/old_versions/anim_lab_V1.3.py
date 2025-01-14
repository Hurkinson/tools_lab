import pygame, sys
import os

# GAN_pixelart\labs\animation_lab

###############################

def audit_folder(file_path):
    file_count = 0
    for path in os.listdir(file_path):
        if os.path.isfile(os.path.join(file_path, path)):
            file_count += 1
    print("il y a {} fichier(s) dans {}".format(file_count, dir))

    return file_count

###############################

title = "Test animation v.1.3"
date = 2023

"""
v.1.1 - add anim_1b
V.1.1 - add dynamique file handling

v.1.2 - add anim_2
v.1.2 - change folder handling
v.1.2 - add UI info

v.1.3 - add pause toggle
v.1.3 - add frame per frame view, forward and backward
v.1.3 - update UI info
"""


project = "E_final"
file_format ="jpg" 

file_path = r"C:\Users\vivie\OneDrive\Documents\Python_projects\GAN_pixelart\labs\animation_lab\{}".format(project)
file_count = audit_folder(file_path)
frame_count = int((file_count - 1)/2)

width = 400
height = 720
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (40, 200, 80)  #   0, 255, 0
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

font_name = pygame.font.match_font('arial')

###############################

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)   
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#==========================================================================================

class popup_anim(pygame.sprite.Sprite):
    def __init__(self, pos_X, pos_Y):
        pygame.sprite.Sprite.__init__(self)
        self.frame_list = []
        self.frame_list.append(pygame.image.load("{}\pix_frame_0.{}".format(file_path, file_format)).convert_alpha())
        self.current_frame = 0
        self.image = self.frame_list[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_X,pos_Y]

    def set_anim(self, type = "low"):
        self.frame_list.clear()

        if type == "low":
            
            for i in range(frame_count):
                image = r"{}\pix_frame_{}.{}".format(file_path, i, file_format)
                self.frame_list.append(pygame.image.load(image))

        else:

            for i in range(frame_count):
                image = r"{}\frame_{}.{}".format(file_path, i, file_format)
                self.frame_list.append(pygame.image.load(image))

    def update(self, forward = True ):
        if forward:
            self.current_frame += 1
            if self.current_frame >= len(self.frame_list):
                self.current_frame = 0

            self.image = self.frame_list[self.current_frame]
        else:
            self.current_frame -= 1
            if self.current_frame < 0:
                self.current_frame = 0

            self.image = self.frame_list[self.current_frame]

#==========================================================================================

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(title)

anim_frame_low = pygame.sprite.Group()
anim_frame_high = pygame.sprite.Group()

drift_x = -480
drift_y = 0

anim_low = popup_anim(drift_x, drift_y)  
anim_low.set_anim("low")
anim_frame_low.add(anim_low)

anim_high = popup_anim(drift_x, drift_y)
anim_high.set_anim("high")
anim_frame_high.add(anim_high)

running = True
anim_res = "low"
paused = False

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT :
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:   
                running = False

            if event.key == pygame.K_r:
                if anim_res == "low":
                    anim_res = "high"
                else:
                    anim_res = "low"

                print(anim_res)
            
            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_RIGHT:
                if paused:
                    anim_frame_low.update()
                    anim_frame_high.update()

            if event.key == pygame.K_LEFT:
                if paused:
                    anim_frame_low.update(False)
                    anim_frame_high.update(False)

    screen.fill((0,0,0))

    if anim_res == "low":
        anim_frame_low.draw(screen)
        draw_text(screen, str(anim_low.current_frame) + " / " + str(len(anim_low.frame_list)), 15, 120, 80)
        
    if anim_res == "high":
        anim_frame_high.draw(screen)
        draw_text(screen, str(anim_high.current_frame) + " / " + str(len(anim_high.frame_list)), 15, 120, 80)

    if not paused:
        anim_frame_low.update()
        anim_frame_high.update()

    if paused:
        draw_text(screen, "Pause" , 30, 200, 50)
        draw_text(screen, "press < > to move frames " , 15, 300, 10)

    draw_text(screen, "{} resolution".format(anim_res), 30, 90, 5)
    draw_text(screen, "Press R to switch resolution" , 15, 90, 40) 
    draw_text(screen, "Press SPACE for pause" , 15, 80, 60)   
    draw_text(screen, "Current frame: " , 15, 57, 80)    
    
    pygame.display.flip()
    clock.tick(FPS)