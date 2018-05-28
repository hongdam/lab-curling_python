import win32file
from win32api import STD_INPUT_HANDLE, STD_OUTPUT_HANDLE
import simulator
from simulator import ShotVec, ShotPos, GameState


# -----Using ctypes kernel32-----#
# import ctypes
#
# STD_INPUT_HANDLE = ctypes.c_ulong(-10)
# STD_OUTPUT_HANDLE = ctypes.c_ulong(-11)
#
# ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
# -----Using ctypes kernel32-----#

# import Functions

# win32file.WriteFile(STD_OUTPUT_HANDLE, b"msg")
# return (err code, len(data))
# win32file.ReadFile(STD_INPUT_HANDLE, 1024)
# (0, b'GO 1 2 3\r\n') (err code, data)

# file = open("./log.txt", "w")
# file.write(cmd+"\n")
# file.flush()

EXE = True


def recv():
    err_code, cmd = win32file.ReadFile(STD_INPUT_HANDLE, 1024)
    if err_code != 0:
        print("ERROR: RECV() (code: %d)" % err_code)
        # raise SystemExit
    # \x00
    if EXE:
        cmd = cmd[:-1]
    cmd = cmd.decode("UTF-8")

    return str(cmd)


def send(msg):
    win32file.WriteFile(STD_OUTPUT_HANDLE, msg.encode())


def main():

    # ISREADY -> NEWGAME -> { POSITION -> SETSTATE -> GO -> POSITION -> SETSTATE } -> POSITION -> SCORE
    # game_state = GameState()

    while True:

        # cmd = ""
        cmd = recv()

        if "GO" in cmd:
            # GO {t1; first player's left time} {t2}
            # return BESTSHOT {x} {y} {curl, 0: counterclockwise}
            shot_pos = ShotPos(0.545, 4.44, 0)
            shot_vec = ShotVec()
            simulator.create_shot(shot_pos, shot_vec)

            send('BESTSHOT %.10f %.10f %d\n' % (shot_vec.x, shot_vec.y, shot_vec.angle))
        elif "POSITION" in cmd:
            pos = cmd.split()[1:]

            pos = [[float(x), float(y)] for x, y in zip(pos[::2], pos[1::2])]

            game_state.body = pos

        elif "SETSTATE" in cmd:
            # SETSTATE {shot_num} {curr_end} {last_end} {yell_to_move}
            state = cmd.split()[1:]
            state = [int(x) for x in state]
            game_state.shot_num = state[0]
            game_state.curr_end = state[1]
            game_state.last_end = state[2]
            game_state.yell_to_move = state[3]

        elif "SCORE" in cmd:
            score = cmd.split()
            score = int(score[1])
            game_state.score[game_state.curr_end] = score

        elif "ISREADY" in cmd:
            # ISREADY
            # return READYOK
            send("READYOK\n")

        elif "NEWGAME" in cmd:
            # NEWGAME
            game_state = GameState()

        elif "GAMEOVER" in cmd:
            # GAMEOVER {DRAW/..}
            pass

        elif "PRINT" in cmd:
            body = []
            for i, row in enumerate(game_state.body):
                body.append([])
                for item in row:
                    body[i].append(item)
            print(body)
            print(game_state.shot_num, game_state.curr_end, game_state.last_end, game_state.yell_to_move)


if __name__ == "__main__":
    main()
