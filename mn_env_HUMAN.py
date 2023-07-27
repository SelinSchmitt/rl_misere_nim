#the following code provides a user interface and game logic to play the game Misére-Nim between 2 human players
#code structure follows the tutorial 'Prof. Dr. Oliver Hofmann, 2D-Spiele mit pygame, https://www.youtube.com/watch?v=_B5qc3jtPIE'
import pygame
import secrets
from Button import Button



def init():
    
    global enabled 
    global window
    global current_player
    global players  
    global ui_dict
   
    ui_dict = {1:1, 2:3, 3:5, 4:7} 
    
    players = [2, 1]
    current_player = secrets.randbelow(len(players))
    enabled = True
    
    pygame.init()
    
    
    WIDTH = 800
    window = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption('Misere Nim')
    
    createButtons()
    createOKButton()
    pickFirstPlayer()

def pickFirstPlayer():
    global current_player
    
    white=(255, 255, 255)
    font = pygame.font.SysFont('Georgia', 28, bold=True)
    
    if current_player == 1:
        player1 = font.render('Player 1', True,white)
        window.blit(player1, (150, 600)) 
    else:
        player2 = font.render('Player 2', True,white)
        window.blit(player2, (600, 600))
     
    return current_player  
  
def player1(window, font, white, gray):
    player1 = font.render('Player 1', True,white)
    window.blit(player1, (150, 600)) 
    player2 = font.render('Player 2', True,gray)
    window.blit(player2, (600, 600))    
    
def player2(window, font, white, gray):
    player2 = font.render('Player 2', True,white)
    window.blit(player2, (600, 600))
    player1 = font.render('Player 1', True,gray)
    window.blit(player1, (150, 600))  
      
def createButtons():

    black = (0, 0, 0)
    purple = (255, 0, 255)
    
    
    ui_elements = []

   
    window = pygame.display.get_surface()
    window.fill(black)    
 
    x_btn = 350
    y_btn = 100
    
    for row1 in range(1):  
        btn1 = Button(x_btn, y_btn, purple,1, enabled)   
        ui_elements.append(btn1)
      
     
    for row2 in range(3):
        btn2 = Button(x_btn-50, y_btn+100,purple, 2, enabled) 
        x_btn += 50 
        ui_elements.append(btn2)
   
        
              
    for row3 in range(5):        
        btn3 = Button(x_btn-250, y_btn+200,purple,3,  enabled ) 
        x_btn += 50
        ui_elements.append(btn3)
        
        
    for row4 in range(7):        
        btn4 = Button(x_btn-550, y_btn+300, purple, 4, enabled ) 
        x_btn += 50     
        ui_elements.append(btn4)
   
        
    
    return ui_elements

def createOKButton():
    black = (0, 0, 0)
    white = (255, 255, 255)  
    
      
    font = pygame.font.SysFont('Arial', 28, bold=True) 
    text = font.render('OK', True, black)
        
    btnOK = pygame.draw.rect(window, white, [600, 450, 50, 25], 0)
    window.blit(text, (605, 445))
    
    return btnOK
 

               
def drawButtons(window, ui_elements):
    for buttons in ui_elements:
        buttons.draw(window)   
 
def user_input(ui_elements, btnOK):
    global current_player
    global ui_dict
    
    white=(255, 255, 255)
    gray = (50, 50, 50)
    current_row = None
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            return False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for ui_elem in ui_elements:
                if ui_elem.checkClick(): 
                    ui_elem.enabled = False
                    
                    current_row = ui_elem.row_nmb 
                    disableRows(ui_elements, current_row) 
                    
                    if all(ui_elem.enabled == False for ui_elem in ui_elements): 
                        gameOver() 
                        
                        
                    updateDict(ui_elem)    
                   
            if btnOK.collidepoint(event.pos): 
                current_player = int(not current_player)
                font = pygame.font.SysFont('Georgia', 28, bold=True)
                
                activateRows(ui_elements, current_row)
                
                if current_player == 1:
                    player1(window, font, white, gray)
                    
            
                else: 
                    player2(window, font, white, gray)
                    

     
    return True            
      
def activateRows(ui_elements, current_row):
 
    for button in ui_elements:
        if button.row_act == False and button.row_nmb != current_row:
            button.row_act = True


        
def disableRows(ui_elements, current_row): 
    for button in ui_elements:
        if button.row_nmb != current_row and button.enabled != False:
            button.row_act = False
          #  if button in deleted_buttons:
           #    continue        
def updateDict(ui_elem):
    if ui_elements.index(ui_elem) == 0: 
        ui_dict[1] -= 1
        print(ui_dict)
        
    elif 1 <= ui_elements.index(ui_elem) <=3:
        ui_dict[2] -= 1 
        print(ui_dict)
        
    elif 4 <=  ui_elements.index(ui_elem) <= 8:  
        ui_dict[3] -= 1
        print(ui_dict)
        
    elif 9 <=  ui_elements.index(ui_elem) <= 15:      
        ui_dict[4] -= 1
        print(ui_dict)
        
                    
def gameOver():
    red = (136, 8, 8)
    window.fill('black') 
    font = pygame.font.SysFont('Georgia', 28, bold=True)    
    gameover = font.render('| GAME OVER: Player %s looses |' % players[current_player], True,red)
    window.blit(gameover, (150, 600)) 
    


init() 

ui_elements = createButtons()
btnOK = createOKButton()
current_player = pickFirstPlayer()
run = True  
while run:
    
    run = user_input(ui_elements, btnOK)
    drawButtons(window, ui_elements)
    pygame.display.flip()
   
  
pygame.quit()


