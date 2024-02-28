
import pygame
from pygame._sdl2 import Window
from enum import Enum, auto
from camera import Camera
from scrollbox import ScrollBox
from textbox import TextBox
from croprectangle import CropRectangle
import os

class Graphics:

    class State(Enum):
        MENU_SCREEN = auto()
        CROP_SCREEN = auto()
        LABEL_SCREEN = auto()
        EDIT_SCREEN = auto()
        SELECT_SCREEN = auto()
        API_SCREEN = auto()

    def __init__(self):


        
        self.font = pygame.font.Font(None, 36)
        self.state = Graphics.State(Graphics.State.MENU_SCREEN)

        self.camera = Camera()

        self.sc_box = CropRectangle(0, 0, 100, 100)

        #Stuff for the editor

        self.next_button = TextBox((0, 0, 100, 50), '>',  is_button=True, click_callback=lambda: self.next_button_click())
        self.prev_button = TextBox((0, 0, 100, 50), '<',  is_button=True, click_callback=lambda: self.prev_button_click())

        self.icon_size = 100
        self.sb_width = Camera.X_RES - (1/20 * Camera.X_RES)
        self.scroll_options = ScrollBox(0, 0, 1/20 * Camera.X_RES, Camera.Y_RES)
        self.scroll_box = ScrollBox(1/20 * Camera.X_RES, 0, self.sb_width, Camera.Y_RES)

        self.time_ints = ["second", "minute", "hour", "day", "week", "month", "quarter", "year"]

        menu_img = pygame.image.load("./pics/menu.png")
        menu_img = pygame.transform.scale(menu_img, (self.icon_size, self.icon_size))
        self.menu_button = TextBox((0, 0, 0, 0), '', is_button=True, image=menu_img, click_callback=lambda: self.init_menu_screen())

        self.dir_button = TextBox((0, 0, 100, 50), 'DIRECTION: Up',  is_button=True, click_callback=lambda: self.dir_button_click())

        #API SCREEN BUTTONS
        self.run_api_button = TextBox((0, 0, 100, 50), 'RUN API', 
                                      is_button=True, 
                                      click_callback=lambda: self.camera.run_api(self),
                                      color_inactive=pygame.Color('green'), 
                                        color_active=pygame.Color('green'))
        self.symbol_button = TextBox((0, 0, 100, 50), 'SYMBOL: all')
        self.from_date_button = TextBox((0, 0, 100, 50), 'FROM_DATE: 2004-01-01')
        self.to_date_button = TextBox((0, 0, 100, 50), 'TO_DATE: 2004-01-03')
        self.time_mult_button = TextBox((0, 0, 100, 50), "TIME_MULT: 1")
        self.time_int = TextBox((0, 0, 100, 50), self.time_ints[0],  is_button=True, click_callback=lambda: self.cycle_time_int())
        self.time_index = 0
        self.num_pics_button = TextBox((0, 0, 100, 50), 'NUM_PICS: 50000')

        self.save_box = TextBox((0, 0, 100, 50), "Save", is_button=True,
                                 color_inactive=pygame.Color('green'), 
                                 color_active=pygame.Color('green'), 
                                 click_callback=lambda: self.camera.save_data(self))
        
        #API BUTTON
        api_img = pygame.image.load("./pics/api.png")
        api_img = pygame.transform.scale(api_img, (self.icon_size, self.icon_size))
        self.api_button = TextBox((0, 0, 0, 0), '', is_button=True, image=api_img, click_callback=lambda: self.init_api_screen())
        
        #CROP BUTTON
        cam_img = pygame.image.load("./pics/camera.jpg")
        cam_img = pygame.transform.scale(cam_img, (self.icon_size, self.icon_size))
        self.crop_button = TextBox((0, 0, 0, 0), '', is_button=True, image=cam_img, click_callback=lambda: self.camera.capture_screen(self))
        
        #EDIT BUTTON
        edit_img = pygame.image.load("./pics/edit_photo.png")
        edit_img = pygame.transform.scale(edit_img, (self.icon_size, self.icon_size))
        self.edit_button = TextBox((0, 0, 0, 0), '', is_button=True, image=edit_img, click_callback=lambda: self.init_edit_screen())
        
        #FOLDER BUTTON
        folder_img = pygame.image.load("./pics/folder_icon.png")
        folder_img = pygame.transform.scale(folder_img, (self.icon_size, self.icon_size))
        self.folder_button = TextBox((0, 0, 0, 0), '', is_button=True, image=folder_img, click_callback=lambda: self.init_select_screen())
        
        self.e_key_pressed = False
        self.s_key_pressed = False
        self.label_boxes = [self.dir_button, self.time_mult_button, self.time_int]
        
        self.edit_boxes = self.label_boxes.copy() + [self.prev_button, self.next_button, self.save_box]
        self.text_boxes = [self.dir_button, self.time_mult_button, self.time_int, self.save_box]
        self.menu_boxes = [self.folder_button, self.edit_button, self.crop_button, self.api_button]
        self.api_boxes = [self.symbol_button, self.from_date_button, self.to_date_button, self.time_mult_button, 
                          self.time_int, 
                          self.num_pics_button, 
                          self.run_api_button]

        self.num_files_txt = None 

        
        self.width = 0
        self.height = 0
        os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"
        self.screen = pygame.display.set_mode((Camera.X_RES, Camera.Y_RES))
        self.window = Window.from_display_module()

        pygame.display.set_caption("Data Collector")

        self.init_menu_screen()

    def cycle_time_int(self):
        self.time_index = (self.time_index + 1) % len(self.time_ints)
        self.time_int.text = self.time_ints[self.time_index]
        self.time_int.txt_surface = self.time_int.font.render(self.time_int.text, True, (0, 0, 0))


    def dir_button_click(self):
        u = "DIRECTION: Up"
        d = "DIRECTION: Down"
        n = "DIRECTION: Neutral"
        if self.dir_button.text.find("Up") != -1:
            self.dir_button.text = d  
        else:
            self.dir_button.text = u
        
        self.dir_button.txt_surface = self.dir_button.font.render(self.dir_button.text, True, (0, 0, 0))
    
    def init_api_screen(self):
        self.state = Graphics.State.API_SCREEN
        spacing = 10

        pygame.display.set_mode((Camera.X_RES, Camera.Y_RES))

        x = spacing
        y = spacing

        for box in self.api_boxes:
            box.rect.x = x
            box.rect.y = y
            y += self.icon_size + spacing
    
    def draw_api_screen(self):
        if self.state == Graphics.State.API_SCREEN:
            self.screen.fill((0, 0, 0))
        
            #draw the text fields
            for box in self.api_boxes:
                box.draw(self.screen)


    def init_menu_screen(self):


        self.state = Graphics.State.MENU_SCREEN
        spacing = 10
        w = self.icon_size + 2 * spacing
        self.width = w
        h = len(self.menu_boxes) * self.icon_size + ((len(self.menu_boxes) + 1) * spacing)
        self.height = h
        pygame.display.set_mode((w, h))

        x = spacing
        y = spacing

        for box in self.menu_boxes:
            box.rect.x = x
            box.rect.y = y
            y += self.icon_size + spacing
        # self.folder_button.rect.x = Camera.X_RES // 2
        # self.folder_button.rect.y = Camera.Y_RES // 2

        # self.edit_button.rect.x = 0
        # self.edit_button.rect.y = 0

        # self.crop_button.rect.x = 0
        # self.edit_button.rect.y = 200


    def draw_menu_screen(self):
        if self.state == Graphics.State.MENU_SCREEN:
            self.screen.fill((255, 255 ,255))
            for box in self.menu_boxes:
                box.draw(self.screen)


    
    def init_crop_screen(self, sc, pic, size):
        self.width, self.height = size
        self.camera.chart_sc = sc
        self.camera.chart_pic = pic
        pygame.display.set_mode(size, pygame.FULLSCREEN)
        self.state = Graphics.State.CROP_SCREEN
        self.camera.saved_pics = []
        self.camera.saved_scs = []

        text = f"# imgs: {self.camera.count_files()} |=| # current: {len(self.camera.saved_scs)}"

        self.num_files_txt = self.font.render(text, True, (240,230,140))
        

    
    def draw_crop_screen(self):
        if self.state == Graphics.State.CROP_SCREEN:

            self.screen.blit(self.camera.chart_pic, (0, 0))

            x = Camera.X_RES - self.num_files_txt.get_width()
            #pygame.draw.rect(self.screen, (177, 177, 177), self.resize_box, 2)
            self.screen.blit(self.num_files_txt, (x, 0))
            
            self.sc_box.draw(self.screen)
            

    def init_label_screen(self):

        pygame.display.set_caption("Data Collector")
        pixel_spacing = 10
        h = pixel_spacing
        for box in self.text_boxes:
            h += box.rect.height + pixel_spacing
        
        self.width = Camera.X_RES // 2
        self.height = h
        pygame.display.set_mode((self.width, self.height))

        #store necessary state and image
        self.state = Graphics.State.LABEL_SCREEN

        #get the correct x and y locations for all the textboxes.
        b_y = pixel_spacing
        for box in self.text_boxes:
            box.rect.y = b_y
            box.rect.x = (self.width - box.rect.width) // 2
            b_y += box.rect.height + pixel_spacing

    def draw_label_screen(self):
        if self.state == Graphics.State.LABEL_SCREEN:
            self.screen.fill((0, 0, 0))
        
            #draw the text fields
            for box in self.text_boxes:
                box.draw(self.screen)
        

    def next_button_click(self):

        l = len(self.camera.image_files)
        self.camera.cur_file_index = (self.camera.cur_file_index + 1) % l
        self.init_edit_screen()



    def prev_button_click(self):
        l = len(self.camera.image_files)
        if self.camera.cur_file_index <= 0:
            self.camera.cur_file_index = l - 1
        else:
            self.camera.cur_file_index -= 1
        self.init_edit_screen()


    def init_edit_screen(self):
        
        self.camera.init_files()
        if len(self.camera.image_files) == 0:
            return
        pygame.display.set_caption("Data Editor")
        self.state = Graphics.State.EDIT_SCREEN


        pixel_spacing = 10
        dy = 0
        for box in self.edit_boxes:
            dy += box.rect.height + pixel_spacing
        
        self.camera.saved_pic = pygame.image.load("./images/" + self.camera.image_files[self.camera.cur_file_index])
        self.width = self.camera.saved_pic.get_width()
        self.height = self.camera.saved_pic.get_height() + dy
        pygame.display.set_mode((self.width, self.height))

        #update labels:
        cur_labels = self.camera.get_cur_labels()
        for i in range(0, len(cur_labels)):
            box = self.label_boxes[i]
            box.text = cur_labels[i]
            box.txt_surface = box.font.render(box.text, True, (0, 0, 0))
        
        #get the correct x and y locations for all the textboxes.
        b_y = self.camera.saved_pic.get_height()
        for box in self.edit_boxes:
            box.rect.y = b_y
            box.rect.x = (self.width - box.rect.width) // 2
            b_y += box.rect.height + pixel_spacing

    
    def draw_edit_screen(self):
        if self.state == Graphics.State.EDIT_SCREEN:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.camera.saved_pic, (0, 0))
            for box in self.edit_boxes:
                box.draw(self.screen)

    def init_select_screen(self):
        self.scroll_box.clear()
        self.scroll_options.clear()
        self.state = Graphics.State.SELECT_SCREEN
        pygame.display.set_mode((self.camera.X_RES, self.camera.Y_RES), pygame.FULLSCREEN)
        self.camera.init_files()

        self.scroll_options.add_item(self.save_box, self.menu_button.rect.size, draw_cb=lambda: self.menu_button.draw(self.screen))


        for s_file in self.camera.image_files:
            file = pygame.image.load("./images/" + s_file)
            self.scroll_box.add_item(file, (file.get_width(), file.get_height()))
        
        self.scroll_box.add_item(self.save_box, self.save_box.rect.size, draw_cb=lambda: self.save_box.draw(self.screen))
        
        
    
    def draw_select_screen(self):
        if self.state == Graphics.State.SELECT_SCREEN:
            self.screen.fill((255, 255, 255))
            self.scroll_box.draw(self.screen)
            self.scroll_options.draw(self.screen)
            
        
    def draw(self):
        self.draw_menu_screen()
        self.draw_crop_screen()
        self.draw_label_screen()
        self.draw_edit_screen()
        self.draw_select_screen()
        self.draw_api_screen()

        pygame.display.flip()

    
    def handle_events(self, event):
        
        if self.state == Graphics.State.MENU_SCREEN:
            for box in self.menu_boxes:
                box.handle_events(event)
                
        if self.state == Graphics.State.CROP_SCREEN:
            self.sc_box.handle_events(event)
        
        elif self.state == Graphics.State.EDIT_SCREEN:
            for box in self.edit_boxes:
                box.handle_events(event)
        if self.state == Graphics.State.LABEL_SCREEN:
            for box in self.text_boxes:
                box.handle_events(event)
                
        if self.state == Graphics.State.API_SCREEN:
            for box in self.api_boxes:
                box.handle_events(event)
        
        if self.state == Graphics.State.SELECT_SCREEN:
            self.scroll_box.handle_events(event)
            self.save_box.handle_events(event)
            self.menu_button.handle_events(event)

        



    