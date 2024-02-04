import pygame

    
class ScrollBox:

    def __init__(self, x, y, width, height, items=[]):
        self.rect = pygame.Rect(x, y, width, height)
        self.items = items
        self.scroll_rect = pygame.Rect(x, y, width, height)
        self.scrolling = False
        self.start_mouse = None
        self.start_scroll = None
        self.y_line_items = []
        self.x_line_items = []
        self.spacing = 21
        self.start_time = None
        self.image_size = 100

    
    def clear(self):
        self.items = []
        self.scroll_rect = self.rect.copy()
        self.y_line_items = []
        self.x_line_items = []


    def add_item(self, item, size, draw_cb=None):
        item = ScrollBox.ScrollItem(item, size, draw_cb)
        new_items = []
        for row in self.items:
            for item2 in row: new_items.append(item2)
        self.items = new_items


        self.items.append(item)
        self.y_line_items = []
        self.x_line_items = []
        self.update_items()

    
    def update_items(self):
        x = self.rect.x + self.spacing
        y = self.rect.y + self.spacing
        nexty = y
        new_items = []

        cur_row = []
        for i in range(0, len(self.items)):
            
            cur_item = self.items[i]


            if x + cur_item.rect.width + self.spacing > self.rect.width:
                x = self.rect.x + self.spacing
                y = nexty
                new_items.append(cur_row)
                cur_row = []
  
            cur_row.append(cur_item)

                # line = pygame.Rect(self.rect.x, y - ((self.spacing - w ) // 2), Camera.X_RES, w)
                # self.lines.append(line)
            nexty = max(y + cur_item.rect.height + self.spacing, nexty)

            cur_item.rect.x = x
            cur_item.rect.y = y

            if cur_item.draw_cb != None:
                cur_item.item.rect.x = x
                cur_item.item.rect.y = y

            if i == len(self.items) - 1:
                x += cur_item.rect.width
            else:
                x += cur_item.rect.width + self.spacing
        
        if len(cur_row) != 0: new_items.append(cur_row)

        self.items = new_items


    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 4)
        #pygame.draw.rect(screen, (0, 0, 255), self.scroll_rect, 2)
        size = 5
        mid_space = (self.spacing - size) // 2

        
        for row in range(0, len(self.items)):

            cur_row = self.items[row]

            for j in range(0, len(cur_row)):
                item = cur_row[j]

                if item.rect.colliderect(self.scroll_rect):
                    if item.draw_cb == None:
                        overlap_rect = item.rect.clip(self.scroll_rect)
                        off_y = overlap_rect.y - item.rect.y
                        crop_rect = None
                        cropped = None
                        diff_y = 0

                        

                        if item.rect.y <= self.scroll_rect.y:
                            crop_rect = pygame.Rect(0, off_y, item.rect.width, overlap_rect.height)
                            cropped = item.item.subsurface(crop_rect)
                            diff_y = item.rect.y
                            screen.blit(cropped, (item.rect.x, self.rect.y))

                            b_y = self.rect.y + cropped.get_height() + mid_space // 2
                            below_line = pygame.Rect(item.rect.x, b_y, item.rect.width, size)
                            top_line = below_line.copy()
                            top_line.y = self.rect.y - mid_space
                            pygame.draw.rect(screen, (0, 0, 0), below_line, 2)
                            pygame.draw.rect(screen, (0, 0, 0), top_line, 2)
                            lh = 2* size + mid_space + cropped.get_height()
                            vl_line = pygame.Rect(item.rect.x - mid_space, top_line.y, size, lh)
                            vr_line = pygame.Rect(item.rect.x + cropped.get_width() + mid_space // 2, top_line.y, size, lh)
                            pygame.draw.rect(screen, (0, 0, 0), vl_line, 2)
                            pygame.draw.rect(screen, (0, 0, 0), vr_line, 2)

                        else:
                            crop_rect = pygame.Rect(0, 0, item.rect.width, overlap_rect.height)
                            cropped = item.item.subsurface(crop_rect)
                            diff_y = item.rect.y - self.scroll_rect.y
                            y = self.rect.y + diff_y
                            screen.blit(cropped, (item.rect.x, y))

                            b_y = y + cropped.get_height() + mid_space // 2
                            below_line = pygame.Rect(item.rect.x, b_y, item.rect.width, size)
                            top_line = below_line.copy()
                            top_line.y = y - mid_space
                            lh = 2* size + mid_space + cropped.get_height()
                            pygame.draw.rect(screen, (0, 0, 0), top_line, 2)
                            pygame.draw.rect(screen, (0, 0, 0), below_line, 2)
                            vl_line = pygame.Rect(item.rect.x - mid_space, top_line.y, size, lh)
                            vr_line = pygame.Rect(item.rect.x + cropped.get_width() + mid_space // 2, top_line.y, size, lh)
                            pygame.draw.rect(screen, (0, 0, 0), vl_line, 2)
                            pygame.draw.rect(screen, (0, 0, 0), vr_line, 2)
                        
                    else:

                        if item.rect.y <= self.scroll_rect.y:
                            item.item.rect.y = self.rect.y
                        else:
                            diff_y = item.rect.y - self.scroll_rect.y
                            y = self.rect.y + diff_y
                            item.item.rect.y = y

                        item.draw_cb()
         

    def handle_events(self, event):
        

        accumulated_scroll = 0
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.scrolling = True
                self.start_time = pygame.time.get_ticks()
                self.start_mouse = event.pos
                self.start_scroll = pygame.Rect(self.scroll_rect.x, self.scroll_rect.y, self.rect.width, self.rect.height)
    
        
        elif event.type == pygame.MOUSEMOTION and self.scrolling:

            # elif event.button == 5 and self.rect.collidepoint(event.pos):
            rel_y = event.pos[1] - self.start_mouse[1]

            self.scroll_rect.y = max(self.rect.y, self.start_scroll[1] - rel_y)

        elif event.type == pygame.MOUSEBUTTONUP:

            if self.scrolling:
                time_in_ms = pygame.time.get_ticks() - self.start_time
                if time_in_ms <= 100:
                    mx, my = pygame.mouse.get_pos()
                    self.handle_click(mx, my)
            self.scrolling = False
            self.start_time = None

    
    def handle_click(self, mx, my):

        scroll_x = self.scroll_rect.x
        scroll_y = self.scroll_rect.y

        x = scroll_x + mx
        scroll_y = self.scroll_rect.y


        for row in self.items:

            for item in row:

                if item.rect.collidepoint((mx, my)):
                    print(item.item)


            
    class ScrollItem:

        def __init__(self, item, size, draw_cb=None):
            self.item = item
            self.rect = pygame.Rect(0, 0, size[0], size[1])
            self.draw_cb = draw_cb