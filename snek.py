import random
import curses
from curses import textpad
from time import sleep

OPPOSITE_DIRECTION_DICT = {
    curses.KEY_UP: curses.KEY_DOWN,
    curses.KEY_DOWN: curses.KEY_UP,
    curses.KEY_RIGHT: curses.KEY_LEFT,
    curses.KEY_LEFT: curses.KEY_RIGHT
}

DIRECTIONS_LIST = [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP]



def create_food(snake, box):
    """Simple function to find coordinates of food which is inside box and not on snake body"""
    food = None
    while food is None:
        food = [random.randint(box[0][0]+1, box[1][0]-1), 
        random.randint(box[0][1]+1, box[1][1]-1)]
        if food in snake:
            food = None
    return food


def main(stdscr):
    """
    Variables & Main loop
    """
    wait = 5
    cursor_x = 0
    cursor_y = 0
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    height, width = stdscr.getmaxyx()
    cursor_x = max(0, cursor_x)
    cursor_x = min(width-1, cursor_x)

    cursor_y = max(0, cursor_y)
    cursor_y = min(height-1, cursor_y)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    title = "Curses example"[:width-1]
    subtitle = "Written by Clay McLeod"[:width-1]
    statusbarstr = "Press ^C to exit | Cursed Snek | Width: {}, Height: {}".format(width, height)

    """
    Calculations for centering the title and subtitle
    """
    start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
    start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
    start_y = int((height // 2) - 2)

    stdscr.attroff(curses.color_pair(2))
    stdscr.attroff(curses.A_BOLD)

    """
    Render some text
    """
    stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
    stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)

    stdscr.clear()
    stdscr.refresh()
    stdscr.attron(curses.color_pair(3))
    stdscr.addstr(height-1, 0, statusbarstr)
    stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(3))

    """
    Render box
    """
    
    sh, sw = stdscr.getmaxyx()
    box = [[3,3], [sh-3, sw-3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

    """
    Create snek
    """
    snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]]
    direction = curses.KEY_RIGHT

    """
    Draw snek
    """
    
    for y,x in snake:
        stdscr.addstr(y, x, '#')

    """
    Food
    """
    food = create_food(snake, box)
    stdscr.addstr(food[0], food[1], '*')

    
    score = 0
    score_text = "Score: {}".format(score)
    stdscr.addstr(1, sw//2 - len(score_text)//2, score_text)
    
    """
    Screen size (height, width) ignored for now
    whstr = "Width: {}, Height: {}".format(width, height)
    stdscr.addstr(0, 0, whstr, curses.color_pair(1))
    """

    while 1:
        """
        Quit thing
        """
        key = stdscr.getch()

        if key in DIRECTIONS_LIST and key != OPPOSITE_DIRECTION_DICT[direction]:
            direction = key

        """
        Snek Head
        """
        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]

        """
        New head
        """
        stdscr.addstr(new_head[0], new_head[1], '#')
        snake.insert(0, new_head)

        if snake[0] == food:
            score += 1
            score_text = "Score: {}".format(score)
            stdscr.addstr(1, sw//2 - len(score_text)//2, score_text, curses.color_pair(2))

            food = create_food(snake, box)
            stdscr.addstr(food[0], food[1], '*')

            stdscr.timeout(100 - (len(snake)//3)%90)
        else:
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        if (snake[0][0] in [box[0][0], box[1][0]] or 
            snake[0][1] in [box[0][1], box[1][1]] or 
            snake[0] in snake[1:]):
            msg = "Game Over, Score: {}".format(score)
            stdscr.addstr(sh//2, sw//2-len(msg)//2, msg, curses.color_pair(1))
            stdscr.nodelay(0)
            stdscr.getch()
            sleep(wait)
            break

curses.wrapper(main)