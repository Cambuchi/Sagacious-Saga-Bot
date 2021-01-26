# Sagacious Saga Bot
A python script to automatically play Sagacious Saga (Found at: https://www.newgrounds.com/portal/view/635494) using floodfill recursion strategy.
Dependant on pyautogui for color retrieval and screen checking for game region, buttons, and game over prompts.
Make sure you have the game open and visible in a browser at 100% zoom.

Note: game is bugged and the top two rows are unclickable, so program behaves as if the game grid is only 8 rows tall.

Here is the script in action. Note that pyautogui is slow at retrieving all of the colors. So improvement in speed can be achieved with buffering.

![](Example.gif)
