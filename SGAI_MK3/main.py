from dataclasses import dataclass
from numpy import isin
import pygame
from Board import Board
import PygameFunctions as PF
import random as rd 
import copy
from QStats import QStats 
from DataCollector import DataCollector

# Constants
ROWS = 6
COLUMNS = 6
BORDER = 150                    # Number of pixels to offset grid to the top-left side
CELL_DIMENSIONS = (100,100)     # Number of pixels (x,y) for each cell
ACTION_SPACE = ["moveUp", "moveDown", "moveLeft", "moveRight", "vaccinate", "heal", "kill"]
SELF_PLAY = True
AI_PLAY_WAITTIME_MS = 50

# Player role variables
player_role = "Government"      # Valid options are "Government" and "Zombie"
roleToRoleNum = {"Government": 1, "Zombie": -1}
roleToRoleBoolean = {"Government": False, "Zombie": True}       # False means Human, True means Zombie. Switching this would turn Humans to Zombies, and vice versa. 

# Initialize variables
running = True
take_action = []
playerMoved = False
font = pygame.font.SysFont("Comic Sans", 20)
self_play = False
hospital = False
trainAI = False
epochs = 1000
epochs_ran = 0
qStats = QStats()
qStats.ethicsChart()

# Option menu
SelfPlayButton = pygame.Rect(350, 250, 100, 100)
HospitalOnButton = pygame.Rect(700, 250, 100, 100)
ProceedButton = pygame.Rect(1050, 650, 100, 100)

proceed = False
hover = ""
while proceed == False:
    for event in pygame.event.get():
        PF.display_options_screen(self_play, hospital, hover)
        hover = ""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if SelfPlayButton.collidepoint(pygame.mouse.get_pos()):
                self_play = not self_play
            elif HospitalOnButton.collidepoint(pygame.mouse.get_pos()):
                hospital = not hospital
            elif ProceedButton.collidepoint(pygame.mouse.get_pos()):
                proceed = True
        elif event.type == pygame.MOUSEMOTION:
            if ProceedButton.collidepoint(pygame.mouse.get_pos()):
                hover = "proceed"
            elif HospitalOnButton.collidepoint(pygame.mouse.get_pos()):
                hover = "hospital"
            elif SelfPlayButton.collidepoint(pygame.mouse.get_pos()):
                hover = "self" 
        elif event.type == pygame.QUIT:
            pygame.quit()

#Repurposing self_play logic to train AI
if self_play:        
    trainAI = True

#Create the game board
GameBoard = Board((ROWS,COLUMNS), BORDER, CELL_DIMENSIONS, roleToRoleNum[player_role], hospital, trainAI, qStats)
GameBoard.populate()
DataCollector.hospital = hospital

# Self play variables
alpha = 0.1
gamma = 0.6
epsilon = 0.1
epochs = 1000
epochs_ran = 0
Original_Board = GameBoard.clone(GameBoard.States)
clock = pygame.time.Clock()
frame = 0 
hovering = ""
action_type = ""

# Buttons
kill_img = pygame.image.load("Assets/kill_button.png").convert_alpha()
#KillButton = kill_img.get_rect(topleft=(800, 50))

heal_img = pygame.image.load("Assets/heal_button.png").convert_alpha()
#HealButton = heal_img.get_rect(topleft=(800, 200))

kill_button = "button"
heal_button = "button"

while running:
    P = PF.run(GameBoard, hospital, heal_button, kill_button)

    if qStats.totalGames % 10 == 0:
        qStats.visualize()
    if epochs_ran % 1000 == 0:
        print("Game Draw - Epochs ran out!")     
        GameBoard.gameFinished()
        qStats.addDraw()
    
    pygame.time.wait(AI_PLAY_WAITTIME_MS)

    qTable = [[0]*7]*ROWS*COLUMNS
    for r in range(ROWS*COLUMNS-1):
        for c in range(7):
            qTable[r][c] = GameBoard.QTable[r][c]
    reward = []
    attempts = 0
    max_attempts = 300
    while attempts != max_attempts: 
        i = 0
        r = rd.uniform(0.0, 1.0)

        # Chooses random action - exploration
        if r < gamma:            
            i = rd.randint(0, len(GameBoard.States) - 1)
            state = qTable[i]
            while GameBoard.States[i].person is None:
                i = rd.randint(0, len(GameBoard.States) - 1)
                state = qTable[i]                    

        # Chooses best action - exploitation
        else:
            biggest = None
            for x in range(len(GameBoard.States)):
                arr = qTable[x]
                exp = sum(arr) / len(arr)
                if biggest is None:
                    biggest = exp
                    i = x
                elif biggest < exp:
                    biggest = exp
                    i = x
            state = qTable[i]
        
        b = 0
        j = 0
        ind = rd.randint(0, len(state) - 1)
        for v in state:
            if v > b:
                b = v
                ind = j
            j += 1

        action_to_take = ACTION_SPACE[ind] #actual action e.g. cure bite etc
            
        old_qval = b
        old_state = i
    
        # Update and get reward for current move
        reward = GameBoard.act(old_state, action_to_take)
        if reward[1] is None or reward[1] > 35 or reward[1] < 0:
            attempts+=1
            qTable[old_state][ind] = 0
        else:
            break #found a valid move

        if attempts == max_attempts-1:
            qStats.saveQTable(qTable,"Qbkp.txt")
            
    if (attempts == max_attempts):
        print("Board Reset - Unable to make a move!")             
        GameBoard.gameOver()
        qStats.addError()
    else:
        ns = reward[1] #what state (0-35)
        NewStateAct = GameBoard.QGreedyat(ns) # action_index, qvalue
        NS = GameBoard.QTable[ns][NewStateAct[0]] #state, action_index
        
        #Update QTable
        GameBoard.QTable[old_state][ind] = GameBoard.QTable[old_state][ind] + alpha * (reward[0] + gamma * NS - GameBoard.QTable[old_state][ind])            

        #UPDATE 
        statecor = GameBoard.toCoord(ns)
        print("AI's current action: " + str(action_to_take)) 
        print("AI's action coord: " + str(statecor))
        if action_to_take == "moveUp":
            GameBoard.moveUp(statecor)
        elif action_to_take == "moveDown":
            GameBoard.moveDown(statecor)
        elif action_to_take == "moveLeft":
            GameBoard.moveLeft(statecor)
        elif action_to_take == "moveRight":
            GameBoard.moveRight(statecor)
        elif action_to_take == "heal":
            GameBoard.heal(statecor)
            DataCollector.zombies_cured+=1
        elif action_to_take == "vaccinate":
            GameBoard.heal(statecor)
            DataCollector.humans_vaccinated+=1
        elif action_to_take == "kill":
            GameBoard.kill(statecor)
            DataCollector.zombies_killed+=1

        if GameBoard.num_zombies() <= 1:
            print("Humans Win!") 
            GameBoard.gameFinished()
            qStats.addWin()

        # Zombies turn
        take_action = []        
        GameBoard.zombie_random_move()
        GameBoard.update()


        if GameBoard.num_humans() == 0:
            print("Zombies Win")
            GameBoard.gameFinished()
            qStats.addLose()
    
        epochs_ran+=1
        DataCollector.turns_taken+=1

    for event in P:
        if event.type == pygame.QUIT:
            running = False
            break
            
    # Update the display
    pygame.display.update()    
    
    print("\n")        
