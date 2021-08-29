from scripted_player import *
from subprocess import Popen, PIPE
from GameState import GameState, Unit

PLAYER_ONE = 0
PLAYER_TWO = 1

EXP_FILE = '../sample_experiment/exp.txt'
EXE_FILE = '../bin/SparCraft'


class Game:
    def __init__(self, player_0, player_1, exp_file=EXP_FILE, execute_file=EXE_FILE, num_exp=10):
        self.player_0 = player_0
        self.player_1 = player_1
        self.exp_file = exp_file
        self.num_exp = num_exp
        self.winner = [0]*3  # player 0 | player 1 | draw
        self.execute_file = execute_file
        self.state = GameState()

        self.player_0.set_player_id(0)
        self.player_1.set_player_id(1)

    def processMessage(self, process: Popen):
        try:
            message = process.stdout.readline().decode('utf-8')
            message = message.replace('\n', '').replace('\r', '')
            l = message.split(' ')
            return False, l
        except Exception as e:
            print("Error: in Reading message from SparCraft")
            print("Error:", e)
            return True, []
    # has_error, list

    def processGameState(self, process: Popen):
        has_error = False
        while not has_error:
            has_error, message = self.processMessage(process)
            if has_error:
                return True
            else:
                # check the length of the message
                try:
                    assert len(message) > 0
                except Exception as e:
                    print("Error: The length of message is 0")
                    print("Error:", e)
                    return True

                # convert the message into values
                if message[0] == "End":
                    return False
                elif message[0] == "Time":
                    try:
                        self.state.setTime(int(message[1]))
                    except Exception as e:
                        print("Error: time is not an integer")
                        print("Error:", e, "Message:", ' '.join(message))
                        return True
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

                        if player == self.state.player_id:
                            self.state.addUnit(unit)
                        else:
                            self.state.addEnemy(unit)
                    except Exception as e:
                        print("Error in processing unit:", ' '.join(message))
                        print(e)
                        return True
                elif message[0] == "Move":
                    try:
                        unitIndex = int(message[1])
                        player = int(message[2])
                        moveType = int(message[3])
                        moveIndex = int(message[4])
                        position_x = int(message[5])
                        position_y = int(message[6])
                        # set up the move
                        self.state.player_unit[unitIndex].moves.append([moveType, moveIndex, position_x, position_y])
                    except Exception as e:
                        print("Error in processing moves:", ' '.join(message))
                        print(e)
                        return True
                else:
                    print("Unknown message:", " ".join(message))
                    return True
    # has_error

    def returnMoves(self, decision: list, process: Popen):
        try:
            moveString = ' '.join(str(i) for i in decision)+'\n'
            process.stdin.write(str.encode(moveString))
            process.stdin.flush()
        except Exception as e:
            print("Return error", e)
            print(decision)

    def run_experiment(self):
        try:
            with Popen([self.execute_file, self.exp_file, str(self.num_exp)], stdin=PIPE, stdout=PIPE, stderr=PIPE) as process:
                for _ in range(self.num_exp):
                    is_finished = False
                    while not is_finished:
                        # print(_)
                        has_error, is_finished = self.run_round(process)
                        self.state = GameState()
                        if has_error:
                            raise Exception
        except Exception as e:
            print("Error in Games", e)
            return True
        return False

    def run_round(self, process):
        # three occasions:
        # 1.gamestate infomation
        # 2.win
        # 3.draw
        has_error, message = self.processMessage(process)
        if has_error:
            print("Error in message 1")
            return True, False
        if message[0] == "Begin":
            # the game is still in progressing, we need to keep it
            has_error, player_message = self.processMessage(process)

            if player_message[0] != "PlayerID" or not player_message[1].isdigit():
                has_error = True
            if has_error:
                print("Error in message 2")
                return True, False

            self.state.player_id = int(player_message[1])

            has_error = self.processGameState(process)
            if has_error:
                return True, False

            if self.state.player_id == 0:
                decision = self.player_0.generate(self.state)
            else:
                decision = self.player_1.generate(self.state)
            # Return the move to sparcraft
            self.returnMoves(decision, process)
            return False, False

        elif message[0] == "Winner":
            # the game finish and clear the game infomation
            self.winner[int(message[-1])] += 1
            print("Winner: Player", int(message[-1]))
            return False, True

        elif message[0] == "Draw":
            # the game finish and clear the game infomation
            self.winner[-1] += 1
            print("Draw")
            return False, True
        # print(message)
        return True, False

    def get_result(self) -> list:
        return self.winner

    def print_result(self) -> None:
        # result of experiment
        print("Player 0:", self.winner[0], "\nPlayer 1:", self.winner[1], "\nDraw:", self.winner[2])
