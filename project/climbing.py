import copy
from email.mime import base
from tkinter import W
from tracemalloc import start

from matplotlib.pyplot import get
from walls import *
import os
import time
import heapq
import pickle


def manhattan_distance(A, B):
    return abs(A[0]-B[0])+abs(A[1]-B[1])


def limb_valid(a, b):
    if manhattan_distance(a.position, b.position) <= (a.length + b.length):
        return True
    return False


class Limb:
    length = 0
    position = (-1, -1)

    def __init__(self, l, p):
        self.length = l
        self.position = p


class Climber:

    left_arm = Limb(2, (-1, -1))
    right_arm = Limb(2, (-1, -1))
    left_leg = Limb(2, (-1, -1))
    right_leg = Limb(2, (-1, -1))

    # Adding repr to print out for climber debugging
    def __repr__(self):
        try:
            return "Climber with position: " + str(self.pos_tuple())
        except:
            return "Climber with no position"
        # (1,1,1,1,1,1,1,1)

    def set_position(self, position_tuple):
        self.left_arm = Limb(0, (position_tuple[0], position_tuple[1]))
        self.right_arm = Limb(0, (position_tuple[2], position_tuple[3]))
        self.left_leg = Limb(0, (position_tuple[4], position_tuple[5]))
        self.right_leg = Limb(0, (position_tuple[6], position_tuple[7]))

    def __copy__(self):
        c = Climber()
        c.left_arm = Limb(self.left_arm.length, self.left_arm.position)
        c.right_arm = Limb(self.right_arm.length, self.right_arm.position)
        c.left_leg = Limb(self.left_leg.length, self.left_leg.position)
        c.right_leg = Limb(self.right_leg.length, self.right_leg.position)
        return c

    def pos_tuple(self):
        return self.left_arm.position + self.right_arm.position + self.left_leg.position + self.right_leg.position

    def occupies_position(self, hold):
        if self.left_arm.position == hold:
            return True
        if self.right_arm.position == hold:
            return True
        if self.left_leg.position == hold:
            return True
        if self.right_leg.position == hold:
            return True
        return False

    def GetSymbol(self, i, j):
        if self.left_arm.position == (i, j):
            return "A"
        if self.right_arm.position == (i, j):
            return "B"
        if self.left_leg.position == (i, j):
            return "C"
        if self.right_leg.position == (i, j):
            return "D"
        return None

    def GetPresetLimbs(self):
        return [self.left_arm, self.right_arm, self.left_leg, self.right_leg]

    def GetLowestLimb(self):
        limbs = self.GetPresetLimbs()
        slims = sorted(limbs, key=lambda l: l.position[0])
        # for l in slims:
        #     print(l.position)
        # print()
        return slims

    def Get_Limbs(self):
        # return self.GetPresetLimbs()
        return self.GetLowestLimb()

    def valid(self):
        if(
            limb_valid(self.left_arm, self.right_arm) and
            limb_valid(self.left_arm, self.left_leg) and
            limb_valid(self.left_arm, self.right_leg) and
            limb_valid(self.right_arm, self.left_leg) and
            limb_valid(self.right_arm, self.right_leg) and
            limb_valid(self.left_leg, self.right_leg)
        ):
            return True
        return False


def print_wall(wall):
    for h_wall in wall:
        for hold in h_wall:
            print(hold, end='')
        print("")


def print_wall_with_climber(wall, climber):
    i, j = len(wall)-1, 0
    for h_wall in reversed(wall):
        j = 0
        for hold in h_wall:
            symbol = climber.GetSymbol(i, j)
            if symbol != None:
                print(symbol, end='')
            else:
                print(hold, end='')
            j = j+1
        print("")
        i = i-1
    print()

# traversal functions


def can_complete(climber, wall, visited_dict):
    for limb in climber.Get_Limbs():
        if limb.position[0] >= len(wall)-1:
            return True
    return False


def print_path(climber, wall, visited, animate=True):
    print("SOLUTION FOUND Printing path")
    moves = 0
    current_node = climber.pos_tuple()
    while current_node != visited[current_node]:
        if(animate == True):
            os.system('cls' if os.name == 'nt' else 'clear')
            print_wall_with_climber(wall, climber)
            time.sleep(0.5)
        else:
            print_wall_with_climber(wall, climber)

        current_node = visited[current_node]
        climber.set_position(current_node)
        moves = moves+1

    print("Completed in ", moves, " moves")


def mark_visited(visited, climber):
    visited[climber.pos_tuple()] = True


def has_visited(visited, climber):
    return visited.get(climber.pos_tuple())


