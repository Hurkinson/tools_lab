import pygame, sys
import os
import json

# GAN_pixelart\labs\animation_lab

###############################

def audit_folder(file_path):
    global filename_list
    
    filename_list = []
     
    for file in os.listdir(file_path):
        if os.path.isfile(os.path.join(file_path, file)):
                        
            f_name, f_ext = file.split(".")

            filename_list.append({f_name:f_ext})

    file_count = len(filename_list)
    print("\nil y a {} fichier(s) dans {}\n".format(file_count, file_path))

    for file in filename_list:
        print(list(file.items())) 

    return file_count

###############################

title = "Test animation v.1.4"
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

V.1.4 - refonte mécanique majeure: gestion des spritesheets

"""


project = "E_final"            # anim_1b  # spritesheet_test  # anim_paul_walk
src_type = "ss"                         #  ss -> spritesheet  | fpf ->frame per frame
file_format ="jpg" 
resolution_swap = False

file_path = r"C:\Users\vivie\OneDrive\Documents\Python_projects\GAN_pixelart\labs\animation_lab\{}".format(project)
file_count = audit_folder(file_path)
frame_count = int((file_count - 1)/2) if resolution_swap else file_count

#==========================================================================================

font_style = pygame.font.match_font('arial')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (40, 200, 80)  #   0, 255, 0
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

###########################################################################################

class files_input:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace(file_format, 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, w, h):

        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0, 0),(x, y, w, h))
        return sprite

    def parse_sprite(self, name):
        sprite = self.data['frames'][name]['frame']
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        image = self.get_sprite(x, y, w, h)
        return image


#==========================================================================================

def update(frame_list, forward = True ):
    global current_frame

    if forward:
        current_frame += 1
        if current_frame > len(frame_list)-1:
            current_frame = 0
        
    else:
        current_frame -= 1
        if current_frame < 0:
            current_frame = 0
        

###############################

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_style, size)
    text_surface = font.render(text, True, WHITE)   
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

###############################

def stage_manager(anim_list):

    for index, anim  in enumerate(anim_list):

        frame_width = anim[current_frame].get_width()
        frame_height = anim[current_frame].get_height()

        if len(anim_list) >= 2:

            canvas.blit(anim[current_frame], ((WIDTH / len(anim_list) * index) + (WIDTH/len(anim_list)/2)  , (HEIGHT - frame_height)/2))

        else:
            canvas.blit(anim[current_frame], ((WIDTH - frame_width)/2, (HEIGHT - frame_height)/2))


#==========================================================================================

pygame.init()

RES = WIDTH, HEIGHT = 1280, 740

clock = pygame.time.Clock()
canvas = pygame.Surface((WIDTH, HEIGHT))
window = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
pygame.display.set_caption(title)


if resolution_swap:

    anim_frame_low = pygame.sprite.Group()
    anim_frame_high = pygame.sprite.Group()

    # drift_x = -480
    # drift_y = 0

    anim_low = files_input(src_type)  
    anim_low.set_anim("low") 
    anim_frame_low.add(anim_low)

    anim_high = files_input(src_type)
    anim_high.set_anim("high")
    anim_frame_high.add(anim_high)

else: 

    my_spritesheet = files_input(r"{}\anim_paul_walk.png".format(file_path))

    anim_front = [my_spritesheet.parse_sprite('walk_front_1.png'), my_spritesheet.parse_sprite('walk_front_2.png'),my_spritesheet.parse_sprite('walk_front_3.png')]
    anim_left = [my_spritesheet.parse_sprite('walk_left_1.png'), my_spritesheet.parse_sprite('walk_left_2.png'),my_spritesheet.parse_sprite('walk_left_3.png')]
    anim_right = [my_spritesheet.parse_sprite('walk_right_1.png'), my_spritesheet.parse_sprite('walk_right_2.png'),my_spritesheet.parse_sprite('walk_right_3.png')]
    anim_back = [my_spritesheet.parse_sprite('walk_back_1.png'), my_spritesheet.parse_sprite('walk_back_2.png'),my_spritesheet.parse_sprite('walk_back_3.png')]
    
    # my_spritesheet = files_input(r".\{}\new_spritesheet.jpg".format(project))

    # anim_front = [my_spritesheet.parse_sprite('walk_front_1.png'), my_spritesheet.parse_sprite('walk_front_2.png'),my_spritesheet.parse_sprite('walk_front_3.png'), my_spritesheet.parse_sprite('walk_front_4.png')]
    # anim_left = [my_spritesheet.parse_sprite('walk_left_1.png'), my_spritesheet.parse_sprite('walk_left_2.png'),my_spritesheet.parse_sprite('walk_left_3.png')]
    # anim_right = [my_spritesheet.parse_sprite('walk_right_1.png'), my_spritesheet.parse_sprite('walk_right_2.png'),my_spritesheet.parse_sprite('walk_right_3.png')]
    # anim_back = [my_spritesheet.parse_sprite('walk_back_1.png'), my_spritesheet.parse_sprite('walk_back_2.png'),my_spritesheet.parse_sprite('walk_back_3.png')]

anim_list = [anim_front,anim_left, anim_right, anim_back]

running = True
anim_res = "low"
paused = False

current_frame = 0

while running:
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            ############### UPDATE SPRITE IF SPACE IS PRESSED #################################

            if event.key == pygame.K_ESCAPE:   
                running = False

            # if event.key == pygame.K_r:
            #     if resolution_swap:

            #         if anim_res == "low":
            #             anim_res = "high"
            #         else:
            #             anim_res = "low"

            #         print(anim_res)
            
            if event.key == pygame.K_SPACE:
                paused = not paused

            if event.key == pygame.K_RIGHT:
                if paused:
                    if resolution_swap:
                        anim_frame_low.update()
                        anim_frame_high.update()

                    for anim in anim_list:
                        update(anim)

            if event.key == pygame.K_LEFT:
                if paused:
                    if resolution_swap:
                        anim_frame_low.update(False)
                        anim_frame_high.update(False)
                    
                    for anim in anim_list:
                        update(anim, False)


    ################################# UPDATE WINDOW AND DISPLAY #################################     

    canvas.fill(BLACK)   

    stage_manager(anim_list)
    #canvas.blit(anim_front[current_frame], ((WIDTH - anim_front[current_frame].get_width())/2, (HEIGHT - anim_front[current_frame].get_height())/2))

    if not paused:
        if resolution_swap:
            anim_frame_low.update()
            anim_frame_high.update()

        update(anim_front)
    
    window.blit(canvas, (0,0))

    if paused:
        draw_text(window, "Pause" , 50, WIDTH/2, HEIGHT/2 - 200)
        draw_text(window, "press < > to move frames " , 15, 300, 10)

    if resolution_swap:
        draw_text(window, "Press R to switch resolution" , 15, 90, 40) 

    draw_text(window, "{} resolution".format(anim_res), 30, 90, 5)
    draw_text(window, "Press SPACE for pause" , 15, 80, 60)   
    draw_text(window, "Current frame: " , 15, 57, 80) 
    draw_text(window, str(current_frame + 1 ) + " / " + str(len(anim_list[0])), 15, 120, 80)   
    

    pygame.display.flip()
    clock.tick(FPS)





# while running:

#     for event in pygame.event.get():

#         if event.type == pygame.QUIT :
#             pygame.quit()
#             sys.exit()

#         if event.type == pygame.KEYDOWN:

#             if event.key == pygame.K_ESCAPE:   
#                 running = False

#             if event.key == pygame.K_r:
#                 if resolution_swap:

#                     if anim_res == "low":
#                         anim_res = "high"
#                     else:
#                         anim_res = "low"

#                     print(anim_res)
            
#             if event.key == pygame.K_SPACE:
#                 paused = not paused

#             if event.key == pygame.K_RIGHT:
#                 if paused:
#                     if resolution_swap:
#                         anim_frame_low.update()
#                         anim_frame_high.update()

#             if event.key == pygame.K_LEFT:
#                 if paused:
#                     if resolution_swap:
#                         anim_frame_low.update(False)
#                         anim_frame_high.update(False)

#     screen.fill((0,0,0))

#     if resolution_swap:
#         if anim_res == "low":
#             anim_frame_low.draw(screen)
#             draw_text(screen, str(anim_low.current_frame) + " / " + str(len(anim_low.frame_list)), 15, 120, 80)
            
#         if anim_res == "high":
#             anim_frame_high.draw(screen)
#             draw_text(screen, str(anim_high.current_frame) + " / " + str(len(anim_high.frame_list)), 15, 120, 80)

#     if not paused:
#         if resolution_swap:
#             anim_frame_low.update()
#             anim_frame_high.update()

#     if paused:
#         draw_text(screen, "Pause" , 30, 200, 50)
#         draw_text(screen, "press < > to move frames " , 15, 300, 10)

#     if resolution_swap:
#         draw_text(screen, "Press R to switch resolution" , 15, 90, 40) 

#     draw_text(screen, "{} resolution".format(anim_res), 30, 90, 5)
#     draw_text(screen, "Press SPACE for pause" , 15, 80, 60)   
#     draw_text(screen, "Current frame: " , 15, 57, 80)    
    
#     pygame.display.flip()
#     clock.tick(FPS)


    # class animator(pygame.sprite.Sprite):
#     def __init__(self, pos_X, pos_Y):
#         pygame.sprite.Sprite.__init__(self)
#         self.frame_list = []
#         self.frame_list.append(pygame.image.load("{}\pix_frame_0.{}".format(file_path, file_format)).convert_alpha())
#         self.current_frame = 0
#         self.image = self.frame_list[self.current_frame]
#         self.rect = self.image.get_rect()
#         self.rect.topleft = [pos_X,pos_Y]

#     def set_anim(self, type = "low"):
#         self.frame_list.clear()

#         if type == "low":
            
#             for i in range(frame_count):
#                 image = r"{}\pix_frame_{}.{}".format(file_path, i, file_format)
#                 self.frame_list.append(pygame.image.load(image))

#         else:

#             for i in range(frame_count):
#                 image = r"{}\frame_{}.{}".format(file_path, i, file_format)
#                 self.frame_list.append(pygame.image.load(image))

#     def update(self, forward = True ):
#         if forward:
#             self.current_frame += 1
#             if self.current_frame >= len(self.frame_list):
#                 self.current_frame = 0

#             self.image = self.frame_list[self.current_frame]
#         else:
#             self.current_frame -= 1
#             if self.current_frame < 0:
#                 self.current_frame = 0

#             self.image = self.frame_list[self.current_frame]


# class files_input(pygame.sprite.Sprite):
#     def __init__(self, src_type, sprt_width = None, sprt_height = None ):
#         pygame.sprite.Sprite.__init__(self)
#         self.src_type = src_type
#         self.sprt_width = sprt_width
#         self.sprt_height = sprt_height
#         self.frame_list = []
#         # self.frame_list.append(pygame.image.load("{}\{}.{}".format(file_path, list(filename_list[0])[0], filename_list[0].get(list(filename_list[0])[0]))).convert_alpha())
#         self.current_frame = 0
#         self.image = self.frame_list[self.current_frame]
#         self.rect = self.image.get_rect()
#         self.rect.topleft = [WIDTH//2,0]

#     def set_frame_list(self):
#         self.frame_list.clear()

#         if src_type == "fpf":
#             for i in range(file_count):
#                 src_file = "{}\{}.{}".format(file_path, list(filename_list[i-1])[i-1], filename_list[i-1].get(list(filename_list[i-1])[i-1]))
#                 self.frame_list.append(pygame.image.load(src_file))

#         if src_type == "ss":
#             self.src = pygame.image.load("{}\{}.{}".format(file_path, list(filename_list[i-1])[i-1], filename_list[i-1].get(list(filename_list[i-1])[i-1])))
#             anim_count = self.src.get_height() // self.sprt_height
#             frame_count = self.src.get_width() // self.sprt_width

#             for animation in range(anim_count):
#                 for frame in range(frame_count):
#                     pass


#     def update(self, forward = True ):
#         if forward:
#             self.current_frame += 1
#             if self.current_frame >= len(self.frame_list):
#                 self.current_frame = 0

#             self.image = self.frame_list[self.current_frame]
#         else:
#             self.current_frame -= 1
#             if self.current_frame < 0:
#                 self.current_frame = 0

#             self.image = self.frame_list[self.current_frame]

