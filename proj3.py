# File:    proj3.py
# Author: Adam Sachsel
# Date: 12/11/2018
# Lecture Section: 08
# Discussion Section: 10
# E-mail:  asachse1@umbc.edu
# Description: This program is a text-based version of the popular
# Sodoku puzzle game. The goal is to place digits from 1-9 in each 
# cell of the board so that no two digits repeat in the same 
# row, column, or 3x3 square. It can read in a puzzle form a file, 
# solve the puzzle, let user play numbers, undo previous moves, 
# check correct numbers, and check if the user won or lost their game.


################
### CONSTANTS ##
################

SOLVE_OR_PLAY = ["Solve", "Play"]
CORRECTION_CHECKER = ["Yes Correctness Checking", "No Correctness Checking"]
ACTION_CHOICES = ["Play number", "Undo", "Save", "Quit"]
NONET_ONE_MIN = 0
NONET_ONE_MAX = 2
NONET_TWO_MIN = 3
NONET_TWO_MAX = 5
NONET_THREE_MIN = 6
NONET_THREE_MAX = 8
NONET_RANGE = 3
MAX_ROW = 8
MIN_ROW = 0
MAX_COL = 8
MIN_COL = 0
MAX_NUM = 9
MIN_NUM = 1
BEGIN_BOARD = 0
END_OF_ROW = 9
END_OF_BOARD = 9
EMPTY_SPACE = 0




# ✔prettyPrint() prints the board with row and column labels,
#               and spaces the board out so that it looks nice
# Input:        board;   the square 2d game board (of integers) to print
# Output:       None;    prints the board in a pretty way
def prettyPrint(board):
    # print column headings and top border
    print("\n    1 2 3 | 4 5 6 | 7 8 9 ") 
    print("  +-------+-------+-------+")

    for i in range(len(board)): 
        # convert "0" cells to underscores  (DEEP COPY!!!)
        boardRow = list(board[i]) 
        for j in range(len(boardRow)):
            if boardRow[j] == 0:
                boardRow[j] = "_"

        # fill in the row with the numbers from the board
        print( "{} | {} {} {} | {} {} {} | {} {} {} |".format(i + 1, 
                boardRow[0], boardRow[1], boardRow[2], 
                boardRow[3], boardRow[4], boardRow[5], 
                boardRow[6], boardRow[7], boardRow[8]) )

        # the middle and last borders of the board
        if (i + 1) % 3 == 0:
            print("  +-------+-------+-------+")


# ✔savePuzzle() writes the contents a sudoku puzzle out
#              to a file in comma separated format
# Input:       board;    the square 2d puzzle (of integers) to write to a file
#              fileName; the name of the file to use for writing to 
def savePuzzle(board, fileName):
    ofp = open(fileName, "w")
    for i in range(len(board)):
        rowStr = ""
        for j in range(len(board[i])):
            rowStr += str(board[i][j]) + ","
        # don't write the last comma to the file
        ofp.write(rowStr[ : len(rowStr)-1] + "\n")
    ofp.close()

#############################
### MY PERSONAL FUNCTIONS ###
#############################

# ✔displayMenu() displays the list of choices to the user in an 
#               orderly fashion and associates a letter with each
# 		        of the options for the user to choose. 
# Input:	    choices; a list of choices the user can make
# 		        at this point.
# Output:	    none; None
def displayMenu(choices):
    print("\n")
    # Iterate through the choices
    for i in range(len(choices)):
        print(choices[i], end=" ")
        if (i != (len(choices) - 1)):
            print("or", end=" ")
    print("")
    # Iterate through the letters they can choose
    for i in range(len(choices)):
        print(choices[i] + " - (" + choices[i][0].lower() + ")")

# ✔getUserChoice() asks the user to select a choice from a list of choices
#                 continuously prompts the user until the choice is valid
#                 a valid choice is one that is a valid index in the list
# Input:          choices; a list of all the possible choices available
# Output:         choice; the validated choice that the user made
def getUserChoice(choices):

    validChoices = []
    userChoice = ""
    #Create list for valid choices
    for i in range(len(choices)):
        validChoices.append(choices[i][0].lower())
    while (userChoice not in validChoices):
        userChoice = input("Please choose an individual letter from"\
        " list above: ")
        # Incorrect Choice
        if (userChoice not in validChoices):
            print("That is not a valid choice.")
    return userChoice

