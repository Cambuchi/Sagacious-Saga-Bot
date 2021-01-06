#! python3
# sagaciousSagaBot.py - bot that plays sagacious saga using floodfill
# recursion.

import pyautogui
import logging
import time
from pprint import pformat

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
#logging.disable(logging.DEBUG) # un/comment to un/block debug log messages
#logging.disable(logging.INFO) # un/comment to un/block info log messages

blue = [(67, 192, 241), (103, 204, 242),
        (90, 201, 245), (86, 197, 241),
        (52, 180, 235), (57, 183, 238),
        (27, 166, 227), (20, 152, 206),
        (127, 208, 242), (132, 212, 246)]
green = [(160, 206, 45), (146, 194, 41),
         (151, 192, 41), (135, 171, 39),
         (131, 174, 40), (161, 208, 57),
         (179, 214, 83), (172, 214, 82),
         (171, 212, 72), (180, 217, 93)]
red = [(242, 55, 53), (243, 58, 60),
       (245, 87, 87), (247, 82, 86),
       (244, 78, 77), (242, 67, 68),
       (242, 116, 115), (248, 120, 119),
       (246, 113, 115), (248, 91, 96),
       (245, 104, 105), (203, 16, 13),
       (210, 5, 17), (182, 17, 16)]
purple = [(129, 89, 151), (98, 67, 113),
          (101, 71, 116), (94, 64, 109),
          (124, 82, 138), (120, 84, 138),
          (132, 92, 154), (144, 107, 162),
          (137, 101, 156), (141, 97, 155),
          (155, 118, 174), (158, 121, 178),
          (150, 106, 164), (145, 105, 168)]
yellow = [(255, 204, 0), (255, 208, 12),
          (253, 213, 38), (255, 210, 36),
          (253, 214, 50), (254, 215, 62),
          (253, 216, 80), (253, 222, 84),
          (254, 207, 0), (231, 187, 0),
          (201, 163, 0), (230, 182, 1),
          (225, 183, 0), (240, 189, 0),
          (251, 199, 0), (208, 169, 0)]
white = [(203, 205, 202), (185, 187, 184),
         (164, 166, 163), (168, 170, 167),
         (148, 150, 147), (194, 196, 193),
         (199, 201, 198), (212, 214, 211),
         (209, 211, 208), (216, 218, 215),
         (222, 224, 221)]

def createGrid():
    # make the grid for game, top two rows are bugged (can't click) so it's 8r x 10c
    logging.debug('Creating 8r x 10c game grid...')
    global sagaGrid
    sagaGrid = []
    for i in range(8):
        sagaGrid.append([i] * 10)
    for r in range(8):
        for c in range(10):
            sagaGrid[r][c] = ''
    logging.debug(f"Game grid made. Size is {len(sagaGrid)} rows by {len(sagaGrid[0])} columns.")
    logging.debug('\n' + (pformat(sagaGrid)))
    return sagaGrid

def getGameRegion():
    # get the game region by finding an image of the game's top left
    # corner somewhere on the screen to base GAME_REGION's coordinates
    global GAME_REGION

    # identify the top left-corner
    logging.debug('Finding game region...')
    region = pyautogui.locateOnScreen(r'images\UpLeftCorner.png')
    if region is None:
        raise Exception('Could not find game on screen. Is the game visible?')

    # calculate the region of the entire game
    topLeftX = region[0]
    topLeftY = region[1]
    GAME_REGION = (topLeftX, topLeftY, 540, 360)
    logging.debug('Game region found: %s' % (GAME_REGION,))

def getPastGameMenu():
    # get past the game menu that loads up every time the game initializes
    global GAME_REGION
    # click on How To Play
    logging.debug('Looking for How To Play button...')
    while True:
        pos = pyautogui.locateCenterOnScreen((r'images\HowToPlay.png'), region=GAME_REGION)
        if pos is not None:
            break
    pyautogui.click(pos, duration=0.25)
    logging.debug('Clicked on How To Play button.')

    # move mouse down to detect play button img accurately
    pyautogui.moveTo(GAME_REGION[0], GAME_REGION[1], duration = 0.25)

    # click on Play!
    logging.debug('Looking for Play button...')
    while True:
        pos2 = pyautogui.locateCenterOnScreen((r'images\Play.png'), region=GAME_REGION)
        if pos2 is not None:
            break
    pyautogui.click(pos2, duration=0.25)
    logging.debug('Clicked on How To Play button.')

