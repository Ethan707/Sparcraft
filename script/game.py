from Player_Random import RandomPlayer
from Player_AttackClosest import AttackClosest
from subprocess import Popen, PIPE
from GameState import GameState, Unit
SPARCRAFT = '../bin/SparCraft'


def processMessage(process: Popen, split=' ') -> list:
    '''
    convert bytes into string and split it into list
    '''
    return process.stdout.readline().decode('utf-8').replace('\n', '').replace('\r', '').split(split)


def processGameState(process: Popen, game: GameState):
    message = processMessage(process)

    while message[0] != "End":
        if message[0] == "Time":
            try:
                game.setTime(int(message[1]))
            except Exception as e:
                print(e)
        elif message[0] == "Unit":
            try:
                # get the infomation
                player = int(message[1])
                hp = int(message[2])
                firstTimeFree = int(message[3])
                position_x = int(message[4])
                position_y = int(message[5])
                # set up the unit
                unit = Unit()
                unit.setPosition(position_x, position_y)
                unit.setHP(hp)
                unit.setFirstTimeFree(firstTimeFree)
                # add unit to game state
                if player == 0:
                    game.addUnit(unit)
                else:
                    game.addEnemy(unit)
            except Exception as e:
                print("Error:", ' '.join(message))
                print(e)
        elif message[0] == "Move":
            try:
                unitIndex = int(message[1])
                player = int(message[2])
                moveType = int(message[3])
                moveIndex = int(message[4])
                position_x = int(message[5])
                position_y = int(message[6])

                # set up the move
                game.player_unit[unitIndex].moves.append([moveType, moveIndex, position_x, position_y])

            except Exception as e:
                print("Error:", ' '.join(message))
                print(e)
        else:
            print("Unknown:", ' '.join(message))
            raise Exception
        message = processMessage(process)
    # return game


def returnMoves(process: Popen, decision: list):
    moveString = ' '.join(str(i) for i in decision)+'\n'
    process.stdin.write(str.encode(moveString))
    process.stdin.flush()


if __name__ == '__main__':
    # open Sparcraft as subprocess
    experiment_file = '../sample_experiment/test_exp.txt'
    process = Popen([SPARCRAFT, experiment_file], stdin=PIPE, stdout=PIPE)
    message = processMessage(process)

    # Check program started
    # Start Message: "Adding 10 State(s)"
    if message[0] == 'Adding':
        print("Sub process successfully start")

    # get amount of experiment
    num_exp = int(message[1])
    winner = [0]*3  # player 0 | player 1 | draw

    game = GameState()
    player = RandomPlayer()
    player = AttackClosest()

    for i in range(num_exp):
        isRoundEnd = False
        while not isRoundEnd:
            message = processMessage(process)
            if message[0] == "Begin":
                # the game is still in progressing, we need to keep it
                processGameState(process, game)
                decision = player.generate(game)
                # print(decision)
                # Return the move to sparcraft
                returnMoves(process, decision)
            elif message[0] == "Winner":
                # the game finish and clear the game infomation
                winner[int(message[-1])] += 1
                isRoundEnd = True
                print("Winner: Player", int(message[-1]))
            elif message[0] == "Draw":
                # the game finish and clear the game infomation
                winner[-1] += 1
                isRoundEnd = True
                print("Draw")
            game.clear()
    # result of experiment
    print("Player 0:", winner[0], "\nPlayer 1:", winner[1], "\nDraw:", winner[2])
