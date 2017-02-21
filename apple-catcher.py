from psychopy import event, gui, visual
import button

# Get participant's name, age, gender via a dialog box
participantDlg = gui.Dlg()
participantDlg.addField('Name:')
participantDlg.addField('Age:')
participantDlg.addField('Gender:', choices = ['Female', 'Male', 'Other'])
participantDlg.addField('Condition:')
participantDlg.show()

# Generate window
win = visual.Window(fullscr = True, color = "white", units = 'norm')

# Get window width and height (units = pixels)
winX = win.size[0]
winY = win.size[1]

# Window edges (units = norm)
topWinEdge = 1.0
bottomWinEdge = -1.0
leftWinEdge = -1.0
rightWinEdge = 1.0
windowWidth = 2.0
windowHeight = 2.0

# Get mouse
mouse = event.Mouse()

# Instruction screen
instructionsC1 = "Condition 1 instructions here"
instructionsC2 = "Condition 2 instructions here"
instructionsC3 = "Condition 3 instructions here"
instructions = visual.TextStim(win, text = instructionsC1, color = 'black', height = 0.08)
startButtonBoxPosX = 0
startButtonBoxPosY = -0.5
startButtonBox = visual.Rect(win, width = 0.3, height = 0.15, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButtonText = visual.TextStim(win, text = 'start', color = 'black', height = 0.08, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButton = button.Button(startButtonBox, mouse)

# Specify game play area (units = norm)
gameAreaWidth = windowWidth
gameAreaHeight = windowHeight * (7.0/8.0) # The game play area is 7/8th the size of the window
gameAreaPosX = 0
gameAreaPosY = (windowHeight - gameAreaHeight)/2.0
topGameAreaEdge = gameAreaPosY + gameAreaHeight/2.0
bottomGameAreaEdge = gameAreaPosY - gameAreaHeight/2.0
leftGameAreaEdge = gameAreaPosX - gameAreaWidth/2.0
rightGameAreaEdge = gameAreaPosX + gameAreaWidth/2.0

# Specify game options box
optionsBoxWidth = windowWidth
optionsBoxHeight = windowHeight - gameAreaHeight
optionsBoxPosX = 0
optionsBoxPosY = bottomGameAreaEdge - optionsBoxHeight/2.0
optionsBox = visual.Rect(win, fillColor = "grey", width = optionsBoxWidth, height = optionsBoxHeight, pos = (optionsBoxPosX, optionsBoxPosY))

# Background image parameters environment
bkgimg = 'mtn.jpg'
bkgPosX = leftGameAreaEdge + gameAreaWidth/2.0
bkgPosY = topGameAreaEdge - gameAreaHeight/2.0
bkg = visual.ImageStim(win, image = bkgimg, size = (gameAreaWidth, gameAreaHeight), pos = (bkgPosX, bkgPosY), opacity = 1)
bkgPauseOverlay = visual.Rect(win, fillColor = "white", width = gameAreaWidth, height = gameAreaHeight, pos = (bkgPosX, bkgPosY), opacity = 0)

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
gameStarted = 0
gamePaused = 0

# Score display
scoreDisplay = visual.TextStim(win, text = 'Score: ' + str(score), color = 'white', height = 0.1, pos = (0, optionsBoxPosY))

# Pause button (CONDITION 1 ONLY)
pauseButtonBoxPosX = -0.75
pauseButtonBoxPosY = optionsBoxPosY
pauseButtonBox = visual.Rect(win, fillColor ="darkgrey", width = 0.3, height = 0.15, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
pauseButtonText = visual.TextStim(win, text = 'Pause', color = 'white', height = 0.08, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
pauseButton = button.Button(pauseButtonBox, mouse)

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

# def pauseGame():
# 	global gamePaused
# 	while gamePaused:
# 		print 'paused'

def displayInstructions():
	global gameStarted
	instructions.draw()
	startButtonBox.draw()
	startButtonText.draw()
	if startButton.isClicked():
		gameStarted = 1

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
    mousePos = mouse.getPos()
    global basketPosX # NEEDED or else the next line doesn't update basketPosX on a global level
    basketPosX = mousePos[0] # Move basket with horizontal mouse movement
    basketEdges = getBasketEdges()
    # Restrict basket within the game area
    if basketEdges['left'] <= leftGameAreaEdge:
    	basketPosX = leftGameAreaEdge + basketWidth/2
    elif basketEdges['right'] >= rightGameAreaEdge:
    	basketPosX = rightGameAreaEdge - basketWidth/2

    basket.setPos([basketPosX, basketPosY])

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
	else: # If the apple hit the ground...
		applePosY = appleStartPosY # Reset apple

# Specify when apples are caught
# (An apple is considered "caught" if the apple touches the basket and it hasn't touched the ground)
def isAppleCaught():
 	global score
 	basketEdges = getBasketEdges()
 	appleEdges = getAppleEdges()
 	if (appleEdges['bottom'] <= basketEdges['top']) & (appleEdges['bottom'] > basketEdges['bottom']) & (appleEdges['left'] <= basketEdges['right']) & (appleEdges['right'] >= basketEdges['left']):
 		appleCaught = True
 		score += 1
 		scoreDisplay.setText('Score: ' + str(score))
	else:
		appleCaught = False
	return appleCaught

# Write data to file
while not event.getKeys(keyList = ['q','space']):
	if (not gameStarted):
		displayInstructions()
	else:
		bkg.draw()
		optionsBox.draw()
		pauseButtonBox.draw()
		pauseButtonText.draw()
		if (not gamePaused):
			moveBasket()
			dropApple()
		basket.draw()
		apple.draw()
		bkgPauseOverlay.draw()
		scoreDisplay.draw()

		if pauseButton.isClicked():
			gamePaused = 1 - gamePaused # gamePaused is always 0 or 1
			if gamePaused:
				bkgPauseOverlay.opacity = 0.5
				pauseButtonText.text = 'Resume'
			else:
				bkgPauseOverlay.opacity = 0
				pauseButtonText.text = 'Pause'

	event.clearEvents()
	mouse.clickReset()
	win.flip()