def setupCoordinates():
    # setup all the clickable zones, using GAME_REGION, assigns values
    # of screen coordinates to each (x,y) coordinate pair in sagaGrid
    logging.debug('Setting up coordinate grid dictionary...')
    global CLICK_COORDS
    global sagaGrid
    sagaClick = []
    CLICK_COORDS = {}
    initialRight = 119
    initialTop = 50 + 58

    for c in range(len(sagaGrid[0])):
        sagaClick.append([])
        for r in range(len(sagaGrid)):
            sagaClick[c].append((r, c))

    for x in range(len(sagaGrid[0])):
        if x == 0:
            moveRight = initialRight
        else:
            moveRight += 31
        for y in range(len(sagaGrid)):
            if y == 0:
                moveTop = initialTop
            else:
                moveTop += 31
            CLICK_COORDS[sagaClick[x][y]] = (GAME_REGION[0]+moveRight,
                                             GAME_REGION[1]+moveTop)
    logging.debug('Coordinate dictionary has been set up.')
    logging.debug('\n' + (pformat(CLICK_COORDS)))

def confirmShortcut():
    # space saver for checking if colors exist on the gameboard
    if any('b' in s1 for s1 in sagaGrid):
        return True
    if any('r' in s1 for s1 in sagaGrid):
        return True
    if any('g' in s1 for s1 in sagaGrid):
        return True
    if any('y' in s1 for s1 in sagaGrid):
        return True
    if any('w' in s1 for s1 in sagaGrid):
        return True
    else:
        return False

def colorConfirmer(r, c):
    # optional color gathering loop, faster than going through whole
    # entire grid loop for just a single coordinate
    global sagaGrid
    x = pyautogui.pixel(CLICK_COORDS[r, c][0],
                        CLICK_COORDS[r, c][1])
    logging.debug('Color found is' + str(x))
    if x in blue:
        logging.debug('Blue found')
        sagaGrid[r][c] = 'b'
        return
    if x in red:
        logging.debug('Red found')
        sagaGrid[r][c] = 'r'
        return
    if x in green:
        logging.debug('Green found')
        sagaGrid[r][c] = 'g'
        return
    if x in purple:
        logging.debug('Purple found')
        sagaGrid[r][c] = 'p'
        return
    if x in yellow:
        logging.debug('Yellow found')
        sagaGrid[r][c] = 'y'
        return
    if x in white:
        logging.debug('White found')
        sagaGrid[r][c] = 'w'
        return
    if x == (0, 0, 0):
        logging.debug('Black found')
        sagaGrid[r][c] = 'k'
        return
    if x == (255, 255, 255):
        checkGameOver()
    if x == (164, 164, 164):
        checkGameOver()
    else:
        logging.debug('Final color check not in list found...')
        checkGameOver()


def getColor():
    # loops through grid and grabs colors with pyautogui
    logging.debug('Putting colors from screen coordinates into game grid...')
    global sagaGrid
    for r in range(len(sagaGrid)):
        for c in range(len(sagaGrid[0])):
            x = pyautogui.pixel(CLICK_COORDS[r, c][0],
                                CLICK_COORDS[r, c][1])
            logging.debug('Color found is' + str(x))
            if x in blue:
                logging.debug('Blue found')
                sagaGrid[r][c] = 'b'
                continue
            if x in red:
                logging.debug('Red found')
                sagaGrid[r][c] = 'r'
                continue
            if x in green:
                logging.debug('Green found')
                sagaGrid[r][c] = 'g'
                continue
            if x in purple:
                logging.debug('Purple found')
                sagaGrid[r][c] = 'p'
                continue
            if x in yellow:
                logging.debug('Yellow found')
                sagaGrid[r][c] = 'y'
                continue
            if x in white:
                logging.debug('White found')
                sagaGrid[r][c] = 'w'
                continue
            if x == (0, 0, 0):
                logging.debug('Black found')
                sagaGrid[r][c] = 'k'
                continue
            else:
                logging.debug('Color not in list found...')
                time.sleep(0.5)
                colorConfirmer(r, c)
    logging.debug('Colors have been collected and placed in sagaGrid')
    logging.debug('\n' + (pformat(sagaGrid)))
    checkColor()
    return sagaGrid

def checkColor():
    # checks the colors from the grid to determine if game over or continue
    global sagaGrid
    # if grid has no black, return game grid
    if not any('k' in s1 for s1 in sagaGrid):
        logging.info('Color check passed.')
        return sagaGrid
    # if grid has black and other colors, is currently filling up, redo colors
    if any('k' in s1 for s1 in sagaGrid) and confirmShortcut() == True:
        logging.info('Black & other colors detected, redo colors')
        getColor()
    # if grid is black and has no color, check for a game over screen.
    if any('k' in s1 for s1 in sagaGrid) and confirmShortcut() == False:
        logging.info('Color check returned all black no color')
        checkGameOver()

