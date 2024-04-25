'''
@author: HYPJUDY
'''
import random
import time

search_cost = 0

FAILED = False

def getCollisionNum(board):
    num = 0
    for col in range(len(board)):
        for anotherCol in range(col+1, len(board)):
            if board[col] == board[anotherCol]:
                num += 1 # collied in the same row
            elif abs(board[col] - board[anotherCol]) == (anotherCol - col):
                num += 1 # collied diagonally
    return num

# for each column, calculate the collision number
# if the queen is moved to the other rows
# find the smallest one and move to it.
def step_steepestHillClimbing(board):
    global search_cost
    collisionNumBoard = {}
    smallestCollisionNum = getCollisionNum(board)
    for col in range(len(board)):
        for row in range(len(board)):
            if board[col] == row:
                continue
            originRow = board[col]
            board[col] = row
            collisionNumBoard[(row,col)] = getCollisionNum(board)
            board[col] = originRow
    
    
    for point,value in collisionNumBoard.items():
        if value < smallestCollisionNum:
            smallestCollisionNum = value
    
    smallestCollisionPoints = []
    for point,value in collisionNumBoard.items():
        if value == smallestCollisionNum:
            smallestCollisionPoints.append(point)
    
    # can not find a steeper move
    # we have come to the peek(local optimization)
    if len(smallestCollisionPoints) == 0:
        #print "local optimization"
        global FAILED
        FAILED = True
        search_cost += 1
        return board
    
    random.shuffle(smallestCollisionPoints)
    board[smallestCollisionPoints[0][1]]=smallestCollisionPoints[0][0]
    search_cost += 1
    return board

def solution_steepestHillClimbing(board):
    global search_cost
    maxRound = 200
    count = 0
    while True:
        collisionNum = getCollisionNum(board)
        if collisionNum == 0:
            return board
        board = step_steepestHillClimbing(board)
        count += 1
        if(count >= maxRound):
            global FAILED
            FAILED = True
            return board
    
def SHC_Q():
    global search_cost
    title = "EightQueens_steepestHillClimbing"
    startTime = time.time()
    successCase = 0
    totalCase = 0
    result = title + " result:\n\n"
    with open("Queens\EightQueensTest2.txt", "r") as ins:
        for line in ins:
            # print ("case: ", totalCase)
            global FAILED
            FAILED = False
            totalCase += 1
            board = []
            for col in line.split():
                board.append(int(col))
            board = solution_steepestHillClimbing(board)
            if FAILED:
                result += "Failed!"
            else:
                successCase += 1
                for col in range(len(board)):
                    result += str(board[col]) + " "
            result += "\n"
    
    endTime = time.time()
    result += "\nTotal time: " + str(endTime - startTime) + '\n'
    result += "Total case number: " + str(totalCase) + ", Success case number: " + str(successCase) + '\n'
    result += "Success rate: " + str(successCase / float(totalCase)) + '\n'
    result += "Average cost: " + str(search_cost / float(totalCase)) + '\n'
    print (result)
    
    f = open(title + '.txt', 'w')
    f.write(result)
    f.close()
    
    return (successCase / float(totalCase), search_cost/totalCase)