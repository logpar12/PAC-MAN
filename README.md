# PAC-MAN
BFS:

def get_path_direction(self, target):
    next_cell = self.find_next_cell_in_path(target)
    xdir = next_cell[0] - self.grid_pos[0]
    ydir = next_cell[1] - self.grid_pos[1]
    return vec(xdir, ydir)

def find_next_cell_in_path(self, target):
    path = a_star(self, [int(self.grid_pos.x), int(self.grid_pos.y)], [
       int(target[0]), int(target[1])])
    return path[1]

def BFS(maze, cost, start, end):
    # Create start and end node
    start_node = medium_Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = medium_Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = medium_Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

Time Complexity:

The search algorithm makes use of multiple loops with no recursion. 
Each ghost makes use of this search algorithm each time they go to 
a new tile. Thus this time complexity could be multipled by the number 
of tiles the ghost traverses in order to find the player.
In this case the time complexity is only caclcualted according to one ghost. 

The algoirthm mainly centers around a while loop the traverses the number
of tiles not yet visited by the ghost. All other compantents will be found
within this while loop. The list containing the tiles yet to be visited 
will change according to the number of tiles the ghost is from pac-man.

The list of not yet visited tiles will increase or decrease 
as the ghost gets closer to pacman. The yet_to_visit list contains 
a list of all child nodes that could result in finding pacman.

The first for-loop traveres the number of tiles not yet visited in 
order to find the smallest f value. This is crucial to finding the next 
tile the ghost should take. This loop alone is O(n). Yet (n) will be 
constantly changing.

The next for-loop is to create the children nodes of the tiles that have 
already been vistied. These child nodes are crucial in determining 
which tile the ghost should go next. The number of children nodes depends 
on the number of tiles left untilthe search algorithm has found its 
target: the user. 

The final for_loop is used to actually determine the values of g, h, and f
of each child node so that the rest of the algorithm can determine the 
best path to pacman. 

Finally, considering the search algorithm's components, 
the time complexity would be:
O(n^(8+m*n)) 
where n is the number of tiles the ghost is from pacman and
m is the number of children nodes for each parent tile.

Description: 

This pygame was created in Pycharms. In order to download the game, 
download Pycharms, download all necessary libraries such as pygames, 
then implement all classes found in the file. After that simple press play.
 
