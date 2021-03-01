#Solves Sudoku puzzles

import numpy as np
import sys
import random
import pandas as pd


def newPage():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
def printPuz(puz):
    newPage()
    for i in range(len(puz)):
        if i==3 or i==6:
            print("----------------------")
        for j in range(len(puz)):
            if j==3 or j==6:
                sys.stdout.write("| ")
            
            
            
            if puz[i,j] == 0:
                sys.stdout.write("  ")
            elif puz[i,j] == 99:
                sys.stdout.write("_ ")
            else:
                sys.stdout.write(str(puz[i,j])+" ")
        print("")	        
def canValueFitHere(puz, value, position):
            i = position[0]
            j = position[1]
            
            toRemove = []
            for num in potential: 
                if num in puz[i,:]:
                    toRemove.append(num)
                if num in puz[:,j]:
                    toRemove.append(num)
                quad = [int(i/3), int(j/3)]
                content = puz[quad[0]*3:(quad[0]+1)*3,quad[1]*3:(quad[1]+1)*3]
                flat_list = [item for sublist in content for item in sublist]
                if num in flat_list:
                    toRemove.append(num)
            remaining = list(set(potential) - set(toRemove))
                
            if value in remaining:
                return True
            else:
                return False			
def iterate(puz):
    rowColBoxElim(puz)
    box(puz)
    row(puz)
    col(puz)
    lastSpaceLeftRow(puz)
    #lastSpaceLeftColumn(puz)
def rowColBoxElim(puz):
    count = 0
    for i in range(len(puz)):
        for j in range(len(puz)):
            if puz[i,j] != 0:
                continue
            toRemove = []
            for num in potential:
                if num in puz[i,:]:
                    toRemove.append(num)
                if num in puz[:,j]:
                    toRemove.append(num)
                quad = [int(i/3), int(j/3)]
                content = puz[quad[0]*3:(quad[0]+1)*3,quad[1]*3:(quad[1]+1)*3]
                flat_list = [item for sublist in content for item in sublist]
                if num in flat_list:
                    toRemove.append(num)
            remaining = list(set(potential) - set(toRemove))
            if len(remaining) == 1:
                puz[i,j] = remaining[0]
                count +=1
                
            #print i, j, remaining
    #print count	
def box(puz):
    for x in range(3):
        for y in range(3):
            content = puz[x*3:(x+1)*3,y*3:(y+1)*3]
            flat_list = [item for sublist in content for item in sublist]
            
            missing = list(set(potential) - set(flat_list))
            
            #Finding global location of the empty spaces
            local_zero_positions = [e for e,value in enumerate(flat_list) if value == 0]
            global_zero_positions = []
            for zero in local_zero_positions:
                global_zero_positions.append([x*3 + int(zero/3), y*3 +(zero%3)])
                
            #can the first number in "missing" fit in exactly one space in the box?
            #if so, put it there
            for value in missing:
                potential_positions = []
                for position in global_zero_positions:
                    if canValueFitHere(puz, value, position) == True:
                        potential_positions.append(position)
                if len(potential_positions) == 1:
                    puz[potential_positions[0][0], potential_positions[0][1]] = value
def row(puz):
    for i in range(9):
        missing = list(set(potential) - set(puz[i,:]))
        
    #Finding global location of the empty spaces
        local_zero_positions = [e for e,value in enumerate(puz[i,:]) if value == 0]
        global_zero_positions = [[i, e] for e in local_zero_positions]
        
        #can the first number in "missing" fit in exactly one space in the row?
        #if so, put it there
        for value in missing:
            potential_positions = []
            for position in global_zero_positions:
                if canValueFitHere(puz, value, position) == True:
                    potential_positions.append(position)
            if len(potential_positions) == 1:
                puz[potential_positions[0][0], potential_positions[0][1]] = value
def col(puz):
    for j in range(9):
        missing = list(set(potential) - set(puz[:,j]))
        
    #Finding global location of the empty spaces
        local_zero_positions = [e for e,value in enumerate(puz[i,:]) if value == 0]
        global_zero_positions = [[j, e] for e in local_zero_positions]

        
        #can the first number in "missing" fit in exactly one space in the row?
        #if so, put it there
        for value in missing:
            potential_positions = []
            for position in global_zero_positions:
                if canValueFitHere(puz, value, position) == True:
                    potential_positions.append(position)
            if len(potential_positions) == 1:
                puz[potential_positions[0][0], potential_positions[0][1]] = value			
def lastSpaceLeftRow(puz):
    for i in range(len(puz)):
        if list(puz[i,:]).count(0) == 1:
            zero_pos = [e for e,value in enumerate(list(puz[i,:])) if value == 0]
            
            puz[i,zero_pos[0]] = list(set(potential) - set(list(puz[i,:])))[0]
def lastSpaceLeftColumn(puz):
    for j in range(len(puz)):
        if list(puz[:,j]).count(0) == 1:
            zero_pos = [e for e,value in enumerate(list(puz[:,j])) if value == 0]
            
            puz[zero_pos[0],j] = list(set(potential) - set(list(puz[:,j])))[0]					
def checkWin(puz):
    won = True
    for i in range(len(puz)):
        for j in range(len(puz)):
            if puz[i,j] == 0:
                won = False
    return won	

df = pd.read_csv('puzzles.csv')
puzzles = df.puzzle.values    
potential = [1, 2, 3, 4, 5, 6, 7, 8, 9]

puz = np.zeros((9,9), dtype="int") #Puzzle is initially blank, so user can fill in values

ux = 'Q'
while ux.upper() !='R' and ux.upper()!='U':
    ux = input('[R]andom puzzle, or [U]ser input? Enter R or U :')

if ux == 'R':
    puzzle = random.choice(puzzles)
    puz = np.array([[int(char) for char in puzzle[i*9:(i+1)*9]] for i in range(9)])
    done=True
else:
    for i in range(len(puz)):
        for j in range(len(puz)):
            puz[i,j] = 99 #code for underscore, to indicate where the next value will be entered on the puzzle
            printPuz(puz)
            input_=999
            while int(input_)>9 or int(input_)<0: # While loop to ensure valid input
                input_ = input("What is the value for position (" + str(i+1) + "," + str(j+1) + ")? (0 for blank) :" )
                try:
                    int(input_)
                except ValueError:
                    input_ = 999
                if int(input_)>9 or int(input_)<0:
                    print('Oops! Invalid value.')
                puz[i,j] = input_

while True:
    printPuz(puz)
    input("\nHit enter to iterate")
    iterate(puz)
    if checkWin(puz):
        break
        
printPuz(puz)
