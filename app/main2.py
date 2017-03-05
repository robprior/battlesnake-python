#!/usr/bin/env python

import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')

import bottle
import os
import random

SNAKE = 1
FOOD  = 2
SAFETY = 3
WALL = 4

def wall_protection(data):
    # If we are heading towards right or left wall.
    if my_snake['coord'][0][0] == data['width'] or my_snake['coord'][0][0] == -data['width']:
        # Move up or down
    # If we are heading towards the top or bottom wall
    elif my_snake['coord'][0][0] == data['height'] or my_snake['coord'][0][0] == -data['height']:
        # Move left or right

def readBoard(data, snake):
    board = [[0 for col in xrange(data['width'])] for row in xrange(data['height'])]
    for co in snake['coords']:
        board[co[1]][co[0]] = SNAKE
    for kibble in data['food']:
         board[kibble[1]][kibble[0]] = FOOD
    for row in board:
        print row

def snake_length(snake):
    return len(snake.coords)

def snake_direction(snake):
    sdir = (snake['coords'][0][0] - snake['coords'][1][0], snake['coords'][0][1] - snake['coords'][1][1])
    return {
        (0,0):'FIRSTMOVE',
        (0,1):'down',
        (0,-1):'up',
        (1,0):'right',
        (-1,0):'left'
        }[sdir]

def in_bounds(width, height, coords):
    if (coords[0] > width) or (coords[0] < 0):
        return 0
    if (coords[1] > height) or (coords[1] < 0):
        return 0
    return 1

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']
    
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': 'Cash meowside how bout dat',
        'head_url': head_url,
        'name': 'longCat',
        'tail_type': "curled",
        'head_type': "tongue",
    }

@bottle.post('/move')
def move():
    
    
    data = bottle.request.json
    
    # TODO: Do things with data and stuff for this test commit and now I changed it again
    directions = ['up', 'down', 'left', 'right']
    
    
    # if we are travelling in direction 'key' then we cannot go directon 'value'
    # ie bad_directions['up'] = 'down' -- we cannot go back the direction we came from
    bad_directions = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}
    
    my_snake, board = parseBoard(data)
    possibleDirs = copy.deepcopy(directions)
    ourCoords = my_snake['coords']
    
    # testing finding the head
    #board[ourCoords[0]][ourCoords[0]] = '*'
    
    for row in board:
        print row
    
    # make a new list from the old list (both called possibleDirs)
    # only re add items to the list if it is not a bad direction
    #possibleDirs = [direc for direc in possibleDirs if not bad_directions[snake_direction(my_snake)]]
    
    moveto = [SAFETY, SAFETY, SAFETY, SAFETY]
    # Up
    if board[my_snake['coord'][0][0]][my_snake['coord'][0][1] - 1] is SNAKE:
        moveto[0] = SNAKE
    # Down
    elif board[my_snake['coord'][0][0]][my_snake['coord'][0][1]+ 1] is SNAKE:
        moveto[1] = SNAKE
    # Left
    elif board[my_snake['coord'][0][0] - 1 ][my_snake['coord'][0][1]+ 1] is SNAKE:
        moveto[2] = SNAKE
    # Right
    elif board[my_snake['coord'][0][0] + 1 ][my_snake['coord'][0][1]+ 1] is SNAKE:
        moveto[3] = SNAKE

    if my_snake['coord'][0][1] - 1 < 0:
        moveto[0] = WALL
    elif my_snake['coord'][0][1] + 1 > board_height - 1:
        moveto[1] = WALL
    elif my_snake['coord'][0][0] - 1 < 0:
        moveto[2] = WALL
    elif my_snake['coord'][0][0] + 1 > board_width - 1:
        moveto[3] = WALL


    # check over the remaining directions
    for dirs in possibleDirs:
        if dirs == 'left':
            newPos = ourCoord[1] - 1
            if newPos < 0 or board[newPos][ourCoords[0]] == 1:
                del dirs
        elif dirs == 'right':
            newPos = ourCoord[1] + 1
            if newPos >= data['width'] or board[newPos][ourCoords[0]] == 1:
                del dirs
        elif dirs == 'up':
            newPos = ourCoord[0] - 1
            if newPos < 0 or board[ourCoords[1]][newPos] == 1:
                del dirs
        elif dirs == 'down':
            newPos = ourCoord[0] + 1
            if newPos < 0 or board[ourCoords[1]][newPos] == 1:
                del dirs
    #while move == bad_directions[snake_direction(my_snake)]:
    #move = random.choice(directions)

    # TODO if len(possibleDirs) > 1 then we need heuristics
    if possibleDirs not None:
        move = possibleDirs[0]
    elif
        move = random.choice(directions)

    return {
        'move': move,
        'taunt': random.choice(tList)
#board
def makeboard(rows, cols):
    board = []
    for r in range(rows):
        brow = []
        for c in range(cols):
            if r == c == 0:
                 brow.append(' ')
            elif r == 0:
                 brow.append(str(c-1))
            elif c == 0:
                 brow.append(str(r-1))
            else:
                 brow.append('*')
        board.append(brow)
    return board

#b = makeboard(20,20)

#for row in b:
#    print ' '.join(row)
    
    
    
    ##


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
