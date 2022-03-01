import copy

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

    def occupies_position(self,i,j):
        if self.left_arm.position == (i,j):
            return True
        if self.right_arm.position == (i,j):
            return True
        if self.left_leg.position == (i,j):
            return True
        if self.right_leg.position == (i,j):
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

    def Get_Limbs(self):
        return [self.left_arm,self.right_arm,self.left_leg,self.right_leg]

    
    def valid(self):
        if(
            limb_valid(self.left_arm,self.right_arm) and
            limb_valid(self.left_arm,self.left_leg) and
            limb_valid(self.left_arm,self.right_leg) and
            #right arm
            limb_valid(self.right_arm,self.left_leg) and
            limb_valid(self.right_arm,self.right_leg) and
            #
            limb_valid(self.left_leg,self.right_leg)
        ):
            return True
        return False        

staircase_wall = [[1,1,1,1,1],
[0,0,0,0,0],
[1,1,1,1,1],
[0,0,0,0,0],
[1,1,1,1,1]]


def print_wall(wall):
    for h_wall in wall:
        for hold in h_wall:
            print(hold, end='')
        print("")

def print_wall_with_climber(wall,climber):
    i,j=0,0
    for h_wall in wall:
        j=0
        for hold in h_wall:
            symbol = climber.GetSymbol(i,j)
            if symbol != None:
                print (symbol, end='')
            else:
                print(hold, end='')
            j=j+1
        print("")
        i=i+1
    print()

visited_dict = dict()
visited_dict[(-1,-1,-1,-1,-1,-1,-1,-1)] = (-1,-1,-1,-1,-1,-1,-1,-1)

def mark_visited(visited,climber):
    visited[climber.pos_tuple()] = True

def has_visited(visited,climber):
    return visited.get(climber.pos_tuple())


#traversal functions    
def get_all_holds(wall):
    holds = []
    i=0
    for row in wall:
        j=0
        for colum in row:
            if wall[i][j] == 1:
                holds.append((i,j))
            j=j+1
        i=i+1
    return holds
    
def find_next_valid_moves(climber, wall, visited):
    moves = []
    holds = get_all_holds(wall)
    for hold in holds:
        copy_climber = copy.copy(climber)
        for limb in copy_climber.Get_Limbs():
            if climber.occupies_position(hold[0],hold[1]):
                continue
            tmp = limb.position
            limb.position = hold

            if copy_climber.valid() and not has_visited(visited,copy_climber):
                visited[copy_climber.pos_tuple()] = climber.pos_tuple()
                moves.append(copy.copy(copy_climber))
                
            limb.position = tmp
    return moves

def can_complete(climber,wall,visited_dict):
    for limb in climber.Get_Limbs():
        if limb.position[0] >= len(wall)-1:
            return True
    return False

def print_path(climber,wall,visited):
    moves=0
    current_node = climber.pos_tuple()
    while current_node != visited[current_node]:
        #print(current_node)
        moves=moves+1
        print_wall_with_climber(wall,climber)
        current_node = visited[current_node]
        climber.set_position(current_node)

    print("Completed in ", moves, " moves")



#print_wall(staircase_wall)
climber = Climber()
print_wall_with_climber(staircase_wall,climber)

queue = []
moves = find_next_valid_moves(climber,staircase_wall,visited_dict)
for move in moves:
    queue.append(move)

while len(queue) != 0:
    climber = queue.pop(0)
    #print_wall_with_climber(staircase_wall,climber)
    #print()
    #check for victory
    if can_complete(climber,staircase_wall,visited_dict):
        print("SOLUTION FOUND")
        print_path(climber,staircase_wall,visited_dict)
        exit(1)

    moves = find_next_valid_moves(climber,staircase_wall,visited_dict)
    for move in moves:
        queue.append(move)



print()
for move in moves:
    print(move.pos_tuple())

if climber.valid():
    print ("Valid")
else:
    print("invalid")

