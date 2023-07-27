#Class Button follows the tutorial from LeMasterTech https://www.youtube.com/watch?v=16DM5Eem0cI
import pygame
surface = pygame.display.set_mode((800, 800)) 
BLACK = (0, 0, 0)
WHITE = (255, 150, 255)
PURPLE = (255, 0, 255)


class Button:
    def __init__(self, x, y, color, row_nmb, row_act, enabled= True, disabled_c = BLACK, act_c = WHITE): 
        self.x = x
        self.y = y
        self.color = color
        self.disabled_c = disabled_c
        self.act_c = act_c
        self.row_nmb= row_nmb #zahl
        self.row_act = row_act
        self.enabled = enabled
   
    def draw(self, surface): 
        if self.enabled: 
            btn_rect = pygame.rect.Rect((self.x, self.y), (20, 70))    
            pygame.draw.rect(surface, self.color, btn_rect, 0, 0)
                  
        else:
            btn_rect = pygame.rect.Rect((self.x, self.y), (20, 70)) 
            pygame.draw.rect(surface, self.color, btn_rect, 0, 0)
            self.color = self.disabled_c
       
        if self.row_act == False: 
            self.color = self.act_c 
        elif self.row_act == True and self.enabled == True:
            self.color = PURPLE
       
 
            
    def checkClick(self):
        mouse_pos = pygame.mouse.get_pos()
        left_click = pygame.mouse.get_pressed()[0]
        btn_rect = pygame.rect.Rect((self.x, self.y), (20,70))
        
        if left_click and btn_rect.collidepoint(mouse_pos) and self.enabled and self.row_act: 
            return True
        else:
            
            return False



           
           


      