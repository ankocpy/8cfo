# 迷路の解決: 迷路を表現した2次元リストを入力として受け取り、スタートからゴールまでの最短経路を見つけるプログラムを作成してください。
from copy import deepcopy as dc
maze = [
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
]
start = (0, 0)  # スタート地点 (行, 列)
end = (29, 29)    # ゴール地点 (行, 列)
H = 30 + 2
W = 30 + 2

def cal_dist(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

def proceed(pos, stack, maze, pre_positions, goal):
    y = pos[0]
    x = pos[1]
    if maze[y-1][x] == " ":
        maze[y-1][x] = 1 # 2 = check済み
        stack.append((y-1, x, cal_dist((y-1, x), goal)))
        pre_positions[y-1][x] = 3
    if maze[y+1][x] == " ":
        maze[y+1][x] = 1 # 2 = check済み
        stack.append((y+1, x, cal_dist((y+1, x), goal)))
        pre_positions[y+1][x] = 1
    if maze[y][x-1] == " ":
        maze[y][x-1] = 1 # 2 = check済み
        stack.append((y, x-1, cal_dist((y, x-1), goal)))
        pre_positions[y][x-1] = 4
    if maze[y][x+1] == " ":
        maze[y][x+1] = 1 # 2 = check済み
        stack.append((y, x+1, cal_dist((y, x+1), goal)))
        pre_positions[y][x+1] = 2   

# 周りの壁を追加  @アンコウ作
trueend = (end[0]+1, end[1]+1)
truestart = (start[0]+1, start[1]+1)

stack = [(truestart[0], truestart[1], cal_dist(truestart, trueend))]
#next_stack = []

new_maze = []

new_maze.append(["■"]*(len(maze[0])+2))

for i in range(len(maze)):
    new_l = ["■"]
    for j in range(len(maze[0])):
        if maze[i][j] == 0:
            new_l.append(" ")
        else:
            new_l.append("■")
    new_l.append("■")
    new_maze.append(new_l)

new_maze.append(["■"]*(len(maze[0])+2))

keep_maze = dc(new_maze)

'''
keep_maze[truestart[0]][truestart[1]] = "S"
keep_maze[trueend[0]][trueend[1]] = "G"

for row in keep_maze:
    print(' '.join(str(cell) for cell in row))
'''
    
pre_positions = []
for i in range(H):
    pre_positions.append([0] * W) # 0 = なし, 1 = 上, 2 = 左, 3 = 下, 4 = 右

cleared = False

while stack:
    nearest = min(stack, key=lambda x: x[2])
    index = stack.index(nearest)
    stack.pop(index)

    proceed((nearest[0], nearest[1]), stack, new_maze, pre_positions, trueend)
    if pre_positions[trueend[0]][trueend[1]] != 0:
        cleared = True
        break

if cleared:
    posy = trueend[0]
    posx = trueend[1]
    predir = pre_positions[posy][posx]
    while keep_maze[truestart[0]][truestart[1]] != ".":
        keep_maze[posy][posx] = "."
        if predir == 1:
            posy -= 1
        elif predir == 2:
            posx -= 1
        elif predir == 3:
            posy += 1
        else:
            posx += 1
        predir = pre_positions[posy][posx]
    keep_maze[truestart[0]][truestart[1]] = "S"
    keep_maze[trueend[0]][trueend[1]] = "G"
else:
    print("エラー：スタートとゴールがつながっていない可能性があります。")


for row in keep_maze:
    print(' '.join(str(cell) for cell in row))


"""
# 複製
keep_maze = dc(new_maze)

# 距離を求める
distance = 1
while trueend not in stack:
    check = False
    for x, y in stack:
        for i in range(4):
            if i == 0: # 上
                if new_maze[y - 1][x] == 0:
                    new_maze[y - 1][x] = distance
                    next_stack.append((x, y - 1))
                    check = True
            if i == 1: # 右
                if new_maze[y][x + 1] == 0:
                    new_maze[y][x + 1] = distance
                    next_stack.append((x + 1, y))
                    check = True
            if i == 2: # 下
                if new_maze[y + 1][x] == 0:
                    new_maze[y + 1][x] = distance
                    next_stack.append((x, y + 1))
                    check = True
            if i == 3: # 左
                if new_maze[y][x - 1] == 0:
                    new_maze[y][x - 1] = distance
                    next_stack.append((x - 1, y))
                    check = True
    if not check:
        print("エラー：スタートとゴールがつながっていない可能性があります。")
        break
    stack = next_stack
    next_stack = []
    distance += 1

# 距離を表示
print("距離表")
for i in new_maze:
    print(i)
x, y = trueend
distance = new_maze[y][x]
print(f"距離:{distance}")

# 逆順にたどる
while distance > 1:
    moved = False
    for i in range(4):
        if i == 0 and y > 0:  # 上
            if new_maze[y - 1][x] == distance - 1:
                y -= 1
                distance -= 1
                keep_maze[y][x] = 2
                break
        if i == 1 and x < len(new_maze[0]) - 1:  # 右
            if new_maze[y][x + 1] == distance - 1:
                x += 1
                distance -= 1
                keep_maze[y][x] = 2
                break
        if i == 2 and y < len(new_maze) - 1:  # 下
            if new_maze[y + 1][x] == distance - 1:
                y += 1
                distance -= 1
                keep_maze[y][x] = 2
                break
        if i == 3 and x > 0:  # 左
            if new_maze[y][x - 1] == distance - 1:
                x -= 1
                distance -= 1
                keep_maze[y][x] = 2
                break

for i in keep_maze:
    for j in i:
        if j == ".":
            i[i.index(j)] = 1
        elif j == "s":
            i[i.index(j)] = 3

keep_maze[trueend[1]][trueend[0]] = 4

# マップの解説
print("迷路の最短経路\n0=空白, 1=壁, 2=最短経路, 3=スタート地点, 4=ゴール地点")

# マップを出力
for row in keep_maze:
    print(' '.join(str(cell) for cell in row))

"""