def checkGameOver():
    # checks when getColor() returns all black pixels, to see if game over
    # if no Game Over, then runs getColor again.
    global GAME_REGION
    global gameOver
    logging.debug('All black detected, checking for Game Over screen...')
    gameOver = pyautogui.locateCenterOnScreen((r'images\GameOver.png'), region=GAME_REGION)
    if gameOver is not None:
        logging.debug('Game Over screen found')
        tryAgain = pyautogui.locateCenterOnScreen((r'images\TryAgain.png'), region=GAME_REGION)
        print('Game Over! Press Enter to try again. Or press CTRL-C to quit.')
        input()
        pyautogui.click(tryAgain, duration=0.25)
        pyautogui.moveTo(GAME_REGION[0], GAME_REGION[1], duration = 0.25)
        main()
    if gameOver is None:
        logging.debug('Not game over, leaving checkGameOver.')
        getColor()

def matchGrid(sagaGrid, x, y, oldChar, newChar):
    # main flood recursion loop, adds +1 to connection count every iteration
    # and returns value when recursion finishes. Every node traveled is
    # replaced with an empty value, which as the function travels through
    # every x,y coordinate, gets skipped in future calls.
    global connections
    gridWidth = len(sagaGrid[0])
    gridHeight = len(sagaGrid)
    if oldChar == None:
        oldChar = sagaGrid[x][y]
    # base cases, if color at x,y coordinate is different then color that called
    # the recursion, or if value is '' due to previous recursion call, skips.
    if sagaGrid[x][y] == '':
        return
    if sagaGrid[x][y] != oldChar:
        return
    # sets current x,y coordinate to newChar ('', in this case).
    sagaGrid[x][y] = newChar
    connections += 1
    # LEFT
    if x > 0: # left
        matchGrid(sagaGrid, x-1, y, oldChar, newChar)
    # UPLEFT
    if x > 0 and y > 0:
        matchGrid(sagaGrid, x-1, y-1, oldChar, newChar)
    # UP
    if y > 0: # up
        matchGrid(sagaGrid, x, y-1, oldChar, newChar)
    # UPRIGHT
    if x < gridHeight-1 and y > 0:
        matchGrid(sagaGrid, x+1, y-1, oldChar, newChar)
    # RIGHT
    if x < gridHeight-1:
        matchGrid(sagaGrid, x+1, y, oldChar, newChar)
    # DOWNRIGHT
    if x < gridHeight-1 and y < gridWidth-1:
        matchGrid(sagaGrid, x+1, y+1, oldChar, newChar)
    # DOWN
    if y < gridWidth-1:
        matchGrid(sagaGrid, x, y+1, oldChar, newChar)
    # DOWNLEFT
    if x > 0 and y <gridWidth-1:
        matchGrid(sagaGrid, x-1, y+1, oldChar, newChar)
    logging.debug(f"Recursion for grid position ({x},{y}) finished."
                  f"\nColor is {oldChar}. \nReturned {connections} connections.")
    return  connections

def gameLoop():
    # main game loop.
    while True:
        getColor()
        maxCoordinate = {'CLICK_HERE': 0,
                         'MAX_CONNECTIONS': 0}
        for x in range(len(sagaGrid)):
            for y in range(len(sagaGrid[0])):
                connections = 0
                matchGrid(sagaGrid, x, y, None, '')
                if connections > maxCoordinate['MAX_CONNECTIONS']:
                    maxCoordinate['CLICK_HERE'] = (x, y)
                    maxCoordinate['MAX_CONNECTIONS'] = connections
        logging.info(f"Clicking coordinates {maxCoordinate['CLICK_HERE']} "
                     f"with {maxCoordinate['MAX_CONNECTIONS']} connections.")
        pyautogui.click(CLICK_COORDS[maxCoordinate['CLICK_HERE']], duration=0.5)
        # Need to move mouse cursor after clicking or else color grabbed after is wrong.
        pyautogui.moveTo(GAME_REGION[0]+50, GAME_REGION[1]+150, duration = 0.25)

def main():
    createGrid()
    getGameRegion()
    getPastGameMenu()
    setupCoordinates()
    gameLoop()

if __name__ == '__main__':
    main()

