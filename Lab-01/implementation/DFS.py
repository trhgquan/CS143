# from collections import deque
def try_bfs:
    # read map file into the program
    f = open('C:/Users/victo/CS143/Lab-01/sample/01.txt', 'rt')

    lines = f.readlines()
    f.close()
    #biểu diễn bản đồ
    points = int(lines[0].strip())
    list_maze_str = lines[points+1:]
    list_maze = []
    for line in list_maze_str:
        line = line.rstrip()
        list_line = list(line)
        list_maze.append(list_line)
    #lấy ra vị trí bắt đầu
    for list_item in list_maze:
        if 'S' in list_item:
            x_start = list_maze.index(list_item)
            y_start = list_item.index('S')
            break
    start_pos = (x_start,y_start)
    frontier = deque()
    reached = deque()
    frontier.append(start_pos)
    reached.append(start_pos)
    # frontier chứa biên theo dạng tuple (x,y)
    # reached chứa những điểm đã đi qua

    while len(frontier) != 0:
        current = frontier.popleft() #current có dạng (x,y)
        
        x_pos = current[0]
        y_pos = current[1]
        # print(x_pos,y_pos)
        neighbors = []
        #nếu đi vào ô điểm thưởng có thể ghi nhớ số điểm rồi trừ sau khi thoát khỏi mê cung
        # tìm những vị trí xung quanh có thể đi được từ phần tử mới nhất trong reached
        #đi xuống
        if(list_maze[x_pos][y_pos-1] != 'x'):
            neighbors.append((x_pos,y_pos-1))
        #đi lên
        if(list_maze[x_pos][y_pos+1] != 'x'):
        neighbors.append((x_pos,y_pos+1))
        # qua trái
        if(list_maze[x_pos-1][y_pos] != 'x'):
            neighbors.append((x_pos-1,y_pos))
        #qua phải
        if(list_maze[x_pos+1][y_pos] != 'x'):
            neighbors.append((x_pos+1,y_pos))

        for next in neighbors:
            if next not in reached:
                frontier.append(next)
                reached.append(next)
    # print(reached)
    for pos in reached:
        x_pos = pos[0]
        y_pos = pos[1]
        list_maze[x_pos][y_pos] = '*'
    f = open('out.txt','w')
    for line in list_maze:
        print(line,file = f)
    f.close()
    return list_maze
    # xác định vị trí bắt đầu
