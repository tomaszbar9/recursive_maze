import argparse
import random
import sys
import turtle

parser = argparse.ArgumentParser('Creates a maze of size s (width height)')
parser.add_argument('--attempts', help='number of attempts in case of exceeded recursion limit; defaults to 10', type=int, nargs=1, default=[10])
parser.add_argument('-s', '--size', help='number of cells: width, height; defaults to 40, 20', type=int, nargs=2, default=[40, 20])
parser.add_argument('-c', '--cell', help='side of one cell in pixels; defaults to 15', type=int, nargs=1, default=[15])
parser.add_argument('--close', help='close the turtle window when finished', action='store_true')
args = parser.parse_args()

WIDTH, HEIGHT = args.size
STEP = args.cell[0]
CLOSE = args.close
ATTEMPTS = args.attempts[0]

def make_maze(width: int, height: int) -> list:
    """
    Create a list of pairs of coordinates for each line representing closed side of every cell in the maze.
    :param int width: number of horizontal cells.
    :param int height: number of vertical cells.
    :return list: list of tuples of pairs of tuples containing two integers each: [((a, b), (c, d)), ...].
    """
    table = [[set() for _ in range(width)] for _ in range(height)]

    # Choose randomly coordinates of path's starting cell.
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)

    # Define oposite side.
    oposits = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

    def make_path(w: int, h: int):
        """Create a path recursively starting from the cell: table[h][w].
        :param int w: index of a column
        :param int h: index of a row
        """
        # Identify all neighbour cells.
        neighbours = {
            'n': (w, h - 1),
            's': (w, h + 1),
            'w': (w - 1, h),
            'e': (w + 1, h),
        }

        # Check all the directions in random order.
        directions = ['n', 's', 'e', 'w']
        random.shuffle(directions)    
        for direction in directions:
            x, y = neighbours[direction]
            if x in range(width) and \
                y in range(height) and \
                    not table[y][x]:
                    # If direction is available, add the relevant sides to the current and the next cell,
                    # and follow the path.
                    table[h][w].add(direction)
                    table[y][x].add(oposits[direction])           
                    make_path(x, y)
    make_path(x, y)

    # Collect lines' coordinates.
    lines = set()
    add_north = lambda x, y: lines.add(((x, y), (x + 1, y)))
    add_south = lambda x, y: lines.add(((x, y + 1), (x + 1, y + 1))) 
    add_west = lambda x, y: lines.add(((x, y), (x, y + 1))) 
    add_east = lambda x, y: lines.add(((x + 1, y), (x + 1, y + 1))) 

    for r, row in enumerate(table):
        for c  in range(len(row)):
            if c % 2 == r % 2:
                if r - 1 < 0:
                    add_north(c, r)
                if c - 1 < 0:
                    add_west(c, r)
                if r + 1 == height:
                    add_south(c, r)
                if c + 1 == width:
                    add_east(c, r)
            else:
                closed_dirs = ''.join([x for x in 'nwse' if x not in table[r][c]])
                for d in closed_dirs:
                    if 'n' in d:
                        add_north(c, r)
                    if 'w' in d:
                        add_west(c, r)
                    if 's' in d:
                        add_south(c, r)
                    if 'e' in d:
                        add_east(c, r)

    # "Open" border lines for start and end.
    start = ((0, height // 2), (0, height // 2 + 1))
    end = ((width, height // 2), (width, height // 2 + 1))
    lines.remove(start)
    lines.remove(end)
    return list(lines)


def lines_for_turtle(pairs: list) -> list:
    """
    Produce a list of lines' coordinates.        
    :param list pairs: coordinates of each closed line.
    :return list: list of lists, each sub-list contains continuous coordinates of one line.
            Lists are sorted from the longest to the shortest.
    """
    # For each piece of line, look for an adjacent line and join them.
    while True:
        added = False
        pairs_length = len(pairs)
        new = [pairs.pop(0)]
        for pair in pairs:
            for n in range(len(new)):
                if pair[0] in (new[n][0], new[n][-1]) or pair[-1] in (new[n][0], new[n][-1]):
                    if pair[0] == new[n][0]:
                        new[n] = pair[-1:0:-1] + new[n]
                    elif pair[0] == new[n][-1]:
                        new[n] += pair[1:]
                    elif pair[-1] == new[n][0]:
                        new[n] = pair[:-1] + new[n]
                    elif pair[-1] == new[n][-1]:
                        new[n] += pair[-2::-1]
                    added = True
                    break
            if added == True:
                added = False
                continue
            else:
                new.append(pair)      
        new_length = len(new)
        pairs = new
        if pairs_length == new_length:
            break
    pairs.sort(key=len, reverse=True)
    return pairs

pairs = []
for x in range(ATTEMPTS):
    try:
        pairs = make_maze(WIDTH, HEIGHT)
        break
    except RecursionError:
        pass

if len(pairs) == 0:
    print("""Sorry, the maze you tried to create was too big.
You can try again, changing the size to smaller or the number of attempts to larger.""")
    sys.exit(1)

joined_lines = lines_for_turtle(pairs)

# Turtle section
home = -(WIDTH * STEP) // 2, -(HEIGHT * STEP) // 2
turtle.hideturtle()
turtle.speed(0)
for l in joined_lines:
    turtle.penup()
    for x, y in l:
        x *= STEP
        y *= STEP
        turtle.setposition(x + home[0], y + home[1])
        turtle.pendown()

if not CLOSE:
    input("Press `enter` to close the turtle window.")