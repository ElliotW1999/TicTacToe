# TicTacToe AI benchmarking program to determine the performance of different AI algorithms playing the game.
# Performance of an algorithm (the agent) is measured by a combination of win rate and computation time against a benchmark algorithm.
# TicTacToe framework from https://inventwithpython.com/chapter10.html
import random


def drawBoard(board):
    # This function prints out the board that it was passed.
    # "board" is a list of 10 strings representing the board (ignore index 0)
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('-----------')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-----------')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])


def inputAgentLetter():
    # Sets the agents letter to X.
    # Returns a list with the agent’s letter as the first item, and the benchmark's letter as the second.
    return ['X', 'O']


def whoGoesFirst():
    # Randomly choose the agent who goes first.
    if random.randint(0, 1) == 0:
        return 'benchmark'
    else:
        return 'agent'


def playAgain():
    # This function returns True if the agent wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def makeMove(board, letter, move):
    board[move] = letter


def isWinner(bo, le):
    # Given a board and a agent’s letter, this function returns True if that agent has won.
    # We use bo instead of board and le instead of letter so we don’t have to type as much.
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or  # across the top
            (bo[4] == le and bo[5] == le and bo[6] == le) or  # across the middle
            (bo[1] == le and bo[2] == le and bo[3] == le) or  # across the bottom
            (bo[7] == le and bo[4] == le and bo[1] == le) or  # down the left side
            (bo[8] == le and bo[5] == le and bo[2] == le) or  # down the middle
            (bo[9] == le and bo[6] == le and bo[3] == le) or  # down the right side
            (bo[7] == le and bo[5] == le and bo[3] == le) or  # diagonal
            (bo[9] == le and bo[5] == le and bo[1] == le))  # diagonal


def getBoardCopy(board):
    # Make a duplicate of the board list and return it the duplicate.
    dupeBoard = []

    for i in board:
        dupeBoard.append(i)
    return dupeBoard


def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '


def evaluate(board):
    if isWinner(board, benchmarkLetter):
        return -10
    if isWinner(board, agentLetter):
        return 10
    else:
        return 0


def minimax(board, depth, isMaximizingPlayer):
    if isBoardFull(board):
        return evaluate(board)

    if isMaximizingPlayer:
        bestVal = -100
        for i in range(1, 10):
            value = minimax(board, depth+1, False)
            bestVal = max(bestVal, value)
        return bestVal

    else:
        bestVal = 100
        for i in range(1, 10):
            value = minimax(board, depth+1, True)
            bestVal = min(bestVal, value)
        return bestVal


def findBestMove(board):
    bestMove = 0
    bestMoveValue = -100
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, benchmarkLetter, i)
            moveValue = minimax(copy, 0, False)
            if moveValue > bestMoveValue:
                bestMoveValue = moveValue
                bestMove = i

    return bestMove


def getAgentMove(board):
    # Minimax: evaluate each possible
    return findBestMove(board)


def chooseRandomMoveFromList(board, movesList):
    # Returns a valid move from the passed list on the passed board.
    # Returns None if there is no valid move.
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None


def getBenchmarkMove(board, benchmarkLetter):
    # Given a board and the benchmark's letter, determine where to move and return that move.
    agentLetter = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, benchmarkLetter, i)
            if isWinner(copy, benchmarkLetter):
                return i

    # Check if the agent could win on their next move, and block them.
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, agentLetter, i)
            if isWinner(copy, agentLetter):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move is not None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])


def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


print('Welcome to Tic Tac Toe!')

while True:
    # Reset the board
    theBoard = [' '] * 10
    agentLetter, benchmarkLetter = inputAgentLetter()
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'agent':
            # Agent’s turn.
            drawBoard(theBoard)
            move = getAgentMove(theBoard)
            makeMove(theBoard, agentLetter, move)

            if isWinner(theBoard, agentLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'benchmark'

        else:
            # Benchmark’s turn.
            move = getBenchmarkMove(theBoard, benchmarkLetter)
            makeMove(theBoard, benchmarkLetter, move)
            if isWinner(theBoard, benchmarkLetter):
                drawBoard(theBoard)
                print('The benchmark has beaten you! You lose.')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    break
                else:
                    turn = 'agent'

    if not playAgain():
        break
