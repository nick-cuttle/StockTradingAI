
import pygame
from pygame._sdl2 import Window
from enum import Enum, auto
from camera import Camera

class Graphics:

    class State(Enum):
        TUTORIAL_SCREEN = auto()
        CROP_SCREEN = auto()
        LABEL_SCREEN = auto()


    def __init__(self):


        
        self.tutorial_font = pygame.font.Font(None, 36)
        self.capture_text = "Hit 'C' to capture a screenshot of the screen."
        self.capture_surface = self.tutorial_font.render(self.capture_text, True, (0,0,0))
        self.state = Graphics.State(Graphics.State.TUTORIAL_SCREEN)

        self.camera = Camera()

        self.sc_box = ResizableRectangle(0, 0, 100, 100)

        self.label_box = TextBox((0,0, 100, 50), "LABEL: ")
        self.risk_box = TextBox((0, 0, 100, 50), "RISK: ")
        self.reward_box = TextBox((0, 0, 100, 50), "REWARD: ")

        self.save_box = TextBox((0, 0, 100, 50), "Save", is_button=True,
                                 color_inactive=pygame.Color('green'), 
                                 color_active=pygame.Color('green'), 
                                 click_callback=lambda: self.camera.save_data(self))
        self.text_boxes = [self.label_box, self.save_box]

        

        self.width = self.capture_surface.get_width()
        self.height = self.capture_surface.get_height()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.window = Window.from_display_module()

        pygame.display.set_caption("Data Collector")

    def draw_tutorial_screen(self):
        if self.state == Graphics.State.TUTORIAL_SCREEN:
            self.screen.fill((255, 255 ,255))
            x, y = (self.width // 2 - self.capture_surface.get_width() // 2, self.height // 2 - self.capture_surface.get_height() // 2)
            self.screen.blit(self.capture_surface, (x, y))
            pygame.display.flip()

    
    def init_crop_screen(self, sc, pic, size):
        self.width, self.height = size
        self.camera.chart_sc = sc
        self.camera.chart_pic = pic
        pygame.display.set_mode(size, pygame.FULLSCREEN)
        self.state = Graphics.State.CROP_SCREEN
        

    
    def draw_crop_screen(self):
        if self.state == Graphics.State.CROP_SCREEN:

            self.screen.blit(self.camera.chart_pic, (0, 0))
            
            self.sc_box.draw(self.screen)
            
            pygame.display.flip()

    def init_label_screen(self, cropped_sc, cropped_pic):


        pixel_spacing = 10
        dy = 0
        for box in self.text_boxes:
            dy += box.rect.height + pixel_spacing
        
        self.width = cropped_sc.width
        self.height = cropped_sc.height + dy
        pygame.display.set_mode((self.width, self.height))

        # Set the position of the window

        new_x = (Camera.X_RES - self.width) // 2
        new_y = (Camera.Y_RES - self.height) // 2
        # pygame.display.get_wm_info()["window"].set_position((new_x, new_y))
        #pygame.display.set_pos((new_x, new_y))




        #store necessary state and image
        self.state = Graphics.State.LABEL_SCREEN
        self.camera.saved_sc = cropped_sc
        self.camera.saved_pic = cropped_pic
        

        #get the correct x and y locations for all the textboxes.
        b_y = cropped_sc.height
        for box in self.text_boxes:
            box.rect.y = b_y
            box.rect.x = (self.width - box.rect.width) // 2
            b_y += box.rect.height + pixel_spacing






    def draw_label_screen(self):
        if self.state == Graphics.State.LABEL_SCREEN:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.camera.saved_pic, (0, 0))
        
            #draw the text fields
            for box in self.text_boxes:
                box.draw(self.screen)
        
            pygame.display.flip()

    

    def draw(self):
        self.draw_tutorial_screen()
        self.draw_crop_screen()
        self.draw_label_screen()

    
    def handle_events(self, event):

        # if self.state== Graphics.State.CROP_SCREEN and event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1 and not self.rect.collidepoint(event.pos):
                
        if self.state == Graphics.State.CROP_SCREEN:
            self.sc_box.handle_events(event)

        for box in self.text_boxes:
            box.handle_events(event)


