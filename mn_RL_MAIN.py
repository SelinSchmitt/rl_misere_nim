#the following code provides the main game user interface to play Misére-Nim against a trained ai

import pygame
import secrets
import random
import ast
from Button import Button




#open final qtable file
with open('final_qtable_mn.txt', 'r') as file:
    content = file.read()
    qtable = eval(content)
#print(qtable)  


def init():
    
    global enabled 
    global row_nmb
    global row_act
    
    global simulateclick
    global gameover
    
    global window
    global current_player
    global players 
    
    global npc_dict
    global button_dict
    global updatedDict
    
    global epsilon
    
    npc_dict ={1:1, 2:3, 3:5, 4:7}


    players = [2, 1]
    current_player = secrets.randbelow(len(players))
    
    enabled = True
    row_nmb = 0
    row_act = True
    
    gameover = False
    simulateclick = True
    
    updatedDict = {}
    epsilon = 0.2
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
    #current_player = 1
    
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


def startKI(updatedDict): 
        #ai chooses max action from qtable
        current_state = list(updatedDict.values())
        if current_state:
            for outer_dict, inner_dict in qtable.items(): 
                if str(current_state) == outer_dict:
                    for k, v in qtable[outer_dict].items(): 
                        inner_dict = qtable[outer_dict] 
                        max_wert = max(inner_dict, key=lambda x: inner_dict[x])
                        max_value = ast.literal_eval(max_wert)
                      
                        return max_value
                    
        else:
            for outer_dict, inner_dict in qtable.items():
                if str(outer_dict) == outer_dict:
                    for k, v in qtable[outer_dict].items(): 
                        inner_dict = qtable[outer_dict] 
                        max_wert = max(inner_dict, key=lambda x: inner_dict[x])
                        max_value = ast.literal_eval(max_wert)
                        return max_value



def kiRemoveButtons(updatedDict, button_dict, max_value):
    #ai removes the chosen buttons
    global simulateclick
    button_dict.update()

    random_k = max_value[0]
    random_v = max_value[1]
    
    if random_k == 1:
        my_set = button_dict[1]
        remove_buttons = random.sample(my_set, random_v)
        for button in remove_buttons:
           button.enabled = False
           button_dict[1].remove(button)
        updatedDict[random_k] -= random_v
        
    elif random_k == 2:
        my_set = button_dict[2]
        enabled_buttons = [button for button in my_set if button.enabled == True]
        remove_buttons = random.sample(enabled_buttons, random_v)
        for button in remove_buttons:
           button.enabled = False
           button_dict[2].remove(button)
        updatedDict[random_k] -= random_v

    elif random_k == 3:
        my_set = button_dict[3]
        enabled_buttons = [button for button in my_set if button.enabled == True]
        remove_buttons = random.sample(enabled_buttons, random_v)
        for button in remove_buttons:
           button.enabled = False
           button_dict[3].remove(button) 
        updatedDict[random_k] -= random_v
        
    elif random_k == 4: 
        my_set = button_dict[4]
        enabled_buttons = [button for button in my_set if button.enabled == True]
        remove_buttons = random.sample(enabled_buttons, random_v)
        for button in remove_buttons:
           button.enabled = False
           button_dict[4].remove(button)
        updatedDict[random_k] -= random_v
    
       
    if all(ui_elem.enabled == False for ui_elem in ui_elements): 
        gameOver() 
        simulateclick = False
      
        
    return updatedDict
    
     
def createButtons():
    black = (0, 0, 0)
    purple = (255, 0, 255)
    
    
    set1 = set()
    set2 = set()
    set3 = set()
    set4 = set()
    
    window = pygame.display.get_surface()
    window.fill(black)    
 
    x_btn = 350
    y_btn = 100
    
    for x in range(1):  
        btn1 = Button(x_btn, y_btn, purple,1, enabled) 
        set1.add(btn1)
      
     
    for y in range(3):
        btn2 = Button(x_btn-50, y_btn+100,purple, 2, enabled) #2
        x_btn += 50 
        set2.add(btn2)
        
              
    for z in range(5):        
        btn3 = Button(x_btn-250, y_btn+200,purple,3, enabled) #3
        x_btn += 50
        set3.add(btn3)
        
        
    for w in range(7):        
        btn4 = Button(x_btn-550, y_btn+300, purple,4, enabled) #4
        x_btn += 50  
        set4.add(btn4)
   
       
    return set1, set2, set3, set4


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

def user_input(ui_elements, btnOK, button_dict):
    global current_player
    global npc_dict
    global updatedDict
    
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
      
                     
                    updatedDict = updateHumanDict(ui_elem, npc_dict) 
    
                       
            if btnOK.collidepoint(event.pos):
                current_player = int(not current_player)
                font = pygame.font.SysFont('Georgia', 28, bold=True)
                
                activateRows(ui_elements, current_row)

                if current_player == 1:
                    player1(window, font, white, gray) 
                                
                else: 
                    player2(window, font, white, gray)
                    max_value = startKI(updatedDict)
                    kiRemoveButtons(updatedDict, button_dict, max_value)
                    simulateButtonClick()

    return True

         
def simulateButtonClick():
    global simulateclick
    
    if simulateclick:
        pos= btnOK.center
        button = btnOK
        click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=button, pos=pos)
        pygame.event.post(click_event) 
    else:
        simulateclick = False

    
    

    
def activateRows(ui_elements, current_row):
 
    for button in ui_elements:
        if button.row_act == False and button.row_nmb != current_row:
            button.row_act = True


        
def disableRows(ui_elements, current_row): 
    for button in ui_elements:
        if button.row_nmb != current_row and button.enabled != False:
            button.row_act = False


    
def updateHumanDict(ui_elem, npc_dict):
    if ui_elem in set1:
        npc_dict[1] -= 1
    elif ui_elem in set2:
        npc_dict[2] -= 1 
        
    elif ui_elem in set3:  
        npc_dict[3] -= 1
        
    elif ui_elem in set4:      
        npc_dict[4] -= 1
        
    return npc_dict  

    if ui_elements.index(ui_elem) == 0:
        npc_dict[1] -= 1
    elif 1 <= ui_elements.index(ui_elem) <=3:
        npc_dict[2] -= 1 
        
    elif 4 <=  ui_elements.index(ui_elem) <= 8:  
        npc_dict[3] -= 1
        
    elif 9 <=  ui_elements.index(ui_elem) <= 15:      
        npc_dict[4] -= 1
        
    return npc_dict   


def createButtonDict():
    button_dict = {}
    button_dict[1] = set1
    button_dict[2] = set2
    button_dict[3] = set3
    button_dict[4] = set4

  
    
    return button_dict      
             
def gameOver():
    red = (136, 8, 8)
    window.fill('black') 
    font = pygame.font.SysFont('Georgia', 28, bold=True)    
    gameover = font.render('| GAME OVER: Player %s looses |' % players[current_player], True,red)
    window.blit(gameover, (150, 600)) 

    


init() 

set1, set2, set3, set4 = createButtons() #erstelle buttons
ui_elements = set1.union(set2, set3, set4) #set von allen sets

btnOK = createOKButton()
current_player = pickFirstPlayer()
button_dict = createButtonDict()

if current_player == 0:
    pygame.time.delay(1000) 
    startKI(npc_dict) 
    max_value= startKI(updatedDict) 
    new_dict = kiRemoveButtons(npc_dict, button_dict, max_value)  
    simulateButtonClick()
    
run = True  
while run:
    
    run = user_input(ui_elements, btnOK, button_dict)
    drawButtons(window, ui_elements)
    pygame.display.flip()
    

  
pygame.quit()