# ✔getUserNumber()   takes in a desired number that the user wants to put into 
#                   the puzzle
# Input:            boardList; uses boardList to check coordinate
# Output:           userChoice; list of the row, column, and number user wishes
#                   to play.

def getUserNumber(boardList):
    userRow = 0
    userCol = 0
    userNum = 0
    spaceFull = True

    #Empty Space Validation
    while (spaceFull == True):
        spaceFull = False

        rowValid = False
        #Row Validation
        while (rowValid == False):
            userRow = (int(input("Enter a row number (1-9): ")) - 1)
            if (userRow >= MIN_ROW) and (userRow <= MAX_ROW):
                rowValid = True
            if (rowValid == False):
                print("That number is not in range for the row.")
        colValid = False
        #Column Validation
        while (colValid == False):
            userCol = (int(input("Enter a column number (1-9): ")) - 1)
            if (userCol >= MIN_COL) and (userCol <= MAX_COL):
                colValid = True
            if (colValid == False):
                print("That number is not in range for the column.")

        #Empty Check
        if (boardList[userRow][userCol] != EMPTY_SPACE):
            spaceFull = True
            print("That space is full please try again.")
    numValid = False
    #Number validation
    while (numValid == False):
        userNum = (int(input("Enter a number to put in cell (" +\
            str(userRow + 1) + "," + str(userCol + 1) + "): ")))
        if (userNum >= MIN_NUM) and (userNum <= MAX_NUM):
            numValid = True
        if (userNum < MIN_NUM) or (userNum > MAX_NUM):
            print("This number is not between 1 and 9")
    #Sudoku Rules
    if (checkSpot(userRow, userCol, userNum, boardList) == True):
        userList = [userRow, userCol, userNum]
        return userList
    #individual rules checking
    else:
        if (numberInRow(userRow, userNum, boardList) == True):
            print("The number " + str(userNum) + " is already in row.")
        if (numberInCol(userCol, userNum, boardList) == True):
            print("The number " + str(userNum) + " is already in column.")
        if (numberInBox(userRow, userCol, userNum, boardList) == True):
            print("The number " + str(userNum) + " is already in nonet.")
        return False

        
    

# ✔createBoardList() takes the contents of the sodoku file
#                   and turns the numbers into seperate lists
# Input:            puzzleFileName;   the name of the file that contains the 
#                   puzzle
# Output:           boardList;  the puzzle contents turned into a 2D list
def createBoardList(fileName):
    #Openning file
    originalFile = open(fileName, "r")
    
    boardList = originalFile.readlines()
    #Removing Commas and white space
    for i in range(len(boardList)):

        boardList[i] = boardList[i].split(",")
        boardList[i][8] = boardList[i][8].strip()
        #adding each object to new list as int
    for i in range(len(boardList)):
        for j in range(len(boardList[i])):
            boardList[i][j] = int(boardList[i][j])
    return(boardList)

# ✔solvePuzzle()   this is the recursive function that solves the sodoku
#                 puzzle for other parts of the program. Creates a list of
#                 numbers to try for each space. Places first number in, checks
#                 if number is valid in the Row, Column, and 3x3 Box. If it is
#                 recursive case traverses to next space. If it is not tries
#                 next number. Once all 9 numbers are exhausted it goes back a
#                 space and tries next number.
# Input:          boardList; the list that contains board data
#                 rowNumber; the row number for traversing
#                 colNumber; the column number for traversing
# Output:         solvedBoardList; the list containing the data for the solved
#                 puzzle.
def solvePuzzle(rowNum, colNum, boardList):
    # End of row? Next Row
    if colNum == END_OF_ROW:
        colNum = 0
        rowNum += 1
    # Finished the board with no errors (Base Case)
    if rowNum == END_OF_BOARD:
        return True
    #Space is full. (Recursive Case)
    if boardList[rowNum][colNum] != EMPTY_SPACE:
        if (solvePuzzle(rowNum, colNum + 1, boardList) == True):
            return True
    #Space is empty
    else:
        #Try numbers 1-9
        for i in range(1, 10):
            #If Valid Play
            if (checkSpot(rowNum, colNum, i, boardList) == True):
                boardList[rowNum][colNum] = i
                # Next spot (Recursive Case)
                if (solvePuzzle(rowNum, colNum + 1, boardList) == True):
                    
                    return True
                # Reset the space and go back
                else:
                    boardList[rowNum][colNum] = EMPTY_SPACE
    # If NOTHING WORKS go back to last call (Base Case)
    return False