class TextBox:
    def __init__(self, rect, text='', color_inactive=pygame.Color('gray'),
                 color_active=pygame.Color('white'), is_button=False, click_callback=None):
        self.rect = pygame.Rect(rect)
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color = color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.txt_surface = self.font.render(text, True, (0, 0, 0))
        self.active = False
        self.is_button = is_button
        self.click_callback = click_callback

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                #clicked and now is active.
                if self.is_button and self.active and self.click_callback is not None:
                    self.click_callback()
                    self.active = False
                    return
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive


        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (0, 0, 0))
        
        self.update()

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        #pygame.display.flip()
        

class Button:

    def __init__(self, x, y, width, height, result):
        self.rect = pygame.Rect(x, y, width, height)
        self.result = result
    

    def on_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                    self.result()

    

class ResizableRectangle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.resize_box = pygame.Rect(x + width // 4, y + height // 4, width // 2, height // 2)
        self.resizing = False
        self.l_resize = False
        self.r_resize = False
        self.up_resize = False
        self.down_resize = False
        self.move = False
        self.recreate = False
        self.start_rect = (x, y, width, height)
        self.start_mouse = (0, 0)

    def update(self):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def handle_events(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if self.recreate:
                self.recreate = False

            #recreate
            elif event.button == 1 and not self.rect.collidepoint(event.pos):
                self.recreate = True
                self.start_rect = (event.pos[0], event.pos[1], 10, 10)
                self.rect.x = self.start_rect[0]
                self.rect.y = self.start_rect[1]

                self.rect.width = self.start_rect[2]
                self.rect.height = self.start_rect[3]

                self.start_mouse = (event.pos[0], event.pos[1])
                

            elif event.button == 1 and self.rect.collidepoint(event.pos):
                mx, my = pygame.mouse.get_pos()
                self.resizing = True
                to_move = True

                if mx <= self.rect.x + self.rect.width * (1/4):
                    self.l_resize = True
                    to_move = False
                if mx >= self.rect.x + self.rect.width * (3/4):
                    self.r_resize = True
                    to_move = False
                if my >= self.rect.y + self.rect.height * (3/4):
                    self.down_resize = True
                    to_move = False
                if my <= self.rect.y + self.rect.height * (1/4):
                    self.up_resize = True
                    to_move = False
                
                if to_move:
                    self.resizing = False
                    self.move = True
            
                self.start_rect = (self.rect.x, self.rect.y, self.rect.width, self.rect.height)
                self.start_mouse = (mx, my)

        elif event.type == pygame.MOUSEMOTION:
            
            if self.recreate:
                mx, my = event.pos
                dx = mx - self.start_rect[0]
                dy = my - self.start_rect[1]
                self.rect.width = abs(dx)
                self.rect.height = abs(dy)


            elif self.move: 
                    dx, dy = event.pos[0] - self.start_mouse[0], event.pos[1] - self.start_mouse[1]
                    self.rect.x = self.start_rect[0] + dx
                    self.rect.y = self.start_rect[1] + dy
                    
        
            elif self.resizing:
                
                if self.r_resize:
                    dx= event.pos[0] - self.start_mouse[0]
                    self.rect.width = self.start_rect[2] + dx
                if self.down_resize:
                    dy = event.pos[1] - self.start_mouse[1]
                    self.rect.height = self.start_rect[3] + dy
                if self.up_resize:
                    dy = event.pos[1] - self.start_mouse[1]
                    self.rect.y = self.start_rect[1] + dy
                    self.rect.height = self.start_rect[3] - dy
                if self.l_resize:
                    dx = event.pos[0] - self.start_mouse[0]
                    self.rect.x = self.start_rect[0] + dx
                    self.rect.width = self.start_rect[2] - dx
                
                

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.resizing = False
                self.down_resize = False
                self.up_resize = False
                self.l_resize = False
                self.r_resize = False
                self.move = False
                

    
    def draw(self, screen):

        pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)


        pos = (self.rect.x + self.rect.width // 4, self.rect.y + self.rect.height // 4, self.rect.width // 2, self.rect.height // 2)
        self.resize_box.x = pos[0]
        self.resize_box.y = pos[1]
        self.resize_box.width = pos[2]
        self.resize_box.height = pos[3]
        pygame.draw.rect(screen, (177, 177, 177), self.resize_box, 2)
        
    



    