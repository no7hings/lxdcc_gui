# coding:utf-8


class Html(object):
    RED = 'red'
    YELLOW = 'yellow'
    ORANGE = 'orange'
    GREEN = 'orange'
    BLUE = 'blue'
    WHITE = 'white'
    GRAY = 'gray'
    BLACK = 'black'

    COLORS = [
        '#ff003f',  # 0 (255, 0, 63)
        '#fffd3f',  # 1 (255, 255, 63)
        '#ff7f3f',  # 2 (255, 127, 63)
        '#3fff7f',  # 3 (64, 255, 127)
        '#3f7fff',  # 4 (63, 127, 255)

        '#dfdfdf',  # 5 (223, 223, 223)
        '#dfdfdf',  # 6 (191, 191, 191)
        '#7f7f7f',  # 7 (127, 127, 127)
        '#3f3f3f',  # 8 (63, 63, 63)
        '#1f1f1f'  # 9 (31, 31, 31)
    ]
    COLOR_DICT = {
        RED: COLORS[0],
        YELLOW: COLORS[1],
        ORANGE: COLORS[2],
        GREEN: COLORS[3],
        BLUE: COLORS[4],

        WHITE: COLORS[5],
        GRAY: COLORS[7],
        BLACK: COLORS[9]
    }
