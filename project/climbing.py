import copy
from walls import *
import os
import time

def manhattan_distance(A,B):
    return abs(A[0]-B[0])+abs(A[1]-B[1])


def limb_valid(a,b):
    if manhattan_distance(a.position,b.position) <= (a.length + b.length):
        return True
    return False

class Limb:
    length = 0
    position = (-1,-1)

    def __init__(self,l,p):
        self.length=l
        self.position=p

class Climber:

    left_arm=Limb(2,(-1,-1))
    right_arm=Limb(2,(-1,-1))
    left_leg=Limb(2,(-1,-1))
    right_leg=Limb(2,(-1,-1))

    def set_position(self, position_tuple):
       self.left_arm=Limb(0,(position_tuple[0],position_tuple[1])) 
       self.right_arm=Limb(0,(position_tuple[2],position_tuple[3])) 
       self.left_leg=Limb(0,(position_tuple[4],position_tuple[5])) 
       self.right_leg=Limb(0,(position_tuple[6],position_tuple[7])) 

    def __copy__(self):
        c = Climber()
        c.left_arm=Limb(self.left_arm.length,self.left_arm.position)
        c.right_arm=Limb(self.right_arm.length,self.right_arm.position)
        c.left_leg=Limb(self.left_leg.length,self.left_leg.position)
        c.right_leg=Limb(self.right_leg.length,self.right_leg.position)
        return c


    def pos_tuple(self):
        return self.left_arm.position + self.right_arm.position + self.left_leg.position + self.right_leg.position

    def occupies_position(self,hold):
        if self.left_arm.position == hold:
            return True
        if self.right_arm.position == hold:
            return True
        if self.left_leg.position == hold:
            return True
        if self.right_leg.position == hold:
            return True
        return False

    def GetSymbol(self,i,j):
        if self.left_arm.position == (i,j):
            return "A"
        if self.right_arm.position == (i,j):
            return "B"
        if self.left_leg.position == (i,j):
            return "C"
        if self.right_leg.position == (i,j):
            return "D"
        return None

    def GetPresetLimbs(self):
        return [self.left_arm,self.right_arm,self.left_leg,self.right_leg]

    def GetLowestLimb(self):
        limbs = self.GetPresetLimbs()
        slims = sorted(limbs, key=lambda l: l.position[0])
        # for l in slims:
        #     print(l.position)
        # print()
        return slims


    def Get_Limbs(self):
        #return self.GetPresetLimbs()
        return self.GetLowestLimb()

    
    def valid(self):
        if(
            limb_valid(self.left_arm,self.right_arm) and
            limb_valid(self.left_arm,self.left_leg) and
            limb_valid(self.left_arm,self.right_leg) and
            limb_valid(self.right_arm,self.left_leg) and
            limb_valid(self.right_arm,self.right_leg) and
            limb_valid(self.left_leg,self.right_leg)
        ):
            return True
        return False        



def print_wall(wall):
    for h_wall in wall:
        for hold in h_wall:
            print(hold, end='')
        print("")

def print_wall_with_climber(wall,climber):
    i,j=len(wall)-1,0
    for h_wall in reversed(wall):
        j=0
        for hold in h_wall:
            symbol = climber.GetSymbol(i,j)
            if symbol != None:
                print (symbol, end='')
            else:
                print(hold, end='')
            j=j+1
        print("")
        i=i-1
    print()

#traversal functions    
def can_complete(climber,wall,visited_dict):
    for limb in climber.Get_Limbs():
        if limb.position[0] >= len(wall)-1:
            return True
    return False

def print_path(climber,wall,visited,animate=True):
    print("SOLUTION FOUND Printing path")
    moves=0
    current_node = climber.pos_tuple()
    while current_node != visited[current_node]:
        if(animate==True):
            os.system('cls' if os.name == 'nt' else 'clear')
            print_wall_with_climber(wall,climber)
            time.sleep(0.1)
        else:
            print_wall_with_climber(wall,climber)
        
        current_node = visited[current_node]
        climber.set_position(current_node)
        moves=moves+1

    print("Completed in ", moves, " moves")


def mark_visited(visited,climber):
    visited[climber.pos_tuple()] = True

def has_visited(visited,climber):
    return visited.get(climber.pos_tuple())

def get_all_holds_highest_fist(wall):
    holds = []
    for i in range(len(wall)):
        for j in range(len(wall[i])):
            if wall[i][j] == 1:
                holds.append((i,j))
    
    hholds = sorted(holds, key=lambda v: v[0], reverse=True)
    return hholds

def get_all_holds(wall):
    holds = []
    for i in range(len(wall)):
        for j in range(len(wall[i])):
            if wall[i][j] == 1:
                holds.append((i,j))
    return holds

#find_candidate_holds=get_all_holds
find_candidate_holds=get_all_holds_highest_fist

#find next valid moves looks through each candidate hold, and returns all valid climber positions 
def find_next_valid_moves(climber, wall, visited):
    moves = []
    holds = find_candidate_holds(wall)
    for hold in holds:
        copy_climber = copy.copy(climber)
        for limb in copy_climber.Get_Limbs():
            #The climbing must not have a limb on the same hold
            if climber.occupies_position(hold):
                continue
            tmp = limb.position
            limb.position = hold

            if copy_climber.valid() and not has_visited(visited,copy_climber):
                #set the prior move, to the current location
                visited[copy_climber.pos_tuple()] = climber.pos_tuple()
                moves.append(copy.copy(copy_climber))
                
            limb.position = tmp
    return moves

def BFS_climb(wall,climber):
    visited_dict = dict()
    visited_dict[(-1,-1,-1,-1,-1,-1,-1,-1)] = (-1,-1,-1,-1,-1,-1,-1,-1)

    print_wall_with_climber(wall,climber)

    #DFS climber
    queue = find_next_valid_moves(climber,wall,visited_dict)
    while len(queue) != 0:
        climber = queue.pop(0)
        if can_complete(climber,wall,visited_dict):
            print_path(climber,wall,visited_dict)
            return
        queue.extend(find_next_valid_moves(climber,wall,visited_dict))
    print("BFS failed unable to find path to the top")

def DFS_climb(wall,climber):
    visited_dict = dict()
    visited_dict[(-1,-1,-1,-1,-1,-1,-1,-1)] = (-1,-1,-1,-1,-1,-1,-1,-1)

    print_wall_with_climber(wall,climber)

    #DFS climber
    stack = find_next_valid_moves(climber,wall,visited_dict)
    while len(stack) != 0:
        climber = stack.pop(0)
        if can_complete(climber,wall,visited_dict):
            print_path(climber,wall,visited_dict)
            return
        stack = find_next_valid_moves(climber,wall,visited_dict) + stack
    print("DFS failed unable to find path to the top")

#test_walls=[zigzag_wall]
test_walls=[staircase_wall_short,staircase_wall_long,zigzag_wall,big_zag]
climber = Climber()
for wall in test_walls:
    BFS_climb(wall,climber)
    #DFS_climb(wall,climber)
