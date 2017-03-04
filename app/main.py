#!/usr/bin/env python

import sys
sys.path.append('/usr/local/lib/python3.6/site-packages')

import bottle
import os
import random

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

    my_snake = {}
    for snake in data['snakes']:
        if snake['id'] == data['you']:
            my_snake = snake
            break

    if data['turn'] == 0:
        return {
            'move': random.choice(directions),
            'taunt': 'For a mewment like this, some people wait a lifetime'
        }
    
    moves = random.shuffle(directions)
    if moves[0] == bad_directions[snake_direction(my_snake)]:
        del moves[0]
    
    return {
        'move': moves[0],
        'taunt': "Youve cat to be kitten me right meow"
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

b = makeboard(20,20)

for row in b:
    print ' '.join(row)
    
    
    
    ##


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
