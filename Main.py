# TicTacToe AI benchmarking program to determine the performance of different AI algorithms playing the game.
# Performance of an algorithm (the agent) is measured by a combination of win rate and computation time against a benchmark algorithm.
# TicTacToe framework from https://inventwithpython.com/chapter10.html
# Minimax + a/b pseudocode from https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/
import random
import time


class TicTacToe:
    theBoard = []
    turn = 0

    def __init__(self):
        self.theBoard = [' '] * 10
        self.turn = self.whoGoesFirst()

    def whoGoesFirst(self):
        # Randomly choose the agent who goes first.
        if random.randint(0, 1) == 0:
            return 'benchmark'
        else:
            return 'agent'

    def isBoardFull(self):
        # Return True if every space on the board has been taken. Otherwise return False.
        for i in range(1, 10):
            if self.isSpaceFree(i):
                return False
        return True

    def drawBoard(self):
        # This function prints out the board that it was passed.
        # "board" is a list of 10 strings representing the board (ignore index 0)
        print(' ' + self.theBoard[7] + ' | ' + self.theBoard[8] + ' | ' + self.theBoard[9])
        print('-----------')
        print(' ' + self.theBoard[4] + ' | ' + self.theBoard[5] + ' | ' + self.theBoard[6])
        print('-----------')
        print(' ' + self.theBoard[1] + ' | ' + self.theBoard[2] + ' | ' + self.theBoard[3])
        print(' ')

    def makeMove(self, letter, move):
        self.theBoard[move] = letter

    def isWinner(self, le):
        # Given a board and a agent’s letter, this function returns True if that agent has won.
        # We use bo instead of board and le instead of letter so we don’t have to type as much.
        return ((self.theBoard[7] == le and self.theBoard[8] == le and self.theBoard[9] == le) or  # across the top
                (self.theBoard[4] == le and self.theBoard[5] == le and self.theBoard[6] == le) or  # across the middle
                (self.theBoard[1] == le and self.theBoard[2] == le and self.theBoard[3] == le) or  # across the bottom
                (self.theBoard[7] == le and self.theBoard[4] == le and self.theBoard[1] == le) or  # down the left side
                (self.theBoard[8] == le and self.theBoard[5] == le and self.theBoard[2] == le) or  # down the middle
                (self.theBoard[9] == le and self.theBoard[6] == le and self.theBoard[3] == le) or  # down the right side
                (self.theBoard[7] == le and self.theBoard[5] == le and self.theBoard[3] == le) or  # diagonal
                (self.theBoard[9] == le and self.theBoard[5] == le and self.theBoard[1] == le))  # diagonal

    def getBoardCopy(self):
        # Make a duplicate of the board list and return it the duplicate.
        dupeBoard = []

        for i in self.theBoard:
            dupeBoard.append(i)
        return dupeBoard

    def isSpaceFree(self, move):
        # Return true if the passed move is free on the passed board.
        return self.theBoard[move] == ' '

    def undoMove(self, move):
        # Return true if the passed move is free on the passed board.
        self.theBoard[move] = ' '

    def evaluate(self, playerLetter):
        if playerLetter == 'X':
            opponentLetter = 'O'
        else:
            opponentLetter = 'X'

        if self.isWinner(opponentLetter):
            return -100
        if self.isWinner(playerLetter):
            return 100
        else:
            return 0
# End class TicTacToe


class Player:
    letter = 'X'

    def getPlayerMove(self):
        # Let the player type in his move.
        move = ' '
        while move not in '1 2 3 4 5 6 7 8 9'.split() or not gameInstance.isSpaceFree(int(move)):
            print('What is your next move? (1-9)')
            move = input()
        return int(move)


