import pyautogui
import os
import pygame
import sys
import ctypes

from PIL import Image

class Camera:

    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    X_RES = screensize[0]
    Y_RES = screensize[1]

    def __init__(self):
        self.c_key_pressed = False
        self.enter_key_pressed = False
        self.chart_pic = None
        self.chart_sc = None
        self.saved_pic = None
        self.saved_sc = None
        

    def handle_c_key(self, g):
        g.capture_text = ""
        self.chart_sc = self.take_screenshot(0, 0, Camera.X_RES, Camera.Y_RES)
        self.chart_pic = self.convert_screenshot(self.chart_sc)
        g.init_crop_screen(self.chart_sc, self.chart_pic, (Camera.X_RES, Camera.Y_RES))
        self.c_key_pressed = True

        #print(f"Mouse clicked at ({x}, {y})!")

    # Function to draw the screenshot onto the Pygame window
    def convert_screenshot(self, screenshot):
        pygame_img = pygame.image.fromstring(
            screenshot.tobytes(), screenshot.size, screenshot.mode
        )
        return pygame_img


    def count_files(self):
        try:
            # Get the list of files in the directory
            files = os.listdir("./images")

            # Count the number of files
            file_count = len(files)

            return file_count

        except FileNotFoundError:
            print(f"The directory  does not exist.")
            return None
    
    def take_screenshot(self, mousex_1, mousey_1, mousex_2, mousey_2):
        # Define the region (left, top, width, height)
        region = (mousex_1, mousey_1, mousex_2 - mousex_1, mousey_2 - mousey_1)

        screenshot = pyautogui.screenshot(region=region)

        return screenshot

    def crop_pic(self, g):
        
        self.enter_key_pressed = True
        # Relative coordinates within the Pygame window
        r_x = g.sc_box.rect.x
        r_y = g.sc_box.rect.y

        # Convert relative coordinates to absolute coordinates
        a_x, a_y = g.window.position
        a_x += r_x
        a_y += r_y
        w = g.sc_box.rect.width
        h = g.sc_box.rect.height

        cropped_sc = self.chart_sc.crop((g.sc_box.rect.x, g.sc_box.rect.y, g.sc_box.rect.x + w, g.sc_box.rect.y + h))
        cropped_pic = self.convert_screenshot(cropped_sc)

        self.saved_pic = cropped_pic
        self.saved_sc = cropped_sc
        g.init_label_screen(cropped_sc, cropped_pic)


    def save_data(self, g):
        #save label file
        if self.saved_sc == None or self.saved_pic == None:
            return

        label = g.label_box.text.split(" ")[1]
        fcount = self.count_files()
        fname = "./labels/" + label + str(fcount + 1) + ".txt"

        label_file = open(fname, "w")
        label_file.write(g.label_box.text + "\n")
        # label_file.write(g.risk_box.text + "\n")
        # label_file.write(g.reward_box.text + "\n")

        label_file.close()

        fname = "./images/" + label + str(fcount + 1) + ".png"
        self.saved_sc.save(fname)