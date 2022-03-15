# CSE 202 Project Implementation: Rock Climbing
Jackob Getzel, Stewart Grant, Patrick Youssef

## Implementation Details


## Code Explanation

As the implementation for the project is quite long we will only be highlighting specific functions that we think are especially important to look at in regards to the implementation.

### Climber Functions

### Graph Instantiation

We never explicitly compute our graph as we quickly understood that the scale of the graph is quite large in this problem and instead spread the graph creation overhead across the traversal. Essentially, as we traverse instead of querying neighbors out of some data structure, we instead determine them in situ,

### BFS Climb

Our BFS implementation is pretty standard with some additions 

```python
def BFS_climb(wall, climber):
    visited_dict = dict()
    base_tuple = (-1, -1, -1, -1, -1, -1, -1, -1)
    visited_dict[base_tuple]] = base_tuple

    print_wall_with_climber(wall, climber)

    # BFS climber
    queue = find_next_valid_moves(climber, wall, visited_dict)
    while len(queue) != 0:
        climber = queue.pop(0)
        if can_complete(climber, wall, visited_dict):
            # print_path(climber, wall, visited_dict)
            print("Found Exit")
            return visited_dict, climber
        queue.extend(find_next_valid_moves(climber, wall, visited_dict))
    print("BFS failed unable to find path to the top")
```

### DFS Climb

As you can see the code for the DFS climb is extremely similar to the BFS climb code, but this is to be expected. The primary difference between BFS and DFS is how the next traversal is decided. As mentioned prior, BFS completes equal depth traversals and then steps into the next depth whereas DFS only goes into depth until hitting an endpoint. This behavior is characteristic fo the queue vs stack in BFS and DFS respectively.

```python
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
```

### Reconstructing Path

## Example Climbs

We saw much better behavior with BFS in terms or number of moves and seemingly redundant moves so the examples here were all generated with BFS.

![Video of an example pod run.](./files/path0.gif)
