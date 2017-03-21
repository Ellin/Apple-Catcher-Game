from psychopy import core, event, gui, visual
import pylab
import button, random


# Get participant's name, age, gender via a dialog box
participantDlg = gui.Dlg()
participantDlg.addField('ID:')
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Gender:', choices = ['Female', 'Male', 'Other'])
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Handedness:', choices = ['Left', 'Right'])
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Experimenter Code:')
participantDlg.addText('                                                                                                               ')
participantDlg.show()

condition = int(participantDlg.data[3])

# Generate window
win = visual.Window(fullscr = True, color = 'white', units = 'norm')

# Get frame rate
frameRate = win.getActualFrameRate()

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

# Timing (Unit = seconds)
gamePlayLength = 120 # Play time (excluding pauses) should max out at 10 minutes
dropIntervalClock = core.Clock()
pauseClock = core.Clock()

# Instruction screen
instructionsDict = {1: 'Condition 1 instructions here', 2: 'Condition 2 instructions here', 3: 'Condition 3 instructions here'}
instructions = visual.TextStim(win, text = instructionsDict[condition], color = 'black', height = 0.08)
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
optionsBox = visual.Rect(win, fillColor = 'grey', width = optionsBoxWidth, height = optionsBoxHeight, pos = (optionsBoxPosX, optionsBoxPosY))

# Background image parameters environment
bkgimg = 'mtn.jpg'
bkgPosX = leftGameAreaEdge + gameAreaWidth/2.0
bkgPosY = topGameAreaEdge - gameAreaHeight/2.0
bkg = visual.ImageStim(win, image = bkgimg, size = (gameAreaWidth, gameAreaHeight), pos = (bkgPosX, bkgPosY), opacity = 1)
bkgPauseOverlay = visual.Rect(win, fillColor = 'white', width = gameAreaWidth, height = gameAreaHeight, pos = (bkgPosX, bkgPosY), opacity = 0)

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

# Apple animation settings 
dropIntervalLength = 1 # Unit = seconds. Time (excluding pauses) between apple drops from when last apple hit the ground to when the next apple drops
# easiest = 4, easier = 3, easier = 2, middle = 1, harder = 0.5 harder = 0.25, hardest = 0
appleDropTime = 2 # Unit = seconds. The time it takes for an apple to hit the ground.
# easiest = 8, easier = 6, easier = 4, middle = 2, harder = 1, harder = 0.5, hardest = 0.25
difficultyLevel = 4
difficultyDict = {1: {'interval': 4, 'drop time': 8}, 2: {'interval': 3, 'drop time': 6}, 3: {'interval': 2, 'drop time': 4}, 4: {'interval': 1, 'drop time': 2}, 5: {'interval': 0.5, 'drop time': 1}, 6: {'interval': 0.25, 'drop time': 0.5}, 7: {'interval': 0, 'drop time': 0.25}}
appleDecrement = gameAreaHeight/(frameRate*appleDropTime) # The decrement is how much down the screen the apple should drop per frame
appleStartPosX = random.uniform(leftGameAreaEdge + appleWidth/2.0, rightGameAreaEdge - appleWidth/2.0)
appleStartPosY = topGameAreaEdge + appleHeight/2
applePosX = appleStartPosX
applePosY = appleStartPosY

# Other game variables
score = 0 # +1 point for every apple caught
gamePaused = 0

# Score display
scoreDisplay = visual.TextStim(win, text = 'Score: ' + str(score), color = 'white', height = 0.1, pos = (0, optionsBoxPosY))

