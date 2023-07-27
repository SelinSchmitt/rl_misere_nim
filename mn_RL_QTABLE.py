import secrets
import random


def init():
    global players
    global current_player
    global my_dict

    global saved_moves
    global epsilon
    
    
    players = [2, 1]
    current_player = secrets.randbelow(len(players))


    my_dict = {1:1, 2:3, 3:5, 4:7}
    saved_moves = []

    epsilon = 0.2

    
    print('Choose a row and then the number you want to subtract from that pile.')
    print('Please note that the pile ends at 0')
    
    for key, value in my_dict.items():
        print('Pile ', key,': ',  value)


       
def playGame(): 
    global current_player
    global my_dict
    global epsilon

    current_player = int(not current_player)
    beginnging_Player = current_player
    available_keys = [key for key in my_dict if my_dict[key] != 0]

    #epsilon-greedy:
    #line 72 references to 'Nedialkov, Python Max Lambda [6 ways], https://iq.opengenus.org/python-max-lambda/ '
    if episode < 100000: 
        print('Exploration unter 100000')
        random_key = random.choice(available_keys)
        values = my_dict[random_key]
        random_value = random.randint(1,values)
        saved_key = (random_key, random_value)
        print('Player %s pick Pile: ' % players[current_player], random_key )
        print('How many do you want to subtract?: ', random_value)
        makeMove(saved_key, random_key, random_value)
            
    else: 
        if random.random() < epsilon: 
            print('Exploration über 100000')
            random_key = random.choice(available_keys)
            values = my_dict[random_key]
            random_value = random.randint(1,values)
            saved_key = (random_key, random_value)
            print('Player %s pick Pile: ' % players[current_player], random_key )
            print('How many do you want to subtract?: ', random_value)
            makeMove(saved_key, random_key, random_value)            
        
        else: 
            print('Ausbeutung')
            for outer_dict, inner_dict in qtable.items(): 
                values_list = list(my_dict.values())
                if str(values_list) in outer_dict:
                    current_state = qtable[str(values_list)]
                    print('current state ', current_state)
                    max_value = max(current_state.values())
                    max_key = max(current_state.items(), key=lambda x: x[1])[0] 
                    print('best action with highest q-value',max_key,  max_value)
                    saved_key = max_key
                    random_k= int(max_key[1]) 
                    random_v = int(max_key[4])
                    print('search in qtable', random_k, random_v)
                    print('Player %s pick Pile: ' % players[current_player], random_k )
                    print('How many do you want to subtract?: ', random_v)
                    makeMove(saved_key, random_k, random_v)                    
                
   
def makeMove(saved_key, k, v):
    if k in [1,2,3,4,5,6,7,0] and  my_dict[k] - v >= 0:  
        original_value = list(my_dict.values()) 

        updatedDict = subtract(my_dict, k, v)

        list_values = list(updatedDict.values())
        moves = (original_value, saved_key)  

        saved_moves.append(moves)
   
        for key, value in my_dict.items():
            print('Pile', key, ':', value)

    else:
        print("not possible")

     
def subtract(my_dict, entry, sub): 
    
    if(entry == 1):
        my_dict[1] -= sub
                
    elif(entry == 2):
        my_dict[2] -= sub
                    
    elif(entry == 3):
        my_dict[3] -= sub
            
    elif(entry == 4):
        my_dict[4] -= sub
        
    return my_dict  

def getReward(tmp_dict):
    pos_reward = 1
    neg_reward = -1
   
    items = list(tmp_dict.items()) 
    for state, value in items[::-2]: 
        inner_dict = tmp_dict[state]  
        for key in inner_dict:
            inner_dict[key] = neg_reward 
     
            
    for state2, value in items[-2::-2]: 
        inner_dict = tmp_dict[state2]
        for key2 in inner_dict:
            inner_dict[key2] = pos_reward  
          
    
  
def InitializeTable(saved_moves, tmp_dict):
    # Line 147 references to  Tutorials Teacher, Python Dictionary setdefault() Method, 
    #https://www.tutorialsteacher.com/python/dict-setdefault?utm_content=cmp-true
    tmp_dict = {}
    for move in saved_moves:

        tmp_dict_key = move[0]
        tmp_dict_state = str(tmp_dict_key)
        tmp_dict.setdefault(tmp_dict_state, {}) 
        tmp_list = eval(tmp_dict_state) 
        if move[0]  == tmp_list:   
            inner_key = move[1]
            inner_dict = tmp_dict[tmp_dict_state] 
            inner_dict.setdefault(str(inner_key), 0) 
            getReward(tmp_dict)   

    return tmp_dict  
    


episodes = 200000
tmp_dict = {}
qtable = {}
new_value = 0
for episode in range(episodes):
    init()  
 
    while True:
        playGame()
          
        if all(value == 0 for value in my_dict.values()):
            tmp_dict = InitializeTable(saved_moves, tmp_dict)

            print('temporary dict: ', tmp_dict)
           
    
            for outerkey, in_dict in tmp_dict.items():
                str_outerkey = str(outerkey) 
                inner_items = next(iter(in_dict.items()))
                key = inner_items[0]
                value = inner_items[1]
                
                if str_outerkey in qtable: 
                    known_moves =  qtable.get(str_outerkey) 
                    
                    if known_moves is not None:
                        if key in known_moves: 
                            print("key in knowm moves: ", key)
                            old_value = known_moves.get(key,value) 
                            
                  
                            new_value = old_value + value
                            
                            print('new value', new_value, 'old value', old_value, 'reward', value)
                            
                        else:
                            
                            new_value = value 
                      
   
                        known_moves.update({key: new_value}) 
                        
                else: # situation is not in qtable
             
                    new_dic = {}
                    new_dic.update({key: value})
                    qtable[str_outerkey] = new_dic
 
            print(qtable)
            break

            
