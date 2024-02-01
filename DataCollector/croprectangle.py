import pygame

class CropRectangle:
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