# ✔numberInRow()    Checks the row of the puzzle to see if it already contains
#                 the number being tried.
# Input:          rowNumber; the number of the row being checked
#                 num; the number the row is being checked for
#                 boardList; copy of the board list
# Output:         isInRow; Boolean to state if number exists already
def numberInRow(rowNumber, num, boardList):

    if (num in boardList[rowNumber]):
        return True
    elif (num not in boardList[rowNumber]):
        return False



# ✔numberInCol()    Checks the column of the puzzle to see if it already
#                 contains
#                 the number being tried.
# Input:          colNumber; the number or the column being checked
#                 num; the number the column is being checked for
#                 boardList; copy of the board list
# Output:         isInCol; Boolean to state if number exists already
def numberInCol(colNumber, num, boardList):
    containsNumber = False
    # Iterates through row with same column
    for i in range(len(boardList)):
        if (boardList[i][colNumber] == num):
            containsNumber = True
    if containsNumber == True:
        return True
    elif containsNumber == False:
        return False

# ✔numberInBox()    Checks the box of the puzzle to see if it already contains
#                 the number being tried.
# Input:          rowNumber; the number of the row of position
#                 colNumber; the number of the column of position
#                 num; the number the box is being checked for
#                 boardList; copy of the board list
# Output:         isInBox; Boolean to state if number exists already
def numberInBox(rowNumber, colNumber, num, boardList):
    containsNumber = False
    # moving to beginning row of Nonet
    if (rowNumber <= NONET_ONE_MAX):
        rowNumber = NONET_ONE_MIN
    elif (rowNumber <= NONET_TWO_MAX):
        rowNumber = NONET_TWO_MIN
    elif (rowNumber <= NONET_THREE_MAX):
        rowNumber = NONET_THREE_MIN
    # moving to beginning column of nonet
    if (colNumber <= NONET_ONE_MAX):
        colNumber = NONET_ONE_MIN
    elif (colNumber <= NONET_TWO_MAX):
        colNumber = NONET_TWO_MIN
    elif (colNumber <= NONET_THREE_MAX): 
        colNumber = NONET_THREE_MIN
    # Traverses the Nonet space by space looking for the number (BOOLEAN FLAG)
    for i in range(NONET_RANGE):
        for j in range(NONET_RANGE):
            if (boardList[rowNumber + i][colNumber + j] == num):
                containsNumber = True
    if containsNumber == True:
        return True
    elif containsNumber == False:
        return False
# ✔checkSpot()     Checks if the number can be used in the spot specified
#                 using the numberInRow(), numberInColumn(), and numberInBox()
#                 functions.
# Input:          rowNumber; number of the row
#                 colNumber; number of the column
#                 checkedNumber; number being checked.
# Output:         spotValid; boolean to say if number is valid in the spot     
def checkSpot(rowNumber, colNumber, num, boardList):
    spotValid = False
    #checks all 3 Sudoku rule conditions
    if ((numberInRow(rowNumber, num, boardList) == False) and 
    (numberInCol(colNumber, num, boardList) == False) and 
    (numberInBox(rowNumber, colNumber, num, boardList) == False)):
        spotValid = True
    return spotValid




# ✔checkPuzzle()   Iterates through the puzzle and uses the
#                 "numberInRow()", "numberInColumn", "numberInBox"
#                 to check if all of the numbers in the puzzle are correct.
# Input:          boardList; the list of the board data
#                 solvedBoard; list of the solved board data
# Output:         isCorrect: Boolean that tells the program if the board
#                 is correctly done.
def checkPuzzle(boardList, solvedBoard):
    puzzleCorrect = True
    # If the board is the same as "solvedBoard" its finished
    for i in range(len(boardList)):
        for j in range(len(boardList[i])):
            if (boardList[i][j] != solvedBoard[i][j]):
                puzzleCorrect = False
    return puzzleCorrect
