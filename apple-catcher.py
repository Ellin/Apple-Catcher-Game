from psychopy import event, gui, visual
import button


# Get participant's name, age, gender via a dialog box
participantDlg = gui.Dlg()
participantDlg.addField('ID:')
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Gender:', choices = ['Female', 'Male', 'Other'])
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Experimenter Code:')
participantDlg.addText('                                                                                                               ')
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
startButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButtonText = visual.TextStim(win, text = 'start', color = 'black', height = 0.08, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButton = button.Button(startButtonBox, mouse)

# Specify game play area (units = norm)
gameAreaWidth = windowWidth
gameAreaHeight = windowHeight * (9.0/10.0) # The game play area is 9/10th the size of the window
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

# Difficulty scale
# parameters: scale colour, height, width, number of ticks, position, opacity, orientation?
scaleColor = 'white'
scaleWidth = 0.5 #changeable
scaleHeight = 0.05
scalePosX = 0.6 #changeable
scalePosY = optionsBoxPosY #changeable

barWidth = scaleWidth* 0.8
barPosX = scalePosX
barPosY = scalePosY
barLeftEdge = barPosX - barWidth/2.0
barRightEdge = barPosX + barWidth/2.0
bar = visual.Line(win, lineColor = scaleColor, start = (barLeftEdge, scalePosY), end = (barRightEdge, scalePosY))

scaleButtonWidth = scaleWidth * 0.1
leftButton = visual.Polygon(win, lineColor = scaleColor, fillColor = scaleColor, edges = 3, radius = scaleButtonWidth/2.0, pos = (barLeftEdge - scaleButtonWidth/2.0, barPosY), ori = -90)
rightButton = visual.Polygon(win, lineColor = scaleColor, fillColor = scaleColor, edges = 3, radius = scaleButtonWidth/2.0, pos = (barRightEdge + scaleButtonWidth/2.0, barPosY), ori = 90)

tickIntervalWidth = barWidth/6.0 # 7 ticks => 6 intervals
tickYStart = scalePosY - scaleHeight/2.0
tickYEnd = scalePosY + scaleHeight/2.0
tick1PosX = barLeftEdge
tick2PosX = barPosX - (2*tickIntervalWidth)
tick3PosX = barPosX - (1*tickIntervalWidth)
tick4PosX = barPosX
tick5PosX = barPosX + (1*tickIntervalWidth)
tick6PosX = barPosX + (2*tickIntervalWidth)
tick7PosX = barRightEdge
tick1 = visual.Line(win, lineColor = scaleColor, start = (tick1PosX, tickYStart), end = (tick1PosX, tickYEnd))
tick2 = visual.Line(win, lineColor = scaleColor, start = (tick2PosX, tickYStart), end = (tick2PosX, tickYEnd))
tick3 = visual.Line(win, lineColor = scaleColor, start = (tick3PosX, tickYStart), end = (tick3PosX, tickYEnd))
tick4 = visual.Line(win, lineColor = scaleColor, start = (tick4PosX, tickYStart), end = (tick4PosX, tickYEnd))
tick5 = visual.Line(win, lineColor = scaleColor, start = (tick5PosX, tickYStart), end = (tick5PosX, tickYEnd))
tick6 = visual.Line(win, lineColor = scaleColor, start = (tick6PosX, tickYStart), end = (tick6PosX, tickYEnd))
tick7 = visual.Line(win, lineColor = scaleColor, start = (tick7PosX, tickYStart), end = (tick7PosX, tickYEnd))

tickLabelPosY = barPosY - scaleHeight
tick1Label = visual.TextStim(win, text = '1', height = scaleHeight, color = scaleColor, pos = (tick1PosX, tickLabelPosY))
tick2Label = visual.TextStim(win, text = '2', height = scaleHeight, color = scaleColor, pos = (tick2PosX, tickLabelPosY))
tick3Label = visual.TextStim(win, text = '3', height = scaleHeight, color = scaleColor, pos = (tick3PosX, tickLabelPosY))
tick4Label = visual.TextStim(win, text = '4', height = scaleHeight, color = scaleColor, pos = (tick4PosX, tickLabelPosY))
tick5Label = visual.TextStim(win, text = '5', height = scaleHeight, color = scaleColor, pos = (tick5PosX, tickLabelPosY))
tick6Label = visual.TextStim(win, text = '6', height = scaleHeight, color = scaleColor, pos = (tick6PosX, tickLabelPosY))
tick7Label = visual.TextStim(win, text = '7', height = scaleHeight, color = scaleColor, pos = (tick7PosX, tickLabelPosY))

def displayDifficultyScale():
	leftButton.draw()
	rightButton.draw()
	bar.draw()
	tick1.draw()
	tick2.draw()
	tick3.draw()
	tick4.draw()
	tick5.draw()
	tick6.draw()
	tick7.draw()
	tick1Label.draw()
	tick2Label.draw()
	tick3Label.draw()
	tick4Label.draw()
	tick5Label.draw()
	tick6Label.draw()
	tick7Label.draw()

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

# Move basket to track the mouse (as long as mouse is not in the game options area)
def moveBasket():
    mousePos = mouse.getPos()
    global basketPosX
    if (not optionsBox.contains(mouse)):
    	basketPosX = mousePos[0] # Set basket's x position to the mouse's x position
    basketEdges = getBasketEdges()
    # Restrict basket within the game area
    if basketEdges['left'] <= leftGameAreaEdge:
    	basketPosX = leftGameAreaEdge + basketWidth/2.0
    elif basketEdges['right'] >= rightGameAreaEdge:
    	basketPosX = rightGameAreaEdge - basketWidth/2.0
    basket.setPos([basketPosX, basketPosY])

# Animate apples falling
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


while not event.getKeys(keyList = ['q','space']):
	if (not gameStarted):
		displayInstructions()

	else:
		bkg.draw()
		optionsBox.draw()
		pauseButtonBox.draw()
		pauseButtonText.draw()
		displayDifficultyScale()
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

