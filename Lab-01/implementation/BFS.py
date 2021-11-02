from collections import deque
def try_bfs(matrix,start,end):
    #start have format (row, column)
    frontier = deque()
    reached = deque()
    frontier.append(start)
    reached.append(start)
    # frontier have tuple (x,y)
    # reached contain points that is visited

    while len(frontier) != 0:
        current = frontier.popleft() #current is (x,y)
        if(current == end): break
        x_pos = current[0] #row position
        y_pos = current[1] #column position
        neighbors = []
       
        # find the neighbors nearby current
        #left
        if(matrix[x_pos][y_pos-1] != 'x'):
            neighbors.append((x_pos,y_pos-1))
        #right
        if(matrix[x_pos][y_pos+1] != 'x'):
            neighbors.append((x_pos,y_pos+1))
        #up
        if(matrix[x_pos-1][y_pos] != 'x'):
            neighbors.append((x_pos-1,y_pos))
        # down
        if(matrix[x_pos+1][y_pos] != 'x'):
            neighbors.append((x_pos+1,y_pos))

        # neighbors not visited, put it in frontier
        for next in neighbors:
            if next not in reached:
                frontier.append(next)
                reached.append(next)
    # neighbors file contain the position visited 
    f = open('neighbors_BFS.txt','w')
    for pos in reached:
        print(pos,file = f)
    f.close()
    return reached