# ✔isBoardFull()    Iterates through the Sudoku board and checks for empty
#                   spaces. Returns the Boolean to state whether the board
#                   is full or not.
# Input:            boardList; the list of the board to check for spots
# Output:           boardFull; the boolean stating whether the board is full
#                   or not.
def isBoardFull(boardList):
    boardFull = True
    #Iterates through board looking for "0" (BOOLEAN FLAG)
    for i in range(len(boardList)):
        for j in range(len(boardList[i])):
            if boardList[i][j] == EMPTY_SPACE:
                boardFull = False
    return boardFull





def main():
    # initialize variables
    undoList = []
    userList = []
    correctionChecker = True
    keepPlaying = True
    # create Board list and solve the Board
    fileName = input("Enter the filename of the Sudoku Puzzle: ")
    # copy for the solver
    boardList = createBoardList(fileName)
    solvedBoard = boardList
    # copy for user
    boardList = createBoardList(fileName)
    # solve board
    solvePuzzle(BEGIN_BOARD, BEGIN_BOARD, solvedBoard)

    prettyPrint(boardList)

    # Solve or Play the Puzzle
    displayMenu(SOLVE_OR_PLAY)
    userChoice = getUserChoice(SOLVE_OR_PLAY)

    # Solve
    if (userChoice == SOLVE_OR_PLAY[0][0].lower()):
        prettyPrint(solvedBoard)
        print("This is the solved puzzle! Have a nice day!!!")
    # Play
    elif (userChoice == SOLVE_OR_PLAY[1][0].lower()):
        # Correction Checker Question
        displayMenu(CORRECTION_CHECKER)
        userChoice = getUserChoice(CORRECTION_CHECKER)
        # If Correction Checker ON
        if (userChoice == CORRECTION_CHECKER[0][0].lower()):
            correctionChecker = True
        # If Correction Checker OFF
        elif (userChoice == CORRECTION_CHECKER[1][0].lower()):
            correctionChecker = False
        
        # Turn Decision Loop (play, undo, save, quit)
        while (isBoardFull(boardList) == False) and (keepPlaying == True):
            prettyPrint(boardList)
            displayMenu(ACTION_CHOICES)
            userChoice = getUserChoice(ACTION_CHOICES)
            # Play
            if (userChoice == ACTION_CHOICES[0][0].lower()):
                # If checking for Correct
                if correctionChecker == True:
                    correctNumber = False

                    # outputs [row, column, number]
                    userList = getUserNumber(boardList)
                    if (userList != False):
                        if (solvedBoard[userList[0]][userList[1]] !=\
                         userList[2]):
                            print("This number is not the correct answer for"\
                            " this location, please try again.")
                        else:
                            #add to board
                            boardList[userList[0]][userList[1]] = userList[2]
                            #add to undo list
                            undoList.append(userList)
                            correctNumber = True

                # If not checking for Correct
                elif correctionChecker == False:
                    userList = getUserNumber(boardList)

                    if (userList != False):
                        #add to board
                        boardList[userList[0]][userList[1]] = userList[2]
                        #add to undo list
                        undoList.append(userList)
                           
            # Undo
            elif (userChoice == ACTION_CHOICES[1][0].lower()):
                if (len(undoList) == 0):
                    print("There are no moves to undo at this time.")
                else:
                    # use last item in undoList to undo last move
                    boardList[undoList[len(undoList) - 1][0]]\
                    [undoList[len(undoList) - 1][1]] = EMPTY_SPACE

                    #Displays the number removed and the location.
                    print("Removed the ("\
                     + str(undoList[len(undoList) - 1][2])
                     + ") from the space (" + \
                     str((undoList[len(undoList) - 1][0]) + 1)\
                      + " , " + str((undoList[len(undoList) - 1][1]) + 1) +\
                       ").")

                    undoList.remove(undoList[len(undoList) - 1])
            
            # Save
            elif (userChoice == ACTION_CHOICES[2][0].lower()):
                saveFile = input("Enter the filename you want to save to: ")
                savePuzzle(boardList, saveFile)
                print("Saved the Puzzle to " + saveFile + ".")
            
            # Quit
            elif (userChoice == ACTION_CHOICES[3][0].lower()):
                keepPlaying = False
                print("Good Bye! Here is the final board: ")
                prettyPrint(boardList)
    # Completed the Puzzle
    if (isBoardFull(boardList) == True):
        prettyPrint(boardList)
        print("Congratulations! You completed the puzzle Successfully.")
        
        




main()