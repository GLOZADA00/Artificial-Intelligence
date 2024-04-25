import random

def main():
    f = open("EightQueensAndPuzzle\EightQueensProblem\eightQueensTest.txt", "wb")
    testCaseCount = 150
    board = ""
    while testCaseCount > 0:
        testCaseCount -= 1
        for col in range(0,7):
            board += str(random.randint(0,7)) + ' '
        board += str(random.randint(0,7)) + '\n'
    print(board)
    f.write(board)
    f.close()
    
if __name__ == '__main__':
    main()