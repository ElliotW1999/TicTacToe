import random
print("hello world")
print(random.random())
testFileAppend = open("testFile.txt", "a")
testFileRead = open("testFile.txt", "r")

movesDict = {}
testFileContents = testFileRead.read()
testFileRows = testFileContents.split("\n")
testFileRows.pop()
print(testFileRows)
for row in testFileRows:
 #   moves = row.split(" ")
#    movesDict[moves[0]] = moves[1]
    print(row)

#for move in movesDict:
    #print(movesDict[move])

print('Welcome to Tic Tac Toe!')
benchmark = AdversaryAI()
player = Player()
while True:
    # Reset the board
    gameInstance = TicTacToe()
    print('The ' + gameInstance.turn + ' will go first.')
    gameIsPlaying = True

    while gameIsPlaying:
        if gameInstance.turn == 'agent':
            # Agent’s turn.
            move = player.getPlayerMove()
            gameInstance.makeMove(player.letter, move)
            if gameInstance.isWinner(player.letter):
                gameInstance.drawBoard()
                print('Hooray! You have won the game!')
                break
            else:
                if gameInstance.isBoardFull():
                    gameInstance.drawBoard()
                    print('The game is a tie!')
                    break
                else:
                    gameInstance.turn = 'benchmark'

        else:
            # Benchmark’s turn.
            move = benchmark.getMove()
            gameInstance.makeMove(benchmark.letter, move)

            gameInstance.drawBoard()
            if gameInstance.isWinner(benchmark.letter):
                gameInstance.drawBoard()
                print('The benchmark has beaten you! You lose.')
                gameIsPlaying = False
                break
            else:
                if gameInstance.isBoardFull():
                    gameInstance.drawBoard()
                    print('The game is a tie!')
                    break
                else:
                    gameInstance.turn = 'agent'