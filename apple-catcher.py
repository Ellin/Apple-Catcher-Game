from psychopy import event, gui, visual

# Get participant's name, age, gender via a dialog box
participantDlg = gui.Dlg()
participantDlg.addField('Name:')
participantDlg.addField('Age:')
participantDlg.addField('Gender:', choices = ['Female', 'Male', 'Other'])
participantDlg.addField('Condition:')
participantDlg.show()

# Generate window
win = visual.Window(fullscr = True, units = 'norm')

# Get window width and height (units = pixels)
winX = win.size[0]
winY = win.size[1]

# Window edges (units = norm)
topWinEdge = 1
bottomWinEdge = -1
leftWinEdge = -1
rightWinEdge = 1
windowHeight = 2

# Specify game play area (units = norm)
topGameAreaEdge = topWinEdge
bottomGameAreaEdge = bottomWinEdge + (windowHeight/float(8)) # The bottom of the game play area is 1/8 from the bottom of the window
leftGameAreaEdge = leftWinEdge
rightGameAreaEdge = rightWinEdge
gameAreaHeight = abs(topGameAreaEdge - bottomGameAreaEdge)
gameAreaWidth = abs(leftGameAreaEdge - rightGameAreaEdge)
gameAreaPosX = rightGameAreaEdge - gameAreaWidth/2.0

# Background image parameters environment
bkgimg = 'mtn.jpg'
bkgPosX = leftGameAreaEdge + gameAreaWidth/2.0
bkgPosY = topGameAreaEdge - gameAreaHeight/2.0
bkg = visual.ImageStim(win, image = bkgimg, size = (gameAreaWidth, gameAreaHeight), pos = (bkgPosX, bkgPosY), opacity = 1)
#bkg.autoDraw = True

# Basket parameters (norm units)
basketWidth = 0.1
basketHeight = 0.08
basketImg = 'opal.png'
basket = visual.ImageStim(win, image = basketImg, size = (basketWidth, basketHeight))
basketPosX = gameAreaPosX # Basket starts at the center of the game area
basketPosY = bottomGameAreaEdge + basketHeight/2.0 # The vertical position of the basket is fixed

# Apple image parameters (norm units)
appleWidth = 0.1
appleHeight = appleWidth
appleImg = 'rock.png'
apple = visual.ImageStim(win, image = appleImg, size = (appleWidth, appleHeight))
applePosX = 0 # TEMP INITIAL STARTING POS

# Apple animation settings 
appleDropInterval = 60 # Apple drops every 60 frames. I.e. Apple drops every second on monitors with a refresh rate of 60Hz.
appleDropSpeed = 20
appleDecrement = 0.01
appleStartPosX = 0
appleStartPosY = topGameAreaEdge + appleHeight/2
applePosX = 0
applePosY = 1.025

# Other game variables
score = 0 # +1 point for every apple caught
gamePaused = 1

# Score display
scoreDisplay = visual.TextStim(win, text = 'Score: ' + str(score), color = "white", height = 0.1, pos = (0,-0.85))

# Condition 1
## Condition 1 can change difficulty levels at any time
## Track difficulty level changes after every pause-start

# Condition 2
## Condition 2 can set difficulty level once at the beginning

# Condition 3
## Condition 3 is yoked to condition 1

# Pause button (relevant only to condition 1)
## if paused, stop basket/apple animations

# Start button (relevant only to condition 1)
## if condition 1,
# Change difficulty level (i.e. speed of falling apples)

def getBasketEdges():
	basketTopEdge = basketPosY + basketHeight/2.0
	basketBottomEdge = basketPosY - basketHeight/2.0
	basketLeftEdge = basketPosX - basketWidth/2.0
 	basketRightEdge = basketPosX + basketWidth/2.0
	return {'top': basketTopEdge, 'bottom': basketBottomEdge, 'left': basketLeftEdge, 'right': basketRightEdge}

def getAppleEdges():
	appleTopEdge = applePosY + appleHeight/2.0
	appleBottomEdge = applePosY - appleHeight/2.0
	appleLeftEdge = applePosX - appleWidth/2.0
	appleRightEdge = applePosX + appleWidth/2.0
	return {'top': appleTopEdge, 'bottom': appleBottomEdge, 'left': appleLeftEdge, 'right': appleRightEdge}

# Drag basket
## instead of click and estimate, you're able to slide the basket around actively as the apples fall?
## set basket x position to the mouse x position (don't change the y coordinates)
def moveBasket():
    mouse = event.Mouse()
    mousePos = mouse.getPos()
    global basketPosX # NEEDED or else the next line doesn't update basketPosX on a global level
    basketPosX = mousePos[0] # Move basket with horizontal mouse movement

    # Restrict basket within the game area
    basketEdges = getBasketEdges()
    if basketEdges['left'] <= leftGameAreaEdge:
    	basketPosX = leftGameAreaEdge + basketWidth/2
    elif basketEdges['right'] >= rightGameAreaEdge:
    	basketPosX = rightGameAreaEdge - basketWidth/2

    basket.setPos([basketPosX, basketPosY])
    basket.draw()

# Animate apples falling
## while applesLeft > 0 & game not paused...
## apples always start falling every x seconds or x frames?
def dropApple():
	global applePosY
	appleEdges = getAppleEdges()
	appleCaught = isAppleCaught()
	if appleCaught:
		applePosY = appleStartPosY # Reset apple
	elif appleEdges['bottom'] > bottomGameAreaEdge: # If apple is still falling...
		applePosY -= appleDecrement
		apple.setPos([applePosX, applePosY])
		apple.draw()
	else: # If the apple hit the ground...
		applePosY = appleStartPosY # Reset apple

# Specify when apples are caught
def isAppleCaught():
 	global score
 	basketEdges = getBasketEdges()
 	appleEdges = getAppleEdges()
 	if (appleEdges['bottom'] <= basketEdges['top']) & (appleEdges['bottom'] >= basketEdges['bottom']) & (appleEdges['left'] <= basketEdges['right']) & (appleEdges['right'] >= basketEdges['left']):
 		appleCaught = True
 		score += 1
 		scoreDisplay.setText('Score: ' + str(score))
	else:
		appleCaught = False
	return appleCaught

## if the apple's coordinates overlap with the basket coordinates...

# Display score



# Write data to file

while not event.getKeys(keyList = ['q','space']):
	bkg.draw()
	moveBasket()
	#apple.setPos([applePosX, applePosY])
	#apple.draw()
	dropApple()
	scoreDisplay.draw()
	win.flip()