def get_all_holds_highest_fist(wall):
    holds = []
    for i in range(len(wall)):
        for j in range(len(wall[i])):
            if wall[i][j] == 1:
                holds.append((i, j))

    hholds = sorted(holds, key=lambda v: v[0], reverse=True)
    return hholds


def get_all_holds(wall):
    holds = []
    for i in range(len(wall)):
        for j in range(len(wall[i])):
            if wall[i][j] == 1:
                holds.append((i, j))
    return holds


# find_candidate_holds=get_all_holds
find_candidate_holds = get_all_holds_highest_fist

# find next valid moves looks through each candidate hold, and returns all valid climber positions


def find_next_valid_moves(climber, wall, visited):
    moves = []
    holds = find_candidate_holds(wall)
    for hold in holds:
        copy_climber = copy.copy(climber)
        for limb in copy_climber.Get_Limbs():
            # The climbing must not have a limb on the same hold
            if climber.occupies_position(hold):
                continue
            tmp = limb.position
            limb.position = hold

            if copy_climber.valid() and not has_visited(visited, copy_climber):
                # set the prior move, to the current location
                visited[copy_climber.pos_tuple()] = climber.pos_tuple()
                moves.append(copy.copy(copy_climber))

            limb.position = tmp
    return moves


def find_next_valid_moves_test(climber, wall):
    moves = []
    holds = find_candidate_holds(wall)
    for hold in holds:
        copy_climber = copy.copy(climber)
        for limb in copy_climber.Get_Limbs():
            # The climbing must not have a limb on the same hold
            if climber.occupies_position(hold):
                continue
            tmp = limb.position
            limb.position = hold

            if copy_climber.valid():
                # set the prior move, to the current location
                moves.append(copy.copy(copy_climber))

            limb.position = tmp
    return moves


def BFS_climb(wall, climber):
    visited_dict = dict()
    visited_dict[(-1, -1, -1, -1, -1, -1, -1, -1)
                 ] = (-1, -1, -1, -1, -1, -1, -1, -1)

    print_wall_with_climber(wall, climber)

    # DFS climber
    queue = find_next_valid_moves(climber, wall, visited_dict)
    while len(queue) != 0:
        climber = queue.pop(0)
        if can_complete(climber, wall, visited_dict):
            # print_path(climber, wall, visited_dict)
            return visited_dict, climber
        queue.extend(find_next_valid_moves(climber, wall, visited_dict))
    print("BFS failed unable to find path to the top")


def DFS_climb(wall, climber):
    visited_dict = dict()
    visited_dict[(-1, -1, -1, -1, -1, -1, -1, -1)
                 ] = (-1, -1, -1, -1, -1, -1, -1, -1)

    print_wall_with_climber(wall, climber)

    # DFS climber
    stack = find_next_valid_moves(climber, wall, visited_dict)
    while len(stack) != 0:
        climber = stack.pop(0)
        if can_complete(climber, wall, visited_dict):
            print_path(climber, wall, visited_dict)
            return
        stack = find_next_valid_moves(climber, wall, visited_dict) + stack
    print("DFS failed unable to find path to the top")


def Dijkstra_climb(wall, climber):

    print_wall_with_climber(wall, climber)

    distances = dict()
    starting_vertex = (-1, -1, -1, -1, -1, -1, -1, -1)
    distances[starting_vertex] = 0

    pq = [(0, starting_vertex)]

    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances[current_vertex]:
            continue

        climber = Climber()
        climber.set_position(current_vertex)
        moves = find_next_valid_moves_test(climber, wall)
        weights = [1 for _ in moves]
        for neighbor, weight in zip(moves, weights):
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))


def get_path(visited, climber):
    # Rectify Path
    end = climber.pos_tuple()
    start = (-1, -1, -1, -1, -1, -1, -1, -1)

    path = [end]
    while True:
        end = visited[end]
        path.append(end)
        if end == start:
            break
    return path


# test_walls=[zigzag_wall]
test_walls = [staircase_wall_short, staircase_wall_long, zigzag_wall, big_zag]
# test_walls = [zigzag_wall]
for i, wall in enumerate(test_walls):
    climber = Climber()
    print(f"Starting Test {i}")
    visited, climber = BFS_climb(wall, climber)
    # DFS_climb(wall,climber)
    # Dijkstra_climb(wall, climber)

    # Save Path
    path = get_path(visited, climber)[::-1]

    # Create Data Struct
    base_climber = Climber()
    data = {"path": path, "wall": wall}

    with open(f"path_{i}.pkl", 'wb') as file:
        pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)
