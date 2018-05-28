import ctypes as c


class ShotPos(c.Structure):
    _fields_ = [
        ('x', c.c_float),
        ('y', c.c_float),
        ('angle', c.c_bool)
    ]



class ShotVec(c.Structure):
    _fields_ = [
        ('x', c.c_float),
        ('y', c.c_float),
        ('angle', c.c_bool)
    ]


class GameState(c.Structure):
    _fields_ = [
        ('shot_num', c.c_int),

        ('curr_end', c.c_int),
        ('last_end', c.c_int),
        ('_score', c.c_int * 10),
        ('yell_to_move', c.c_bool),

        ('_body', (c.c_float * 2) * 16) # [16][2]
    ]

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        for i, v in enumerate(value):
            self._score[i] = v

    @property
    def body(self):
        return self._body
    @body.setter
    def body(self, value):
        for i, row in enumerate(value):
            for j, item in enumerate(row):
                self.body[i][j] = item



dll = c.WinDLL('./dll/CurlingSimulator')
#dll = c.WinDLL('C:\Users\sun\PycharmProjects\lab-curling_v.0.1/dll/CurlingSimulator')

# create_shot
create_shot = dll['CreateShot']
create_shot.argtypes = (ShotPos, c.POINTER(ShotVec))
create_shot.restype = c.c_bool

# get_score
get_score = dll['GetScore']
get_score.argtypes = (c.POINTER(GameState),)
get_score.restype = c.c_int

# simulation
simulation = dll['Simulation']
simulation.argtypes = (c.POINTER(GameState), ShotVec, c.c_float,
                       c.POINTER(ShotVec), c.c_int)
simulation.restype = c.c_int


def _function_test():
    # --------- create_shot --------------
    a = ShotPos(2.3, 4.8, False)
    b = ShotVec(0, 0, 0)
    # input is not pointer
    create_shot(a, b)
    print(b.x, b.y, b.angle)

    # --------- get_score --------------
    s = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    body =[[0.0, 0.0], [2.690301, 5.398643], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [4.203744, 3.752828],
           [3.073219, 5.037444], [2.648806, 4.760893], [2.395548, 5.828968], [0.0, 0.0], [2.280121, 6.513048],
           [0.0, 0.0], [2.249753, 6.814593], [2.122123, 4.99945], [2.131128, 8.505591], [0.0, 0.0]]

    # old style

    # arr = (c.c_int * 10)(*s)
    # cbody = ((c.c_float * 2) * 16)()
    # for i, row in enumerate(body):
    #     for j, item in enumerate(row):
    #         cbody[i][j] = item
    # game_state = GameState(16, 1, 9, s, True, body)

    game_state = GameState()
    game_state.shot_num = 16
    game_state.curr_end = 1
    game_state.last_end = 9
    game_state.score = s
    game_state.yell_to_move = True
    game_state.body = body

    print(get_score(game_state))

    # --------- simulation --------------
    score = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    arr = (c.c_int * 10)(*score)
    cbody = ((c.c_float * 2) * 16)()
    body = [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]
    for i, row in enumerate(body):
        for j, item in enumerate(row):
            cbody[i][j] = item
    g = GameState(0, 1, 9, arr, True, cbody)
    b = ShotVec(-1.0526649951934814, -29.590171813964844, False)
    b_ = ShotVec(0, 0, 0)
    # -1 simulation until a stone stops
    simulation(g, b, 0.145, b_, -1)
    print(b.x, b.y)
    print(b_.x, b_.y)

    print(g.body[0][0], g.body[0][1], g.body[1][0], g.body[1][1])

if __name__ =='__main__':
    # _function_test()
    g = GameState()



# DLLAPI int CreateHitShot(SHOTPOS Shot, float Power, SHOTVEC *lpResShot);
# DLLAPI int CreateShot(SHOTPOS ShotPos, SHOTVEC *lpResShotVec);
# DLLAPI int SimulationEx(GAMESTATE *pGameState, SHOTVEC Shot, float RandX, float RandY, SHOTVEC *lpResShot,
# float *pLoci, int ResLociSize);
# DLLAPI int Simulation(GAMESTATE *pGameState, SHOTVEC Shot, float Rand, SHOTVEC *lpResShot, int LoopCount);
# DLLAPI int GetScore(GAMESTATE *pGameState)

# [[float(i),float(j)] for i, j in zip(a[::2], a[1::2])]