class AdversaryAI:
    letter = 'O'

    def findBestMove(self):
        bestMove = 0
        bestMoveValue = -100
        for i in range(1, 10):
            if gameInstance.isSpaceFree(i):
                gameInstance.makeMove(self.letter, i)
                moveValue = self.minimax(0, False, -100, 100)
                gameInstance.undoMove(i)
                if moveValue > bestMoveValue:
                    bestMoveValue = moveValue
                    bestMove = i
        return bestMove

    def getMove(self):
        return self.findBestMove()

    def minimax(self, depth, isMaximizingPlayer, alpha, beta):
        score = gameInstance.evaluate(self.letter)

        if score == 100 or score == -100:
            return score

        if gameInstance.isBoardFull():
            return 0

        if isMaximizingPlayer:
            bestVal = -100
            for i in range(1, 10):
                if gameInstance.isSpaceFree(i):
                    gameInstance.makeMove(self.letter, i)
                    value = self.minimax(depth + 1, False, alpha, beta)
                    bestVal = max(bestVal, value)
                    alpha = max(alpha, bestVal)
                    gameInstance.undoMove(i)
                    if beta <= alpha:
                        break
            return bestVal

        else:
            bestVal = 100
            for i in range(1, 10):
                if gameInstance.isSpaceFree(i):
                    gameInstance.makeMove(agent.letter, i)
                    value = self.minimax(depth + 1, True, alpha, beta)
                    bestVal = min(bestVal, value)
                    beta = min(beta, bestVal)
                    gameInstance.undoMove(i)
                    if beta <= alpha:
                        break
            return bestVal
# end class AdversaryAI


# Agent uses TD(0) algorithm
# Pseudocode is as follows: Each ply is a different state, where the state is the board
# Create a Q-Table, mapping values to each state
# For each state:
#   If an agent's turn, take a move according to policy
#       Use epsilon to determine policy
#   Update value of V(St) according to value of new position using:
#   V(St) = V(St) + a(Rt+1 + y(V(St+1)) - V(St)), where Rt+1 = -1
class Agent:
    alpha = .08             # Learning rate
    gamma = 0.8             # Discount factor
    epsilon = 0.2          # Exploration/ exploitation variable
    letter = 'X'
    stateValues = {}        # Dictionary where each key is a state and each value is an int
    agentMovesUpdate = []
    currentState = 0

    def __init__(self, file, isTest):
        movesRows = open(file, "r").read().split("\n")  # List of strings
        self.agentMovesUpdate = open(file, "w")                 # Used to rewrite learned values after each episode (game)
        #self.epsilon = .99**episode
        #if isTest:
        #    self.epsilon = 0
        self.currentState = 'init'
        self.stateValues['init'] = 0
        movesRows.pop()
        for row in movesRows:
            moves = row.split(".")
            self.stateValues[moves[0]] = int(moves[1])

    def getMove(self):
        possibleActions = []
        actionValues = {}   # Dictionary of actions and their values
        # For each available action
        for i in range(1, 10):
            if gameInstance.isSpaceFree(i):
                possibleActions.append(i)

        # Choose a random action, or best action, based on epsilon
        if random.random() < self.epsilon:
            # return random action
            return random.choice(possibleActions)
        else:
            # return best action
            for action in possibleActions:
                gameInstance.makeMove(self.letter, action)
                actionValues[action] = self.getStateValue()
                gameInstance.undoMove(action)
            return max(actionValues, key=actionValues.get)

    def saveStates(self):
        """ Update states file and closes. To be called at end of episode """
        for state in self.stateValues:
            self.agentMovesUpdate.write(state + "." + str(self.stateValues[state]) + "\n")
        self.agentMovesUpdate.close()

    def updateStates(self, isTerminal):
        """ Updates previous states value. To be called after a change in state.
          V(St-1) = V(St-1) + a(Rt + y(V(St)) - V(St-1)), where Rt = 0. Also updates V(St-1) to V(St)"""

        newStateValue = self.getStateValue()   # adds V(St) to list of states
        TDtarget = (0 + self.gamma*newStateValue)
        delta = (TDtarget - self.stateValues[self.currentState])
        self.stateValues[self.currentState] += self.alpha * delta
        self.currentState = (''.join(gameInstance.theBoard))
        if isTerminal:
            self.stateValues[self.currentState] = gameInstance.evaluate(self.letter)

    def getStateValue(self):
        """ Returns the value given state key
        Otherwise adds state to state list if it does not exist, initialized at value 1."""
        if (''.join(gameInstance.theBoard)) in self.stateValues:
            return self.stateValues[(''.join(gameInstance.theBoard))]
        else:
            self.stateValues[(''.join(gameInstance.theBoard))] = 1
            return self.stateValues[(''.join(gameInstance.theBoard))]
# end class Agent


