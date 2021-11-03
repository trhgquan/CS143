from collections import deque
def try_dfs(matrix, start, end,reached):
    # if start == end: return 
    # if end in reached: return reached
    # reached contain positions visited
    # find the neighbors of start
    neighbors = []
    start_row = start[0]
    start_col = start[1]

    #left
    if(matrix[start_row][start_col-1] != 'x'):
        neighbors.append((start_row,start_col-1))
    #right
    if(matrix[start_row][start_col+1] != 'x'):
        neighbors.append((start_row,start_col+1))
    #up
    if(matrix[start_row-1][start_col] != 'x'):
        neighbors.append((start_row-1,start_col))
    # down
    if(matrix[start_row+1][start_col] != 'x'):
        neighbors.append((start_row+1,start_col))


    for next in neighbors:
        if next not in reached:
            reached.append(next)
            route = try_dfs(matrix,next,end,reached)
            if end in route:
                break
    
    return reached