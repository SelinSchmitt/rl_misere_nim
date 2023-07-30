#the following code provides a npc player that simulates the winning strategy of misere nim
#code structure is based on the tutorial 'Prof. Dr. Oliver Hofmann, 2D-Spiele mit pygame, https://www.youtube.com/watch?v=_B5qc3jtPIE'
import pygame
import secrets
import random
from Button import Button



def init():
    
    global enabled 
    global row_nmb
    global row_act

    global window
    global current_player
    global players 
    
    global npc_dict
    global button_dict
    
    npc_dict ={1:1, 2:3, 3:5, 4:7}


    players = [2, 1]
    current_player = secrets.randbelow(len(players))
    
    enabled = True
    row_nmb = 0
    row_act = True
  
    
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


           
def startNPC(updatedDict, button_dict): 
    updated_by_npc_dict = {}
    print(updatedDict)
     
    if (any(updatedDict.keys())>= 0):
        keys_left = [key for key in updatedDict.keys() if updatedDict[key] != 0]

        random_k, random_v = chooseRandomNumbers(updatedDict) 

        nimsum = possible_nimsum(updatedDict,random_k, random_v) 
        
        checkForExceptions(keys_left, updatedDict, button_dict, random_k, random_v)
        if not checkForExceptions(keys_left, updatedDict, button_dict, random_k, random_v):
            if nimsum == 0 :  
                updated_by_npc_dict = npcRemoveButtons(updatedDict, button_dict, random_k, random_v)
                print(updated_by_npc_dict)
                print('key: ', random_k,'value: ', random_v, 'nim: ', nimsum) 

           
            elif len(keys_left) == 2 and list(updatedDict.values()).count(1) == 2:    
                random_v = 1
                updated_by_npc_dict = npcRemoveButtons(updatedDict, button_dict, random_k, random_v)
                print('key: ', random_k,'value: ', random_v, 'nim: ', nimsum) 
                
            else: 
                random_k, random_v = chooseRandomNumbers(updatedDict)
                updated_by_npc_dict = npcRemoveButtons(updatedDict, button_dict, random_k, random_v)
                print('zufällige Zahl')
                

   
    else:
        print("GAMEOVER")

def checkForExceptions(keys_left, updatedDict, button_dict, random_k, random_v):
    #check for exceptions in the game
    exception = False
    keys_left = [key for key in updatedDict.keys() if updatedDict[key] != 0]
    if list(updatedDict.values()).count(1) == 2: #1, 1, ...
        largest_pile = max(updatedDict, key=updatedDict.get) 
        largest_value = max(updatedDict.values())
        print('LARGEST PILE = ',largest_pile)
        
        my_set = button_dict[largest_pile]
        enabled_buttons = [button for button in my_set if button.enabled == True]
        remove_buttons = random.sample(enabled_buttons, largest_value-1) 
    
        for button in remove_buttons:
           button.enabled = False
           button_dict[largest_pile].remove(button)
        updatedDict[largest_pile] -= largest_value-1
        
        exception = True
        return exception 
    
    elif list(updatedDict.values()).count(2) >= 1 and list(updatedDict.values()).count(1) == 1:  #1, 2, 2
        smallest_keys = []
        for key in updatedDict:
            if updatedDict[key] > 0:
                smallest_keys.append(key)

        smallest_pile = min(smallest_keys, key=updatedDict.get)
      
        smallest_value = updatedDict[smallest_pile]
        print('SMALLEST PILE = ',smallest_pile)
        print('SMALLEST VALUE = ',smallest_value)
        
        my_set = button_dict[smallest_pile] 
        enabled_buttons = [button for button in my_set if button.enabled == True] 
        remove_buttons = random.sample(enabled_buttons, smallest_value) 
    
        for button in remove_buttons:
           button.enabled = False
           button_dict[smallest_pile].remove(button)
        updatedDict[smallest_pile] -= smallest_value
        
        exception = True
        return exception 
    
    elif len(keys_left) == 2 and (list(updatedDict.values()).count(1) == 1 or list(updatedDict.values()).count(2) >= 1): 
        largest_pile = max(updatedDict, key=updatedDict.get) 
        largest_value = max(updatedDict.values())
        print('LARGER PILE = ',largest_pile)
        
        my_set = button_dict[largest_pile]
        enabled_buttons = [button for button in my_set if button.enabled == True]
        remove_buttons = random.sample(enabled_buttons, largest_value) 
    
        for button in remove_buttons:
           button.enabled = False
           button_dict[largest_pile].remove(button)
        updatedDict[largest_pile] -= largest_value
        
        exception = True
        return exception  
    

    elif len(keys_left) == 1:#0, 2
        value = updatedDict[random_k]
        if value == 2:
            print('ENDSPURT 1')
            my_set = button_dict[random_k]
            
            random_v = 1
            enabled_buttons = [button for button in my_set if button.enabled == True]
            remove_buttons = random.sample(enabled_buttons, random_v) 
        
            for button in remove_buttons:
                button.enabled = False
                button_dict[random_k].remove(button)
            updatedDict[random_k] -= random_v 
            exception = True
            return exception
        
        elif value > 2: #0, 5
            print('ENDSPURT 2')
            my_set = button_dict[random_k]
            largest_value = max(updatedDict.values())
            random_v = largest_value - 1
            enabled_buttons = [button for button in my_set if button.enabled == True]
            remove_buttons = random.sample(enabled_buttons, random_v) 
        
            for button in remove_buttons:
                button.enabled = False
                button_dict[random_k].remove(button)
            updatedDict[random_k] -= random_v 
            exception = True
            return exception            
            
        else:
            return             
      
    elif len(keys_left) >= 3 and (list(updatedDict.values()).count(2) == 1 and list(updatedDict.values()).count(3) == 1):
        
        print("test)")
    else:
        return
        
    
