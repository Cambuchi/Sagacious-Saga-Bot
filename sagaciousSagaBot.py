#! python3
# sagaciousSagaBot.py - bot that plays sagacious saga using floodfill
# recursion.

import pyautogui
import logging
import time
from pprint import pformat

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
logging.disable(logging.DEBUG) # un/comment to un/block debug log messages
#logging.disable(logging.INFO) # un/comment to un/block info log messages

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
    region = pyautogui.locateOnScreen('UpLeftCorner.png')
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
        pos = pyautogui.locateCenterOnScreen(('HowToPlay.png'), region=GAME_REGION)
        if pos is not None:
            break
    pyautogui.click(pos, duration=0.25)
    logging.debug('Clicked on How To Play button.')

    # move mouse down to detect play button img accurately
    pyautogui.moveTo(GAME_REGION[0], GAME_REGION[1], duration = 0.25)

    # click on Play!
    logging.debug('Looking for Play button...')
    while True:
        pos2 = pyautogui.locateCenterOnScreen(('Play.png'), region=GAME_REGION)
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
    initialRight = 120
    initialTop = 50 + 59

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

def getColor():
    logging.debug('Putting colors from screen coordinates into game grid...')
    global sagaGrid
    for r in range(len(sagaGrid)):
        for c in range(len(sagaGrid[0])):
            sagaGrid[r][c] = pyautogui.pixel(CLICK_COORDS[r, c][0],
                                             CLICK_COORDS[r, c][1])
    logging.debug('Colors have been collected and placed in sagaGrid')
    logging.debug('\n' + (pformat(sagaGrid)))
    return sagaGrid

def checkColor():
    # checks the colors from the grid to determine what to do
    global sagaGrid
    if not any((0, 0, 0) in s1 for s1 in sagaGrid):
        return sagaGrid
    # game always has blue, so if detects black & blue, delays for board to fill
    while any((0, 0, 0) in s1 for s1 in sagaGrid) and any((67,192,241) in s1 for s1 in sagaGrid):
        logging.info('Black & Blue detected, board fill pause started')
        time.sleep(0.25)
        getColor()
    # game always has blue, so detecting black and no blue is same as returning all black.
    if any((0, 0, 0) in s1 for s1 in sagaGrid) and not any((67,192,241) in s1 for s1 in sagaGrid):
        checkGameOver()

def checkGameOver():
    # checks when getColor() returns all black pixels, to see if game over
    # if no Game Over, then runs getColor again.
    global GAME_REGION
    global gameOver
    logging.debug('Black detected, checking for Game Over screen...')
    gameOver = pyautogui.locateCenterOnScreen(('GameOver.png'), region=GAME_REGION)
    if gameOver is not None:
        logging.debug('Game Over screen found')
        tryAgain = pyautogui.locateCenterOnScreen(('TryAgain.png'), region=GAME_REGION)
        print('Game Over! Press Enter to try again. Or press CTRL-C to quit.')
        input()
        pyautogui.click(tryAgain, duration=0.25)
        pyautogui.moveTo(GAME_REGION[0], GAME_REGION[1], duration = 0.25)
        main()
    if gameOver is None:
        logging.debug('Not game over, leaving checkGameOver.')
        return getColor()

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
    global connections
    while True:
        getColor()
        checkColor()
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
        pyautogui.click(CLICK_COORDS[maxCoordinate['CLICK_HERE']], duration=0.25)
        # Need to move mouse cursor after clicking or else color grabbed after is wrong.
        pyautogui.moveTo(GAME_REGION[0]+50, GAME_REGION[1]+100, duration = 0.25)
        time.sleep(0.5)

def main():
    createGrid()
    getGameRegion()
    getPastGameMenu()
    setupCoordinates()
    gameLoop()

if __name__ == '__main__':
    main()

