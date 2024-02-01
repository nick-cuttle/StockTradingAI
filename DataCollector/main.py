import pygame
from graphics import Graphics
import sys


if __name__ == "__main__":
        # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60

    g = Graphics() 
    
    # Run the game loop
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            
            g.handle_events(event)

            keys = pygame.key.get_pressed()

            if keys[pygame.K_c] and not g.camera.c_key_pressed:
                if g.state == Graphics.State.TUTORIAL_SCREEN:
                    g.camera.handle_c_key(g)
            elif not keys[pygame.K_c]:
                g.camera.c_key_pressed = False
            
            if keys[pygame.K_e] and not g.e_key_pressed:
                g.e_key_pressed = True
                g.init_edit_screen()
            elif not keys[pygame.K_e]:
                g.e_key_pressed = False
            
            if keys[pygame.K_s] and not g.s_key_pressed:
                g.s_key_pressed = True
                g.init_select_screen()
            elif not keys[pygame.K_e]:
                g.s_key_pressed = False

            if keys[pygame.K_RETURN] and not g.camera.enter_key_pressed:
                if g.state == Graphics.State.CROP_SCREEN:
                    g.camera.crop_pic(g)
            elif not keys[pygame.K_RETURN]:
                g.camera.enter_key_pressed = False
                
            g.draw()

 