def npcRemoveButtons(updatedDict, button_dict, random_k, random_v):
    button_dict.update()
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
      
        
    return updatedDict
    
     
def chooseRandomNumbers(updatedDict):
  
    available_keys = [key for key in updatedDict if updatedDict[key] != 0]
    if available_keys: #wenn keys da sind
        random_key = random.choice(available_keys)
        values = updatedDict[random_key]
        random_value = random.randint(1,values)
        return random_key, random_value

    else:
        return None, None 


def possible_nimsum(updatedDict, random_k, random_v): 
     
    if random_k in updatedDict and random_v> 0:

        copy = updatedDict.copy()
        copy[random_k] -= random_v
        result = 0
        for values in copy.values(): 
            binary =  format(values, '04b')
            print('Value: ',values,  'Binärzahl ', binary) 
     
            binary_int = int(binary, 2)
            result ^= binary_int
        
        nimsum = format(result, '04b')
        print(nimsum, result)
        
        if '1' in nimsum:
            result = 1
            return result
        else:
            result =  0
            return result
         
        #alternative to the nimsum   
        #if result % 2 == 0:
        #    result= 0
        #    return result            
        #else:
        #    result=1
        #    return result    
        
     
         

      
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
      
                     
                    updatedDict = updateHumanDict(ui_elem, npc_dict) #return dict updated by the human
    
                       
            if btnOK.collidepoint(event.pos):
                current_player = int(not current_player)
                font = pygame.font.SysFont('Georgia', 28, bold=True)
                
                activateRows(ui_elements, current_row)

                if current_player == 1:
                    player1(window, font, white, gray) 
                                
                else: 
                    player2(window, font, white, gray)
                    startNPC(updatedDict, button_dict) #give the updated dict to the npc player
                    simulateButtonClick() 

                

    return True

         
def simulateButtonClick():
   #simuale a button click if the npc player starts the game
    pos= btnOK.center
    button = btnOK
    click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=button, pos=pos)
    pygame.event.post(click_event)  

    
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



def createButtonDict():
    button_dict = {}
    button_dict[1] = set1
    button_dict[2] = set2
    button_dict[3] = set3
    button_dict[4] = set4

  
    
    return button_dict      
             
def gameOver():
    red = (136, 8, 8)
    window.fill('black') #screen leeren
    font = pygame.font.SysFont('Georgia', 28, bold=True)    
    gameover = font.render('| GAME OVER: Player %s looses |' % players[current_player], True,red)
    window.blit(gameover, (150, 600)) 
    
    


init() 


set1, set2, set3, set4 = createButtons() 
ui_elements = set1.union(set2, set3, set4) #save all sets of the rows into one set

btnOK = createOKButton()
current_player = pickFirstPlayer()
button_dict = createButtonDict()

if current_player == 0:
    pygame.time.delay(1000) 
    startNPC(npc_dict, button_dict)
    simulateButtonClick()
    
run = True  
while run:
    
    run = user_input(ui_elements, btnOK, button_dict)
    drawButtons(window, ui_elements)
    pygame.display.flip()

  
pygame.quit()


   