print('Welcome to Tic Tac Toe!')
stateFile = "stateFile.txt"     # text file contains 2 columns: State, e.g.: XOXOXOXOX, and Value, e.g.: -3
agentScore = 0
benchmarkScore = 0
benchmark = AdversaryAI()
episode = 1
trainingEpisodes = 100
training = True
for y in range(1, 51):
    avgAgentTime = 0
    avgBenchmarkTime = 0
    for x in range(1, trainingEpisodes):
        # Reset times
        agentTime = 0
        benchmarkTime = 0
        episode += 1
        # Reset the board
        gameInstance = TicTacToe()
        agent = Agent(stateFile, episode)
        gameIsPlaying = True

        while gameIsPlaying:
            if gameInstance.turn == 'agent':
                # Agent’s turn.
                move = agent.getMove()
                gameInstance.makeMove(agent.letter, move)
                if gameInstance.isWinner(agent.letter):
                    #print('Hooray! You have won the game!')
                    agentScore += 1
                    agent.updateStates(True)
                    agent.saveStates()
                    break
                else:
                    if gameInstance.isBoardFull():
                        #gameInstance.drawBoard()
                        #print('The game is a tie!')
                        agent.updateStates(True)
                        agent.saveStates()
                        break
                    else:
                        gameInstance.turn = 'benchmark'
                        agent.updateStates(False)

            else:
                # Benchmark’s turn.
                move = benchmark.getMove()
                gameInstance.makeMove(benchmark.letter, move)
                if gameInstance.isWinner(benchmark.letter):
                    #gameInstance.drawBoard()
                    #print('The benchmark has beaten you! You lose.')
                    gameIsPlaying = False
                    agent.updateStates(True)
                    agent.saveStates()
                    break
                else:
                    if gameInstance.isBoardFull():
                        #gameInstance.drawBoard()
                        #print('The game is a tie!')
                        agent.updateStates(True)
                        agent.saveStates()
                        break
                    else:
                        gameInstance.turn = 'agent'


    for j in range(1, trainingEpisodes):
        # Reset times
        agentTime = 0
        benchmarkTime = 0
        agent_start_time = time.time()
        agent = Agent(stateFile, episode)
        agent.epsilon = 0
        agentTime += (time.time() - agent_start_time)
        episode += 1
        # Reset the board
        gameInstance = TicTacToe()
        gameIsPlaying = True

        while gameIsPlaying:
            if gameInstance.turn == 'agent':
                # Agent’s turn.
                agent_start_time = time.time()
                move = agent.getMove()
                agentTime += (time.time() - agent_start_time)
                gameInstance.makeMove(agent.letter, move)
                if gameInstance.isWinner(agent.letter):
                    #gameInstance.drawBoard()
                    #print('Hooray! You have won the game!')
                    agentScore += 1
                    agent.saveStates()
                    avgAgentTime += agentTime / trainingEpisodes
                    avgBenchmarkTime += benchmarkTime / trainingEpisodes
                    break
                else:
                    if gameInstance.isBoardFull():
                        #gameInstance.drawBoard()
                       # print('The game is a tie!')
                        avgAgentTime += agentTime / trainingEpisodes
                        avgBenchmarkTime += benchmarkTime / trainingEpisodes
                        agent.saveStates()
                        break
                    else:
                        gameInstance.turn = 'benchmark'

            else:
                # Benchmark’s turn.
                benchmark_start_time = time.time()
                move = benchmark.getMove()
                benchmarkTime += (time.time() - benchmark_start_time)
                gameInstance.makeMove(benchmark.letter, move)
                if gameInstance.isWinner(benchmark.letter):
                    #gameInstance.drawBoard()
                    #print('The benchmark has beaten you! You lose.')
                    benchmarkScore += 1
                    gameIsPlaying = False
                    avgAgentTime += agentTime / trainingEpisodes
                    avgBenchmarkTime += benchmarkTime / trainingEpisodes
                    agent.saveStates()
                    break
                else:
                    if gameInstance.isBoardFull():
                        #gameInstance.drawBoard()
                        #print('The game is a tie!')
                        avgAgentTime += agentTime / trainingEpisodes
                        avgBenchmarkTime += benchmarkTime / trainingEpisodes
                        agent.saveStates()
                        break
                    else:
                        gameInstance.turn = 'agent'

    print("agent winrate is " + str(agentScore) + " wins, " + str(benchmarkScore) + " losses, " +
                                                                    str(trainingEpisodes-agentScore-benchmarkScore) + " draws")
    print("average benchmark computation time is " + str(avgBenchmarkTime))
    print("average agent computation time is " + str(avgAgentTime))
    print("number of states saved: " + str(len(agent.stateValues)))
    agentScore = 0
    benchmarkScore = 0
    if trainingEpisodes-agentScore-benchmarkScore == 100:
        training = False
