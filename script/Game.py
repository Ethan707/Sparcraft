from Player_Random import RandomPlayer
from Player_AttackClosest import AttackClosest
from Player_AttackWeakest import AttackWeakest
from Player_Kiter_NOKDPS import Kiter_NOKDPS
from Player_NOKDPS import NOKDPS
from subprocess import Popen, PIPE
from GameState import GameState, Unit
SPARCRAFT = '../SparCraft'

PLAYER_ONE = 0
PLAYER_TWO = 1


def processMessage(process: Popen, split=' ') -> list:
    '''
    @description: convert bytes into string and split it into list
    @param {Popen} process: the process of sparcraft
    @param {string} split: the split flag
    @return {list}: the list of the string

    '''
    return process.stdout.readline().decode('utf-8').replace('\n', '').replace('\r', '').split(split)


def processGameState(process: Popen, game: GameState) -> None:
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
                position = [int(message[4]), int(message[5])]
                range = int(message[6])
                damage = int(message[7])
                dpf = float(message[8])
                # set up the unit
                unit = Unit(position, hp, range, damage, dpf)
                # add unit to game state

                if player == game.player_id:
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


def returnMoves(process: Popen, decision: list) -> None:
    '''
    @description: return the move string to sparcraft
    @param {Popen} process: the process of sparcraft
    @param {list} decision: the move list (int)
    @return {*}
    '''

    moveString = ' '.join(str(i) for i in decision)+'\n'
    process.stdin.write(str.encode(moveString))
    process.stdin.flush()


if __name__ == '__main__':
    # open Sparcraft as subprocess
    experiment_file = '../test_exp.txt'
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
    # player = RandomPlayer()

    playerZero = NOKDPS(0)
    playerOne = AttackWeakest(1)

    for i in range(num_exp):
        isRoundEnd = False
        while not isRoundEnd:
            # three occasions:
            # 1.gamestate infomation
            # 2.win
            # 3.draw
            message = processMessage(process)
            if message[0] == "Begin":
                # the game is still in progressing, we need to keep it
                player_message = processMessage(process)
                assert player_message[0] == "PlayerID"
                game.player_id = int(player_message[1])
                processGameState(process, game)
                if game.player_id == 0:
                    decision = playerZero.generate(game)
                else:
                    decision = playerOne.generate(game)
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
            else:
                print("Error: ", ' '.join(message))
                raise Exception
            game.clear()

    # result of experiment
    print("Player 0:", winner[0], "\nPlayer 1:", winner[1], "\nDraw:", winner[2])
