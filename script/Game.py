from Player_Random import RandomPlayer
from Player_AttackClosest import AttackClosest
from Player_AttackWeakest import AttackWeakest
from Player_Kiter_NOKDPS import Kiter_NOKDPS
from Player_NOKDPS import NOKDPS
from subprocess import Popen, PIPE
from GameState import GameState, Unit

PLAYER_ONE = 0
PLAYER_TWO = 1

EXP_FILE = '../sample_experiment/exp.txt'
EXE_FILE = '../bin/SparCraft'
# /home/ethan/workspace/Sparcraft/bin/SparCraft


class Game:
    def __init__(self, player_0, player_1, exp_file=EXP_FILE, num_exp=10, execute_file=EXE_FILE):
        self.player_0 = player_0
        self.player_1 = player_1
        self.exp_file = exp_file
        self.num_exp = num_exp
        self.winner = [0]*3  # player 0 | player 1 | draw
        self.execute_file = execute_file
        self.process = Popen(['../bin/SparCraft', '../sample_experiment/exp.txt',
                             str(self.num_exp)], stdin=PIPE, stdout=PIPE)
        self.state = GameState()

        self.player_0.set_player_id(0)
        self.player_1.set_player_id(1)

    def processMessage(self, split=' ') -> list:
        '''
        @description: convert bytes into string and split it into list
        @param {Popen} process: the process of sparcraft
        @param {string} split: the split flag
        @return {list}: the list of the string

        '''
        return self.process.stdout.readline().decode('utf-8').replace('\n', '').replace('\r', '').split(split)

    def processGameState(self, state: GameState) -> None:
        message = self.processMessage()

        while message[0] != "End":
            if message[0] == "Time":
                try:
                    state.setTime(int(message[1]))
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

                    if player == state.player_id:
                        state.addUnit(unit)
                    else:
                        state.addEnemy(unit)
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
                    state.player_unit[unitIndex].moves.append([moveType, moveIndex, position_x, position_y])

                except Exception as e:
                    # print("Error:", ' '.join(message))
                    print(e)
            else:
                print("Unknown:", ' '.join(message))
                print(message)
                # self.process.kill()
                raise Exception
            message = self.processMessage()
        # return game

    def returnMoves(self,  decision: list) -> None:
        '''
        @description: return the move string to sparcraft
        @param {Popen} process: the process of sparcraft
        @param {list} decision: the move list (int)
        @return {*}
        '''

        moveString = ' '.join(str(i) for i in decision)+'\n'
        self.process.stdin.write(str.encode(moveString))
        self.process.stdin.flush()

    def init_experiment(self):
        message = self.processMessage()
        # Check program started
        # Start Message: numState
        assert message[0].isdigit() and int(message[0]) == self.num_exp
        # print(message[0])
        # print("SparCraft starts successfully")

    def run_experiment(self):
        self.init_experiment()
        # print(self.num_exp)
        for i in range(self.num_exp):
            # print(self.num_exp)
            end = False
            while not end:
                end = self.run_round()
                self.state.clear()

    def run_round(self):
        # three occasions:
        # 1.gamestate infomation
        # 2.win
        # 3.draw
        message = self.processMessage()
        if message[0] == "Begin":
            # the game is still in progressing, we need to keep it
            player_message = self.processMessage()
            assert player_message[0] == "PlayerID" and player_message[1].isdigit()
            self.state.player_id = int(player_message[1])
            self.processGameState(self.state)
            # print(len(self.state.player_unit))

            if self.state.player_id == 0:
                decision = self.player_0.generate(self.state)
            else:
                decision = self.player_1.generate(self.state)
            # print(decision)
            # Return the move to sparcraft
            self.returnMoves(decision)
            return False

        elif message[0] == "Winner":
            # the game finish and clear the game infomation
            self.winner[int(message[-1])] += 1
            print("Winner: Player", int(message[-1]))
            return True

        elif message[0] == "Draw":
            # the game finish and clear the game infomation
            self.winner[-1] += 1
            print("Draw")
            return True

        else:
            print("Error: ", ' '.join(message))
            self.process.kill()
            raise Exception
        return True

    def get_result(self) -> list:
        return self.winner

    def print_result(self) -> None:
        # result of experiment
        print("Player 0:", self.winner[0], "\nPlayer 1:", self.winner[1], "\nDraw:", self.winner[2])

    def clear(self):
        pass

    def kill(self):
        self.process.kill()
