#the following code provides a terminal version of Misére-Nim
import secrets

#line 7 and 8 are based on 'Secrets | Python module to Generate secure random numbers'
#https://www.geeksforgeeks.org/secrets-python-module-generate-secure-random-numbers/

players = [2, 1]
current_player = secrets.randbelow(len(players))

dict = {1:1, 2:3, 3:5, 4:7}


def playGame(current_player):

    try:

        print(dict.items())
        
        while True:
            current_player = int(not current_player)
            
            entry = int(input('Player %s pick Pile: ' % players[current_player] ))
            sub = int(input('How many do you want to subtract?: ')) 

            if sub in [1,2,3,4,5,6,7,0]: 
                subtract(entry, sub)
            
                if(dict[1] < 0) or (dict[2] < 0) or (dict[3] < 0) or (dict[4] < 0):
                    print('not possible')
                    break    
                            
                gameOver() 
                    
                dict.update 
                print(dict.values())
                
            else: 
                print('illegal move')    
                print(dict.values())    
                
    except:
        print(' ')
       
def subtract(entry, sub):
    if(entry == 1):
        dict[1] -= sub
                
    elif(entry == 2):
        dict[2] -= sub
                    
    elif(entry == 3):
        dict[3] -= sub
            
    elif(entry == 4):
        dict[4] -= sub
        
 
def gameOver(): #gameover
    if(any(dict.values()) == False): 
        print() 
        print('GAME OVER: Player %s looses' % players[current_player])
        print() 
        quit()                    

print('Choose a row and then the number you want to subtract from that pile.')
print('Please note that the pile ends at 0')  
playGame(current_player)



        


    


