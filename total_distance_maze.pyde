# import random
import time
from heapq import heappush, heappop

n_rows = 120
n_cols = 165

# step = n_rows * n_cols
step = 0
edges = []
dists = None
max_dist = -1

def setup():
    size(1024, 768)
    noStroke()
    loop()
    frameRate(200)

    global edges, dists, max_dist
    edges, dists = generate_maze(n_rows * n_cols)
    for row in dists:
        max_dist = max(max_dist, max(row))


def draw():
    global step
    global edges
    
    while step < len(edges):
        start_node, end_node = edges[step]
        
        h_val = 20.0 * dists[end_node[0]][end_node[1]]/max_dist + 45.0
        # h_val = 50.0 * dists[end_node[0]][end_node[1]]/max_dist + 25.0
        # h_val = 100.0 * dists[end_node[0]][end_node[1]]/max_dist
    
        if step == 0:
            background(180)
            draw_empty_maze()
            draw_node(start_node, h_val)
    
        # generate_maze(step)
    
        draw_node(end_node, h_val)
        draw_edge(start_node, end_node, h_val)
    
        step += 1
        time.sleep(0.005)
    
        # draw_steps(steps)
        if step >= len(edges):
            noLoop()


def draw_empty_maze():
    fill(15)
    rect(x_offset(), y_offset(), maze_width(), maze_height())


def generate_maze(maze_size):
    # edges = [[c * r for c in range(n_cols)]
    #          for r in range(2 * n_rows)]

    edges = [[int(random(1, 50)) for c in range(n_cols)]
             for r in range(2 * n_rows)]
    
    dists = [[-1 for c in range(n_cols)]
             for r in range(n_rows)]

    order = []  # store the edges in the order they're added
    
    start_node = (n_rows/2, n_cols/2)
    start_node = (int(random(n_rows)), int(random(n_cols)))

    in_tree = {start_node}
    dists[start_node[0]][start_node[1]] = 0
    candidates = []
    for n in get_neighbors(start_node, edges):
        heappush(candidates, (n[1], (start_node, n[0])))
    # draw_node(0, 0)
    while len(in_tree) < maze_size:
        cost, (edge_start, edge_end) = heappop(candidates)
        if edge_end in in_tree:
            continue
        for neigh, neigh_cost in get_neighbors(edge_end, edges):
            if neigh not in in_tree:
                heappush(candidates, (neigh_cost, (edge_end, neigh)))
        in_tree.add(edge_end)
        order.append((edge_start, edge_end))
        dists[edge_end[0]][edge_end[1]] = cost + dists[edge_start[0]][edge_start[1]]

    return order, dists

def draw_steps(steps):
    pass


#########################
#
# Helpers
#
#########################

def get_neighbors(node, edges):
    neighbors = []
    for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        row = node[0] + dir[0]
        col = node[1] + dir[1]
        if 0 <= row < n_rows and 0 <= col < n_cols:
            neigh = (row, col)
            neighbors.append((neigh, get_cost(node, neigh, edges)))
    return neighbors

def get_cost(node1, node2, edges):
    dir = (node1[0] - node2[0], node1[1] - node2[1])
    if dir not in {(0, 1), (1, 0), (0, -1), (-1, 0)}:
        raise Exception('invalid dir: {}'.format(dir))
    if dir == (0, 1):
        return edges[2 * node1[0]][node1[1]]
    elif dir == (0, -1):
        return edges[2 * node1[0]][node1[1] - 1]
    elif dir == (1, 0):
        return edges[2 * node1[0] + 1][node1[1]]
    else:  # dir == (-1, 0)
        return edges[2 * node1[0] - 1][node1[1]]

def square_edge_length():
    fill_height_size = height / (3 + 2 * n_rows)
    fill_width_size = width / (3 + 2 * n_cols)
    return min(fill_height_size, fill_width_size)

def maze_width():
    return square_edge_length() * (1 + 2 * n_cols)

def maze_height():
    return square_edge_length() * (1 + 2 * n_rows)

def x_offset():
    return (width - maze_width()) / 2

def y_offset():
    return (height - maze_height()) / 2

def draw_node(node, hue_val):
    # fill(245)
    colorMode(HSB, 100, 100, 100)
    fill(hue_val, 100, 100)
    column = node[1]
    row = node[0]
    edge = square_edge_length()
    rect(
        x_offset() + edge * (1 + 2 * column),
        y_offset() + edge * (1 + 2 * row),
        edge,
        edge,
    )

def draw_edge(node1, node2, hue_val):
    # fill(245)
    colorMode(HSB, 100, 100, 100)
    fill(hue_val, 100, 100)
    edge = square_edge_length()
    rect(
        x_offset() + edge * (1 + node1[1] + node2[1]),
        y_offset() + edge * (1 + node1[0] + node2[0]),
        edge,
        edge,
    )
