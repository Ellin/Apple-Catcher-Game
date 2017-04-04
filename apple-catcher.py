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
frameRate = win.getActualFrameRate() # Note: 59.9474475876 = buggy animation

# Window edges (units = norm)
topWinEdge = 1.0
bottomWinEdge = -1.0
leftWinEdge = -1.0
rightWinEdge = 1.0
windowWidth = 2.0
windowHeight = 2.0

# Get mouse
mouse = event.Mouse()

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

# CONDITION SPECIFIC INITIALIZATIONS
if condition == 1:
	instructionsText = 'Condition 1 instructions: In the actual game, you will be able to change the difficulty level at any time to suit your preference by pressing the pause button to activate the difficulty scale in the bottom right corner. If you want the game to be more difficult, press the right arrow button. If you want the game to be less difficult, press the left arrow button. Press start when you are ready to play.'
	startButtonBoxPosX = 0
	startButtonBoxPosY = -0.5
	difficultyScale = button.Scale(win, scaleColor = 'white', activeColor = 'red', startLevel = 4, width = 0.5, height = 0.05, pos = (0.6, optionsBoxPosY), opacity = 0.3)
	# Pause button
	pauseButtonBoxPosX = -0.75
	pauseButtonBoxPosY = optionsBoxPosY
	pauseButtonBox = visual.Rect(win, fillColor ='darkgrey', width = 0.3, height = 0.15, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
	pauseButtonText = visual.TextStim(win, text = 'Pause', color = 'white', height = 0.08, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
	pauseButton = button.Button(pauseButtonBox, mouse)

elif condition == 2:
	instructionsText = 'Condition 2 instructions: Before you start the game, choose how difficult you want the game to be using the scale below. The practise was set at a difficulty of level 4. If you want the game to be more difficult, press the right arrow button. If you want the game to be less difficult, press the left arrow button. You will not be able to change the difficulty of the game once you start. Press start when you are ready to play.'
	difficultyScale = button.Scale(win, scaleColor = 'black', activeColor = 'red', startLevel = 4, width = 0.5, height = 0.05, pos = (0, -0.5))
	startButtonBoxPosX = 0
	startButtonBoxPosY = -0.75
elif condition == 3:
	instructionsText = 'Condition 3 instructions: In the actual game, the difficulty of the game (how quickly the apples drop) may change as you play. Press start when you are ready to play.'
	startButtonBoxPosX = 0
	startButtonBoxPosY = -0.5

# Timing (Unit = seconds)
practisePlayLength = 15 # Practise lasts 15 seconds
gamePlayLength = 5*60 # Play time (excluding pauses) should max out at 10 minutes
dropIntervalClock = core.Clock()
pauseClock = core.Clock()

#Practise Instruction Screen
practiseInstructions = visual.TextStim(win, wrapWidth = 2, text = "Try to catch as many apples as you can by dragging the basket. Press next to practise doing this.", color = 'black', height = 0.08)
practiseButtonBoxPosX = 0
practiseButtonBoxPosY = -0.5
practiseButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (practiseButtonBoxPosX, practiseButtonBoxPosY))
practiseButtonText = visual.TextStim(win, text = 'Next', color = 'black', height = 0.08, pos = (practiseButtonBoxPosX, practiseButtonBoxPosY))
practiseButton = button.Button(practiseButtonBox, mouse)

# Instruction screen
instructions = visual.TextStim(win, wrapWidth = 2, text = instructionsText, color = 'black', height = 0.08)
startButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButtonText = visual.TextStim(win, text = 'start', color = 'black', height = 0.08, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButton = button.Button(startButtonBox, mouse)

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
difficultyLevel = 4 # Initial setting
difficultyDict = {
	1: {'interval': 4, 'drop time': 8}, 
	2: {'interval': 3, 'drop time': 6}, 
	3: {'interval': 2, 'drop time': 4}, 
	4: {'interval': 1, 'drop time': 2}, 
	5: {'interval': 0.5, 'drop time': 1}, 
	6: {'interval': 0.25, 'drop time': 0.5}, 
	7: {'interval': 0, 'drop time': 0.25}}
dropIntervalLength = difficultyDict[difficultyLevel]['interval'] # Unit = seconds. Time (excluding pauses) between apple drops from when last apple hit the ground to when the next apple drops
# easiest = 4, easier = 3, easier = 2, middle = 1, harder = 0.5 harder = 0.25, hardest = 0
appleDropTime = difficultyDict[difficultyLevel]['drop time'] # Unit = seconds. The time it takes for an apple to hit the ground.
# easiest = 8, easier = 6, easier = 4, middle = 2, harder = 1, harder = 0.5, hardest = 0.25

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


# Condition 1
## Condition 1 can change difficulty levels at any time
## Track difficulty level changes after every pause-start

# Condition 2
## Condition 2 can set difficulty level once at the beginning

# Condition 3
## Condition 3 is yoked to condition 1


def displayInstructions():
	global difficultyLevel
	global dropIntervalLength
	global appleDropTime
	global appleDecrement
	instructions.draw()
	if condition == 2:
		if difficultyScale.hasLevelChanged():
			difficultyLevel = difficultyScale.activeLevel
			dropIntervalLength = difficultyDict[difficultyLevel]['interval']
			appleDropTime = difficultyDict[difficultyLevel]['drop time']
			appleDecrement = gameAreaHeight/(frameRate*appleDropTime)
		difficultyScale.draw()
	startButtonBox.draw()
	startButtonText.draw()

def displayPractiseScreen():
	practiseInstructions.draw()
	practiseButtonBox.draw()
	practiseButtonText.draw()

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

def decrementApple():
	global applePosY
	applePosY -= appleDecrement
	apple.setPos([applePosX, applePosY])

def isAppleCaught():
	basketEdges = getBasketEdges()
	appleEdges = getAppleEdges()
	if (appleEdges['left'] <= basketEdges['right']) & (appleEdges['right'] >= basketEdges['left']) & (appleEdges['bottom'] <= basketEdges['top']): # If the apple is overlapping the same horizontal space (column) as the basket... & If the apple's bottom is touching or is below the top of the basket...  if the apple's decrement is larger than the basket, then it could skip over the basket and end up under the basket
		return True
	else:
		return False

def isAppleTouchingGround():
	appleEdges = getAppleEdges()
	if appleEdges['bottom'] <= bottomGameAreaEdge:
		return True
	else:
		return False

# Animate apples falling
def updateApple():
# Update apple position:
# if apple is currently touching the basket or touching the ground or will be fully past the ground with another decrement (i.e. appleposy will be below game bottom -  appleheight/2.0 so that apple will not be visible), then reset apple
# else: decrement apple.
	if isAppleCaught() or isAppleTouchingGround():
		resetApple()
	else:
		decrementApple()

def updateScore():
	global score
	if isAppleCaught():
		score += 1
		scoreDisplay.setText('Score: ' + str(score))

def playCond1():
	global gamePaused
	global applePosY
	global difficultyLevel
	global dropIntervalLength
	global appleDropTime
	global appleDecrement

	bkg.draw()
	if (not gamePaused):
		moveBasket()
		if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
			updateApple()
			updateScore()
	elif difficultyScale.hasLevelChanged():
		difficultyLevel = difficultyScale.activeLevel
		dropIntervalLength = difficultyDict[difficultyLevel]['interval']
		appleDropTime = difficultyDict[difficultyLevel]['drop time']
		appleDecrement = gameAreaHeight/(frameRate*appleDropTime)
	apple.draw()
	basket.draw()
	optionsBox.draw()
	pauseButtonBox.draw()
	pauseButtonText.draw()
	difficultyScale.draw()
	bkgPauseOverlay.draw()
	scoreDisplay.draw()

	if pauseButton.isClicked():
		gamePaused = 1 - gamePaused # Flip pause status of game from 0 to 1 or vice versa
		if gamePaused:
			pauseGame()
		else:
			resumeGame()

def playCond2():
	bkg.draw()
	moveBasket()
	if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
		updateApple()
		updateScore()
	apple.draw()
	basket.draw()
	optionsBox.draw()
	scoreDisplay.draw()


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

def playPractise():
	bkg.draw()
	moveBasket()
	if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
		updateApple()
		updateScore()
	apple.draw()
	basket.draw()
	optionsBox.draw()
	scoreDisplay.draw()


# START EXPERIMENT
#win.setRecordFrameIntervals(True)


# while not practiseButton.isClicked():
# 	displayPractiseScreen()
# 	if event.getKeys(keyList = ['q','escape']):
# 		core.quit()
# 	mouse.clickReset()
# 	win.flip()

# resetApple() # Initialize apple
# gamePlayClock = core.Clock() # Effectively starts the game play timer
# while gamePlayClock.getTime() <= practisePlayLength: 
# 	if event.getKeys(keyList = ['q','escape']):
# 		core.quit()
# 	playPractise()
# 	mouse.clickReset()
# 	win.flip()

while not startButton.isClicked():
	displayInstructions()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

score = 0
scoreDisplay.setText('Score: ' + str(score))
resetApple() # Initialize apple
gamePlayClock = core.Clock() # Effectively starts the game play timer

if condition == 1:
	while gamePlayClock.getTime() <= gamePlayLength or gamePaused: 
		if event.getKeys(keyList = ['q','escape']):
			core.quit()
		playCond1()
		mouse.clickReset()
		win.flip()
elif condition == 2:
	while gamePlayClock.getTime() <= gamePlayLength or gamePaused: 
		if event.getKeys(keyList = ['q','escape']):
			core.quit()
		playCond2()
		mouse.clickReset()
		win.flip()
elif condition == 3:
	pass

win.close()

# pylab.plot(win.frameIntervals)
# pylab.show()
