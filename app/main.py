import bottle
import os
import random


def snake_direction(snake):
    if snake.coords[0][0] != snake.coords[1][0]:
        if snake.coords[0][0] > snake.coords[1][0]:
            return 'down'
        return 'up'
    if snake.coords[0][1] != snake.coords[1][1]:
        if snake.coords[0][1] > snake.coords[1][1]:
            return 'right'
        return 'left'

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
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json

    # TODO: Do things with data and stuff for this test commit and now I changed it again
    directions = ['up', 'down', 'left', 'right']

    return {
        'move': random.choice(directions),
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
