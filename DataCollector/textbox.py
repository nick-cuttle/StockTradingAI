import pygame

class TextBox:
    def __init__(self, rect, text='', color_inactive=pygame.Color('gray'),
                 color_active=pygame.Color('white'), is_button=False, click_callback=None, image=None):
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
        self.image = image
        if self.image != None:
            self.rect.width = self.image.get_width()
            self.rect.height = self.image.get_height()

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


        if event.type == pygame.KEYDOWN and self.image == None:
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
        if self.image == None:
            width = max(200, self.txt_surface.get_width() + 10)
            self.rect.w = width

    def draw(self, screen):

        if self.image != None:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        
        else:
            pygame.draw.rect(screen, self.color, self.rect, 0)
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
            screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))