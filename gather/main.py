import numpy as np



def make_universe(
        size=100, edge_ratio=1, born=0b01000, live=0b01100, beta=0.4,
        states=2, init='random'
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
    uni.states = states
    uni.data = np.zeros((size, uni.width))
    if init=='random':
        uni.data = np.random.randint(0, uni.states, (size, uni.width))
    elif init=='center':
        center = np.random.randint(1, uni.states, (20, 20))
        uni.data[(uni.size//2)-10:(uni.size//2)+10,(uni.width//2)-10:(uni.width//2)+10] = center
    elif init=='none':
        pass
    uni.back = uni.data.copy()
    uni.has_space = has_neumann_space(uni)

    return uni

def update_universe(method, universe):
    pass

def has_neumann_space(universe):
    """
    Find live positions which have space in their neumann neighborhood
    """
    occupied = np.argwhere(universe.data)
    has_space = []
    for position in occupied:
        if neumann_neighbors_sum(position, universe) < 4:
            has_space.append(position)
    return has_space

def eden(universe):
    """
    Basic eden model implementation
    """
    index = np.random.randint(0, len(universe.has_space))
    site = universe.has_space.pop(index)
    if neumann_neighbors_sum(site, universe) == 4:
        return
    target = choose_neumann_neighbor(site, universe)
    universe.data[target[0], target[1]] = universe.data[site[0], site[1]]
    universe.back = universe.data.copy()
    if neumann_neighbors_sum(site, universe) < 4:
        universe.has_space.append(site)
    if neumann_neighbors_sum(target, universe) < 4:
        universe.has_space.append(target)

def print_array(universe):
    """
    Performs a basic print.

    :param universe:    the univese, containing the data to print
    :return:            None
    """
    temp = np.empty_like(universe.data, str)
    out = []
    transcript = {0.0: '.',
                  1.0: 'm',
                  2.0: 'p',
                  }
    for i in range(universe.size):
        for j in range(universe.width):
            temp[i][j] = transcript[universe.data[i][j]]
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
    universe.back = universe.data
    for _ in range(int(updates * N * D)):
        a = int(np.random.random() * N)
        b = int(np.random.random() * D)
        nb = neumann_neighbors_same([a,b], universe)
        if nb - 2 <= 0 or np.random.random() < cost[nb - 2]:
            universe.data[a, b] = 1 - universe.data[a, b]

def conway(universe):
    """
    Performs conway update on the array.

    :param universe: the universe
    :return:        None
    """
    N = universe.size
    D = universe.width
    universe.back = universe.data.copy()
    for i in range(N):
        for j in range(D):
            NB = moore_neighbors_sum([i,j], universe)
            if universe.back[i][j] == 1:
                universe.data[i][j] = (universe.live>>NB)&1
            else:
                universe.data[i][j] = (universe.born>>NB)&1

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
            NB = [l[i][j], r[i][j], u[i][j], d[i][j], ul[i][j], ur[i][j],\
               dl[i][j], dr[i][j]]
            if universe.data[i][j] == 1:
                universe.data[i][j] = (universe.live>>NB.count(True))&1
            else:
                universe.data[i][j] = (universe.born>>NB.count(True))&1

def neumann_neighbors_same(pos, universe):
    """
    Calculates the number of neumann neighbors that share state with the position.

    :param pos:         position to be checked
    :param universe: the universe
    :return:            neighbors
    """
    a = pos[0]
    b = pos[1]
    if universe.back[a, b]:
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
        l = universe.back[(a + 1) % N][b]
        r = universe.back[(a - 1 + N) % N][b]
        u = universe.back[a][(b + 1) % D]
        d = universe.back[a][(b - 1 + D) % D]
        nb = np.asarray([l, u, d, r])
    else:
        l = universe.back[(a + 1)][b]
        r = universe.back[(a - 1)][b]
        u = universe.back[a][(b + 1)]
        d = universe.back[a][(b - 1)]
        nb = np.asarray([l, u, d, r])
    return np.sum(nb > 0)

def choose_neumann_neighbor(pos, universe):
    """
    Given a position, look for an empty space and pick one

    :param pos:         position to be checked
    :param universe: the universe
    :return:            neighbor position
    """
    NB = neighbor_coords(pos, universe)
    nb = np.asarray(neighbor_truth(pos, universe))
    choice = int((np.random.random() * np.sum(nb == 0)))
    pos_list = np.argwhere(nb == 0).flatten()
    return np.asarray(NB[pos_list[choice]])

def neighbor_truth(pos, universe):
    """Returns the state of the neighbors"""
    N = universe.size
    D = universe.width
    l = universe.back[(pos[0] + 1) % N][pos[1]]
    r = universe.back[(pos[0] - 1 + N) % N][pos[1]]
    u = universe.back[pos[0]][(pos[1] + 1) % D]
    d = universe.back[pos[0]][(pos[1] - 1 + D) % D]
    return [l, u, d, r]

def neighbor_coords(pos, universe):
    """Returns the coordinates of neighbors"""
    N = universe.size
    D = universe.width
    L = [(pos[0] + 1) % N, pos[1]]
    R = [(pos[0] - 1 + N) % N, pos[1]]
    U = [pos[0], (pos[1] + 1) % D]
    D = [pos[0], (pos[1] - 1 + D) % D]
    return [L, U, D, R]

def moore_neighbors_same(pos, universe):
    """
    Calculates the number of moore neighbors that share state with the position.

    :param pos:         position to be checked
    :param universe: the universe
    :return:            neighbors
    """
    a = pos[0]
    b = pos[1]
    if universe.back[a, b]:
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
        l = universe.back[(a + 1) % N][b]
        r = universe.back[(a - 1 + N) % N][b]
        ul = universe.back[(a + 1) % N][(b + 1) % D]
        ur = universe.back[(a - 1 + N) % N][(b + 1) % D]
        dl = universe.back[(a + 1) % N][(b - 1 + D) % D]
        dr = universe.back[(a - 1 + N) % N][(b - 1 + D) % D]
        u = universe.back[a][(b + 1) % D]
        d = universe.back[a][(b - 1 + D) % D]
        nb = [l, u, d, r, ul, ur, dl, dr]
    else:
        l = universe.back[(a + 1)][b]
        r = universe.back[(a - 1)][b]
        ul = universe.back[(a + 1)][(b + 1)]
        ur = universe.back[(a - 1)][(b + 1)]
        dl = universe.back[(a + 1)][(b - 1)]
        dr = universe.back[(a - 1)][(b - 1)]
        u = universe.back[a][(b + 1)]
        d = universe.back[a][(b - 1)]
        nb = [l, u, d, r, ul, ur, dl, dr]
    return nb.count(True)