# Pause button (CONDITION 1 ONLY)
pauseButtonBoxPosX = -0.75
pauseButtonBoxPosY = optionsBoxPosY
pauseButtonBox = visual.Rect(win, fillColor ='darkgrey', width = 0.3, height = 0.15, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
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
	instructions.draw()
	startButtonBox.draw()
	startButtonText.draw()

# Difficulty scale
# parameters: scale colour, height, width, number of ticks, position, opacity, orientation?
difficultyScale = button.Scale(win, scaleColor = 'white', activeColor = 'red', startLevel = 4, width = 0.5, height = 0.05, pos = (0.6, optionsBoxPosY), opacity = 0.3)

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

def resetApple():
	global applePosX
	global applePosY
	dropIntervalClock.reset()
	applePosY = appleStartPosY
	applePosX = random.uniform(leftGameAreaEdge + appleWidth/2.0, rightGameAreaEdge - appleWidth/2.0)
	while abs(applePosX - basketPosX) < basketWidth + appleWidth/2.0: # Make sure the new apple drops at least a basket width + half the apple's width away from the participant's basket to force the participant to move at least half a basket width to catch the next apple
		applePosX = random.uniform(leftGameAreaEdge + appleWidth/2.0, rightGameAreaEdge - appleWidth/2.0)
	apple.setPos([applePosX, applePosY])

# Animate apples falling
def dropApple():
	global score
	global applePosY
	appleEdges = getAppleEdges()
	appleCaught = isAppleCaught()
	if appleCaught:
		score += 1
		scoreDisplay.setText('Score: ' + str(score))
		resetApple()
	elif appleEdges['bottom'] - appleDecrement >= bottomGameAreaEdge: # If the apple bottom will stay above/on the ground with the next decrement, then continue to move the apple down
		applePosY -= appleDecrement
		apple.setPos([applePosX, applePosY])
	else: # If the apple hit the ground or would be going through the ground if decremented further, then reset apple
		resetApple()

# Specify when apples are caught
# (An apple is considered "caught" if the apple touches the basket and it hasn't touched the ground)
def isAppleCaught():
	basketEdges = getBasketEdges()
	appleEdges = getAppleEdges()

	if (appleEdges['left'] <= basketEdges['right']) & (appleEdges['right'] >= basketEdges['left']): # If the apple is in the same horizontal space (column) as the basket...
		if appleEdges['bottom'] - appleDecrement >= bottomGameAreaEdge: # If the apple bottom will stay above/on the ground with the next decrement, then check to see if apple is in the basket
			if (appleEdges['bottom'] <= basketEdges['top']) & (appleEdges['bottom'] > basketEdges['bottom']): 
				appleCaught = True
			else:
				appleCaught = False
		else:
			appleCaught = True # If the apple bottom will be going through the ground with the next decrement, then count as hit b/c it's currently above the basket (e.g. if the apple's decrement is larger than the basket, then it could skip over the basket in the next frame)
	else:
		appleCaught = False
	return appleCaught

def playGame():
	global gamePaused
	global applePosY
	global difficultyLevel
	global dropIntervalLength
	global appleDropTime
	global appleDecrement

	bkg.draw()
	optionsBox.draw()
	pauseButtonBox.draw()
	pauseButtonText.draw()
	difficultyScale.draw()
	if (not gamePaused):
		moveBasket()
		if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
			dropApple()
	elif difficultyScale.hasLevelChanged():
		difficultyLevel = difficultyScale.activeLevel
		dropIntervalLength = difficultyDict[difficultyLevel]['interval']
		appleDropTime = difficultyDict[difficultyLevel]['drop time']
		appleDecrement = gameAreaHeight/(frameRate*appleDropTime)
	apple.draw()
	basket.draw()
	bkgPauseOverlay.draw()
	scoreDisplay.draw()

	if pauseButton.isClicked():
		gamePaused = 1 - gamePaused # Flip pause status of game from 0 to 1 or vice versa
		if gamePaused:
			pauseGame()
		else:
			resumeGame()

def pauseGame():
	bkgPauseOverlay.opacity = 0.5
	difficultyScale.setOpacity(1)
	pauseButtonText.text = 'Resume'
	pauseClock.reset()

def resumeGame():
	gamePlayClock.add(pauseClock.getTime()) # This effectively subtracts the pause time from the game play time
	dropIntervalClock.add(pauseClock.getTime())
	bkgPauseOverlay.opacity = 0
	difficultyScale.setOpacity(0.5)
	pauseButtonText.text = 'Pause'


# START EXPERIMENT
#win.setRecordFrameIntervals(True)

while not startButton.isClicked():
	displayInstructions()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()
#practiseScreen()

resetApple() # Initialize apple
gamePlayClock = core.Clock() # Effectively starts the game play timer

while gamePlayClock.getTime() <= gamePlayLength or gamePaused: 
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	playGame()
	mouse.clickReset()
	win.flip()

win.close()

# pylab.plot(win.frameIntervals)
# pylab.show()
