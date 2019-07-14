import numpy as np



def make_universe(
        size=100, edge_ratio=1, born=0b01100, live=0b01000, beta=1,
        init='random'
):
    class Universe:
        """Data structure for the universe"""
        pass

    uni = Universe()
    uni.size = size                 # Dimensions
    uni.edge_ratio = edge_ratio     # Ratio of long side to short
    uni.width = int(size * edge_ratio)
    uni.born = born                 # Birth rules of universe
    uni.live = live                 # Remain-alive rules
    uni.beta = beta
    if init=='random':
        uni.data = np.random.random((size, uni.width)) > 0.5
    else:
        uni.data = np.zeros((size, int(size * np.edge_ratio)), np.bool_)

    return uni

def update_universe(method, universe):
    pass

def print_array(universe):
    """
    Performs a basic print.

    :param universe:    the univese, containing the data to print
    :return:            None
    """
    temp = np.empty_like(universe.data, str)
    out = []
    transcript = {0: '.',
                  1: 'o',
                  }
    for i in range(universe.size):
        for j in range(universe.width):
            temp[i][j] = transcript[univese.data[i][j]]
        out.append(''.join(temp[i,:]))
    fin = '\n'.join(out)
    print(fin)

def ising(updates, universe):
    """
    Performs ising updates on the array.

    :param updates:  ising updates (as percentage of all positions, 0 is off)
    :param universe: the universe
    :return:        None
    """
    if updates == 0:
        return
    cost = np.zeros(3, np.float32)
    cost[1] = np.exp(-4 * universe.beta)
    cost[2] = cost[1] ** 2
    N = universe.size
    D = universe.width
    arr = universe.data.copy()
    for _ in range(int(updates * N * D)):
        a = int(np.random.random() * N)
        b = int(np.random.random() * D)
        nb = neumann_neighbors_same([a,b], universe)
        if nb - 2 <= 0 or np.random.random() < cost[nb - 2]:
            arr[a, b] = 1 - arr[a, b]
    universe.data = arr

def conway(universe):
    """
    Performs conway update on the array.

    :param universe: the universe
    :return:        None
    """
    N = dim[0]
    D = dim[1]
    arr = universe.data.copy()
    for i in range(N):
        for j in range(D):
            NB = neumann_neighbors_sum([i,j], universe)
            if arr[i][j] == 1:
                arr[i][j] == (universe.live>>NB)&1
            else:
                arr[i][j] == (universe.born>>NB)&1
    universe.data = arr

def conway_old(universe):
    """
    Performs conway update on the array.

    :param universe: the universe
    :return:        None
    """
    l = np.roll(universe.data, 1, axis=0)
    r = np.roll(universe.data, -1, axis=0)
    u = np.roll(universe.data, 1, axis=1)
    d = np.roll(universe.data, -1, axis=1)
    ul = np.roll(l, 1, axis=1)
    dl = np.roll(l, -1, axis=1)
    ur = np.roll(r, 1, axis=1)
    dr = np.roll(r, -1, axis=1)
    N = universe.size
    D = universe.width
    for i in range(N):
        for j in range(D):
            NB = l[i][j] + r[i][j] + u[i][j] + d[i][j] + ul[i][j] + ur[i][j]\
                + dl[i][j] + dr[i][j]
            if universe.data[i][j] == 1:
                universe.data[i][j] == (universe.live>>NB)&1
            else:
                universe.data[i][j] == (universe.born>>NB)&1

def neumann_neighbors_same(pos, universe):
    """
    Calculates the number of neumann neighbors that share state with the position.

    :param pos:         position to be checked
    :param universe: the universe
    :return:            neighbors
    """
    a = pos[0]
    b = pos[1]
    if universe.data[a, b]:
        return neumann_neighbors_sum(pos, universe)
    else:
        return 4 - neumann_neighbors_sum(pos, universe)

def neumann_neighbors_sum(pos, universe):
    """
    Calculated the population of the neumann neighborhood at position.

    :param pos:         position to be checked
    :param universe: the universe
    :return:            neighbors
    """
    N = universe.size
    D = universe.width
    a = pos[0]
    b = pos[1]
    if a == 0 or b == 0 or a == N-1 or b == D-1:
        l = universe.data[(a + 1) % N][b]
        r = universe.data[(a - 1 + N) % N][b]
        u = universe.data[a][(b + 1) % D]
        d = universe.data[a][(b - 1 + D) % D]
        nb = l + u + d + r
    else:
        l = universe.data[(a + 1)][b]
        r = universe.data[(a - 1)][b]
        u = universe.data[a][(b + 1)]
        d = universe.data[a][(b - 1)]
        nb = l + u + d + r
    return nb

def moore_neighbors_same(pos, universe):
    """
    Calculates the number of moore neighbors that share state with the position.

    :param pos:         position to be checked
    :param universe: the universe
    :return:            neighbors
    """
    a = pos[0]
    b = pos[1]
    if universe.data[a, b]:
        return moore_neighbors_sum(pos, universe)
    else:
        return 8 - moore_neighbors_sum(pos, universe)


def moore_neighbors_sum(pos, universe):
    """
    Calculated the population of the moore neighborhood at position.

    :param pos:         position to be checked
    :param universe: the universe
    :return:            neighbors
    """
    N = universe.size
    D = universe.width
    a = pos[0]
    b = pos[1]
    if a == 0 or b == 0 or a == N-1 or b == D-1:
        l = universe.data[(a + 1) % N][b]
        r = universe.data[(a - 1 + N) % N][b]
        ul = universe.data[(a + 1) % N][(b + 1) % D]
        ur = universe.data[(a - 1 + N) % N][(b + 1) % D]
        dl = universe.data[(a + 1) % N][(b - 1 + D) % D]
        dr = universe.data[(a - 1 + N) % N][(b - 1 + D) % D]
        u = universe.data[a][(b + 1) % D]
        d = universe.data[a][(b - 1 + D) % D]
        nb = l + u + d + r + ul + ur + dl + dr
    else:
        l = universe.data[(a + 1)][b]
        r = universe.data[(a - 1)][b]
        ul = universe.data[(a + 1)][(b + 1)]
        ur = universe.data[(a - 1)][(b + 1)]
        dl = universe.data[(a + 1)][(b - 1)]
        dr = universe.data[(a - 1)][(b - 1)]
        u = universe.data[a][(b + 1)]
        d = universe.data[a][(b - 1)]
        nb = l + u + d + r + ul + ur + dl + dr
    return nb
