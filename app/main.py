#!/usr/bin/env python

import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')

import bottle
import os
import random
import 

tList = [ 'Cash meowside how bout dat',
				'Cash meowside how bout dat',
				'Youve cat to be kitten me right meow',
				'Are you fur-real ?',
				'For a mewment like this, some people wait a lifetime',
				'Paw-lease',
				'I’ve cat to say, I’m not feline that way',
				'No need to have a hissy fit',
				'You’re pawful',
				'Let’s purrtend that never happened',
				'I don’t like your cattitude',
				'Your pissing meowff',
				'Happy Caturday']



SNAKE = 1
FOOD  = 2
def wall_protection(data):
    # If we are heading towards right or left wall.
    if my_snake['coord'][0][0] == data['width'] or my_snake['coord'][0][0] == -data['width']:
        # Move up or down
    # If we are heading towards the top or bottom wall
    elif my_snake['coord'][0][0] == data['height'] or my_snake['coord'][0][0] == -data['height']:
        # Move left or right

def readBoard(data):
    board = [[0 for col in xrange(data['width'])] for row in xrange(data['height'])]
    for snake in data['snakes']:
        for co in snake['coords']:
            board[co[1]][co[0]] = SNAKE
    for kibble in data['food']:
         board[kibble[1]][kibble[0]] = FOOD
    for row in board:
        print row


def find_food(data):
    for f in data['food']:
        grid[f[0]][f[1]] = FOOD


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
        'taunt': random.choice(tList),
        'head_url': head_url,
        'name': 'longCat',
        'tail_type': "curled",
        'head_type': "tongue",
    }

@bottle.post('/move')
def move():
    
    data = bottle.request.json

    readBoard(data)
    
    # TODO: Do things with data and stuff for this test commit and now I changed it again
    directions = ['up', 'down', 'left', 'right']


    # if we are travelling in direction 'key' then we cannot go directon 'value'
    # ie bad_directions['up'] = 'down' -- we cannot go back the direction we came from
    bad_directions = {'up':'down', 'down':'up', 'left':'right', 'right':'left'}

    my_snake = {}
    for snake in data['snakes']:
        if snake['id'] == data['you']:
            my_snake = snake
            break

    if data['turn'] == 0:
        return {
            'move': random.choice(directions),
            'taunt': random.choice(tList)
        }


    move = random.choice(directions)    

    

    move = random.choice(directions)

    while move == bad_directions[snake_direction(my_snake)]:
        move = random.choice(directions)

    moves = random.shuffle(directions)
    if moves[0] == bad_directions[snake_direction(my_snake)]:
        del moves[0]


    
    return {
        'move': move,
        'taunt': random.choice(tList)
    }

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
