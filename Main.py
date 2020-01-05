# TicTacToe AI benchmarking program to determine the performance of different AI algorithms playing the game.
# Performance of an algorithm (the agent) is measured by a combination of win rate and computation time against a benchmark algorithm.
# TicTacToe framework from https://inventwithpython.com/chapter10.html
# Minimax + a/b code from https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/
import random
import time


def drawBoard(board):
    # This function prints out the board that it was passed.
    # "board" is a list of 10 strings representing the board (ignore index 0)
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('-----------')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('-----------')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print(' ')


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


def evaluate(board, playerLetter):
    if playerLetter == 'X':
        opponentLetter = 'O'
    else:
        opponentLetter = 'X'

    if isWinner(board, opponentLetter):
        return -10
    if isWinner(board, playerLetter):
        return 10
    else:
        return 0


def minimax(board, depth, isMaximizingPlayer):
    score = evaluate(board, agentLetter)

    if score == 10 or score == -10:
        return score

    if isBoardFull(board):
        return 0

    if isMaximizingPlayer:
        bestVal = -100
        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, agentLetter, i)
                value = minimax(copy, depth+1, False) - depth
                bestVal = max(bestVal, value)
        return bestVal

    else:
        bestVal = 100
        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, benchmarkLetter, i)
                value = minimax(copy, depth+1, True) + depth
                bestVal = min(bestVal, value)
        return bestVal


def findBestMove(board):
    bestMove = 0
    bestMoveValue = -100
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, agentLetter, i)
            moveValue = minimax(copy, 0, False)
            if moveValue > bestMoveValue:
                bestMoveValue = moveValue
                bestMove = i

    return bestMove


def findBestBenchmarkMove(board):
    bestMove = 0
    bestMoveValue = -100
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, benchmarkLetter, i)
            moveValue = minimaxBenchmark(copy, 0, False, -100, 100)
            if moveValue > bestMoveValue:
                bestMoveValue = moveValue
                bestMove = i

    return bestMove


def getAgentMove(board):
    return findBestMove(board)


def getBenchmarkMove(board):
    return findBestBenchmarkMove(board)


def minimaxBenchmark(board, depth, isMaximizingPlayer, alpha, beta):
    score = evaluate(board, benchmarkLetter)

    if score == 10 or score == -10:
        return score

    if isBoardFull(board):
        return 0

    if isMaximizingPlayer:
        bestVal = -100
        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, benchmarkLetter, i)
                value = minimaxBenchmark(copy, depth+1, False, alpha, beta) - depth
                bestVal = max(bestVal, value)
                alpha = max(alpha, bestVal)
                if beta <= alpha:
                    break
        return bestVal

    else:
        bestVal = 100
        for i in range(1, 10):
            copy = getBoardCopy(board)
            if isSpaceFree(copy, i):
                makeMove(copy, agentLetter, i)
                value = minimaxBenchmark(copy, depth+1, True, alpha, beta) + depth
                bestVal = min(bestVal, value)
                beta = min(beta, bestVal)
                if beta <= alpha:
                    break
        return bestVal


def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


print('Welcome to Tic Tac Toe!')
agentScore = 0
benchmarkScore = 0
avgAgentTime = 0
avgBenchmarkTime = 0


#while True:
for j in range(1, 7):
    # Reset
    agentTime = 0
    benchmarkTime = 0
    # Reset the board
    theBoard = [' '] * 10
    agentLetter, benchmarkLetter = inputAgentLetter()
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'agent':
            # Agent’s turn.
            #drawBoard(theBoard)
            agent_start_time = time.time()
            move = getAgentMove(theBoard)
            agentTime += (time.time() - agent_start_time)
            makeMove(theBoard, agentLetter, move)

            if isWinner(theBoard, agentLetter):
                drawBoard(theBoard)
                print('Hooray! You have won the game!')
                agentScore += 1
                avgAgentTime += agentTime / 6
                avgBenchmarkTime += benchmarkTime / 6
                break
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    avgAgentTime += agentTime / 6
                    avgBenchmarkTime += benchmarkTime / 6
                    break
                else:
                    turn = 'benchmark'

        else:
            # Benchmark’s turn.
            benchmark_start_time = time.time()
            move = getBenchmarkMove(theBoard)
            benchmarkTime += (time.time() - benchmark_start_time)
            makeMove(theBoard, benchmarkLetter, move)
            if isWinner(theBoard, benchmarkLetter):
                drawBoard(theBoard)
                print('The benchmark has beaten you! You lose.')
                benchmarkScore += 1
                gameIsPlaying = False
                avgAgentTime += agentTime / 6
                avgBenchmarkTime += benchmarkTime / 6
                break
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie!')
                    avgAgentTime += agentTime / 6
                    avgBenchmarkTime += benchmarkTime / 6
                    break
                else:
                    turn = 'agent'
print("agent winrate is " + str(agentScore) + " for, " + str(benchmarkScore) + " against, in 6 games")
print("average benchmark computation time is " + str(avgBenchmarkTime))
print("average agent computation time is " + str(avgAgentTime))