# coding:utf-8
import os

import enum


class Root(object):
    MAIN = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')
    )
    DATA = '{}/.data'.format(MAIN)
    DOCUMENT = '{}/.doc'.format(MAIN)
    #
    main = '/'.join(
        os.path.dirname(__file__.replace('\\', '/')).split('/')
    )
    icon = '{}/.icon'.format(main)
    data = '{}/.data'.format(main)
    doc = '{}/.doc'.format(main)


class Data(object):
    ROOT = os.path.dirname(__file__.replace('\\', '/'))
    DATA_ROOT = '{}/.data'.format(ROOT)


class Orientation(enum.IntEnum):
    Horizontal = 0
    Vertical = 1


class Alignment(enum.IntEnum):
    Left = 0
    Right = 1


class Direction(enum.IntEnum):
    LeftToRight = 0
    RightToLeft = 1


class ActionFlag(enum.IntEnum):
    PressClick = 0x01
    PressDbClick = 0x02
    PressMove = 0x03
    #
    TrackClick = 0x11
    TrackMove = 0x12
    TrackCircle = 0x13
    #
    ZoomMove = 0x21
    #
    CheckClick = 0x31
    CheckDbClick = 0x32
    ExpandClick = 0x33
    OptionClick = 0x34
    ChooseClick = 0x35
    #
    SplitHHover = 0x41
    SplitVHover = 0x42
    SplitHPess = 0x43
    SplitVPess = 0x44
    SplitHMove = 0x45
    SplitVMove = 0x46
    #
    ZoomWheel = 0x51
    #
    RectSelectClick = 0x61
    RectSelectMove = 0x62
    #
    NGGraphTrackClick = 0x71
    NGGraphTrackMove = 0x72
    NGNodePressClick = 0x73
    NGNodePressMove = 0x74
    #
    KeyAltPress = 0x81
    KeyControlPress = 0x82
    KeyShiftPress = 0x83
    KeyControlShiftPress = 0x84
    #
    DragPress = 0x91
    DragMove = 0x92
    DragRelease = 0x93


class DragFlag(enum.IntEnum):
    Ignore = 0x00
    Copy = 0x01
    Move = 0x02


class RectRegion(enum.IntEnum):
    Unknown = 0
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4
    TopLeft = 5
    TopRight = 6
    BottomLeft = 7
    BottomRight = 8
    Inside = 9
    Outside = 10


class AlignRegion(enum.IntEnum):
    Unknown = 0
    Top = 1
    Bottom = 2
    Left = 3
    Right = 4
    TopLeft = 5
    TopRight = 6
    BottomLeft = 7
    BottomRight = 8
    Center = 9


class TagFilterMode(enum.IntEnum):
    MatchAll = 0
    MatchOne = 1


class SortMode(enum.IntEnum):
    Number = 0
    Name = 1


class SortOrder(enum.IntEnum):
    Ascend = 0
    Descend = 1


class Size(object):
    ITEM_HEIGHT = 20


class SectorChartMode(enum.IntEnum):
    Completion = 0
    Error = 1


class State(object):
    NORMAL = 'normal'
    ENABLE = 'enable'
    DISABLE = 'disable'
    WARNING = 'warning'
    ERROR = 'error'
    LOCKED = 'locked'
    LOST = 'lost'


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
