from psychopy import core, event, gui, visual
import os, csv, random
import pylab
import tools

# Condition 1: Can pause to change difficulty levels at any time
# Condition 2: Can set difficulty level once at the beginning
# Condition 3: Difficulty level changes are yoked to condition 1

# Get participant's name, age, gender via a dialog box
participantDlg = gui.Dlg()
participantDlg.addField('ID:')
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Gender:', choices = ['Female', 'Male', 'Other'])
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Handedness:', choices = ['Right', 'Left'])
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Condition:')
participantDlg.addText('                                                                                                               ')
participantDlg.addField('Version:', 0)
participantDlg.addText('                                                                                                               ')
participantDlg.show()

participantID = participantDlg.data[0]
gender = participantDlg.data[1]
handedness = participantDlg.data[2]
condition = int(participantDlg.data[3])
yokeID = int(participantDlg.data[4]) # The participant ID that the game is yoked to (relevant only for condition 2)
participantDataDict = {'ID': participantID, 'Gender': gender, 'Handedness': handedness, 'Condition': condition}

# Generate window
win = visual.Window(fullscr = True, color = 'white', units = 'norm')

# Get frame rate
frameRate = 60

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
	levelChangeLog = []
	difficultyScale = tools.Scale(win, scaleColor = 'white', activeColor = 'red', startLevel = 4, width = 0.5, height = 0.05, pos = (0.6, optionsBoxPosY), opacity = 0.3)
	# Pause button
	pauseButtonBoxPosX = -0.75
	pauseButtonBoxPosY = optionsBoxPosY
	pauseButtonBox = visual.Rect(win, fillColor ='darkgrey', width = 0.3, height = 0.15, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
	pauseButtonText = visual.TextStim(win, text = 'Pause', color = 'white', height = 0.08, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
	pauseButton = tools.Button(pauseButtonBox, mouse)

elif condition == 2:
	instructionsText = 'Condition 2 instructions: Before you start the game, choose how difficult you want the game to be using the scale below. The practise was set at a difficulty of level 4. If you want the game to be more difficult, press the right arrow button. If you want the game to be less difficult, press the left arrow button. You will not be able to change the difficulty of the game once you start. Press start when you are ready to play.'
	difficultyScale = tools.Scale(win, scaleColor = 'black', activeColor = 'red', startLevel = 4, width = 0.5, height = 0.05, pos = (0, -0.5))
	startButtonBoxPosX = 0
	startButtonBoxPosY = -0.75
elif condition == 3:
	instructionsText = 'Condition 3 instructions: In the actual game, the difficulty of the game (how quickly the apples drop) may change as you play. Press start when you are ready to play.'
	startButtonBoxPosX = 0
	startButtonBoxPosY = -0.5
	levelChangeLog = []
	i = 0 # Index for level change log

# Timing (Unit = seconds)
practisePlayLength = 2 # Practise lasts 15 seconds
gamePlayLength = 5 # Play time (excluding pauses) should max out at 10 minutes
dropIntervalClock = core.Clock()
pauseClock = core.Clock()

#Practise Instruction Screen
practiseInstructions = visual.TextStim(win, wrapWidth = 2, text = "Try to catch as many apples as you can by dragging the basket. Press next to practise doing this.", color = 'black', height = 0.08)
practiseButtonBoxPosX = 0
practiseButtonBoxPosY = -0.5
practiseButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (practiseButtonBoxPosX, practiseButtonBoxPosY))
practiseButtonText = visual.TextStim(win, text = 'Next', color = 'black', height = 0.08, pos = (practiseButtonBoxPosX, practiseButtonBoxPosY))
practiseButton = tools.Button(practiseButtonBox, mouse)

# Instruction screen
instructions = visual.TextStim(win, wrapWidth = 2, text = instructionsText, color = 'black', height = 0.08)
startButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButtonText = visual.TextStim(win, text = 'start', color = 'black', height = 0.08, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButton = tools.Button(startButtonBox, mouse)

# End Screen
endText = visual.TextStim(win, wrapWidth = 2, text = 'This is the end of the study. Please get the experimenter.', color = 'black', height = 0.08)

# Probe Instruction Screen
probeInstructions = visual.TextStim(win, wrapWidth = 1.8, text = 'We now have a couple questions about your experience of this study. On the following screen, you will see the questions with rating scales next to them. To adjust your answer, use the left or right arrow buttons.', color = 'black', height = 0.08, pos = (0, 0.5))
probeStartButtonBoxPosX = 0
probeStartButtonBoxPosY = 0
probeStartButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (probeStartButtonBoxPosX, probeStartButtonBoxPosY))
probeStartButtonText = visual.TextStim(win, text = 'Next', color = 'black', height = 0.08, pos = (probeStartButtonBoxPosX, probeStartButtonBoxPosY))
probeStartButton = tools.Button(probeStartButtonBox, mouse)


# Probe Screen
q1 = visual.TextStim(win, alignHoriz = 'left', text = 'How bored were you during this study?', color = 'black', height = 0.08, pos = (-0.9, 0.8))
q2 = visual.TextStim(win, alignHoriz = 'left', text = 'How frustrated were you during this study?', color = 'black', height = 0.08, pos = (-0.9, 0.4))
q3 = visual.TextStim(win, alignHoriz = 'left', text = 'How motivated were you during this study?', color = 'black', height = 0.08, pos = (-0.9, 0))
q4 = visual.TextStim(win, alignHoriz = 'left', text = 'How challenging did you find this study?', color = 'black', height = 0.08, pos = (-0.9, -0.4))
q1Scale = tools.Scale(win, scaleColor = 'black', activeColor = 'red', startLevel = 4, width = 0.6, height = 0.06, pos = (0.5, 0.8))
q2Scale = tools.Scale(win, scaleColor = 'black', activeColor = 'red', startLevel = 4, width = 0.6, height = 0.06, pos = (0.5, 0.4))
q3Scale = tools.Scale(win, scaleColor = 'black', activeColor = 'red', startLevel = 4, width = 0.6, height = 0.06, pos = (0.5, 0))
q4Scale = tools.Scale(win, scaleColor = 'black', activeColor = 'red', startLevel = 4, width = 0.6, height = 0.06, pos = (0.5, -0.4))
q1Label1 = visual.TextStim(win, wrapWidth = 0.15, text = 'Not at all boring', color = 'black', height = 0.045, pos = (0.25, 0.65))
q1Label2 = visual.TextStim(win, wrapWidth = 0.15, text = 'Neutral', color = 'black', height = 0.045, pos = (0.5, 0.65))
q1Label3 = visual.TextStim(win, wrapWidth = 0.15, text = 'Extremely boring', color = 'black', height = 0.045, pos = (0.75, 0.65))
q2Label1 = visual.TextStim(win, wrapWidth = 0.15, text = 'Not at all frustrating', color = 'black', height = 0.045, pos = (0.25, 0.25))
q2Label2 = visual.TextStim(win, wrapWidth = 0.15, text = 'Neutral', color = 'black', height = 0.045, pos = (0.5, 0.25))
q2Label3 = visual.TextStim(win, wrapWidth = 0.15, text = 'Extremely frustrating', color = 'black', height = 0.045, pos = (0.75, 0.25))
q3Label1 = visual.TextStim(win, wrapWidth = 0.15, text = 'Not at all motivated', color = 'black', height = 0.045, pos = (0.25, -0.15))
q3Label2 = visual.TextStim(win, wrapWidth = 0.15, text = 'Neutral', color = 'black', height = 0.045, pos = (0.5, -0.15))
q3Label3 = visual.TextStim(win, wrapWidth = 0.15, text = 'Extremely motivated', color = 'black', height = 0.045, pos = (0.75, -0.15))
q4Label1 = visual.TextStim(win, wrapWidth = 0.15, text = 'Not at all challenging', color = 'black', height = 0.045, pos = (0.25, -0.55))
q4Label2 = visual.TextStim(win, wrapWidth = 0.15, text = 'Neutral', color = 'black', height = 0.045, pos = (0.5, -0.55))
q4Label3 = visual.TextStim(win, wrapWidth = 0.15, text = 'Extremely challenging', color = 'black', height = 0.045, pos = (0.75, -0.55))
q1Answer = 4
q2Answer = 4
q3Answer = 4
q4Answer = 4
probeSubmitButtonBoxPosX = 0
probeSubmitButtonBoxPosY = -0.8
probeSubmitButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (probeSubmitButtonBoxPosX, probeSubmitButtonBoxPosY))
probeSubmitButtonText = visual.TextStim(win, text = 'Submit', color = 'black', height = 0.08, pos = (probeSubmitButtonBoxPosX, probeSubmitButtonBoxPosY))
probeSubmitButton = tools.Button(probeSubmitButtonBox, mouse)

# Timer Textb
timerStim = visual.TextStim(win, text = "", color = 'white', height = 0.1, pos = (0, 0.9))

# Background image parameters environment
bkgimg = 'tree-bkg.png'
bkgPosX = leftGameAreaEdge + gameAreaWidth/2.0
bkgPosY = topGameAreaEdge - gameAreaHeight/2.0
bkg = visual.ImageStim(win, image = bkgimg, size = (gameAreaWidth, gameAreaHeight), pos = (bkgPosX, bkgPosY), opacity = 1)
bkgPauseOverlay = visual.Rect(win, fillColor = 'white', width = gameAreaWidth, height = gameAreaHeight, pos = (bkgPosX, bkgPosY), opacity = 0)

# Basket parameters (norm units)
basketWidth = 0.1
basketHeight = 0.08
basketImg = 'basket.png'
basket = visual.ImageStim(win, image = basketImg, size = (basketWidth, basketHeight))
basketPosX = gameAreaPosX # Basket starts at the center of the game area
basketPosY = bottomGameAreaEdge + basketHeight/2.0 # The vertical position of the basket is fixed

# Apple image parameters (norm units)
appleWidth = 0.05
appleHeight = 0.1
appleImg = 'apple.png'
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

def displayEndScreen():
	while True:
		if event.getKeys(keyList = ['q','escape']):
			core.quit()
		endText.draw()
		win.flip()

def updateTimerText():
	global timerStim
	time = gamePlayClock.getTime()
	minutes = int(time/60)
	seconds = int(time)%60
	timerText = str(minutes).zfill(2) + ':' + str(seconds).zfill(2) # create a string of characters representing the time
	timerStim.text = timerText

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
		updateTimerText()
	elif difficultyScale.hasLevelChanged():
		difficultyLevel = difficultyScale.activeLevel
		dropIntervalLength = difficultyDict[difficultyLevel]['interval']
		appleDropTime = difficultyDict[difficultyLevel]['drop time']
		appleDecrement = gameAreaHeight/(frameRate*appleDropTime)
	apple.draw()
	basket.draw()
	timerStim.draw()
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
	updateTimerText()
	timerStim.draw()
	optionsBox.draw()
	scoreDisplay.draw()

def playCond3():
	global i
	global nextLevelChangeTime
	global difficultyLevel
	global dropIntervalLength
	global appleDropTime
	global appleDecrement

	bkg.draw()
	moveBasket()
	if gamePlayClock.getTime() >= nextLevelChangeTime: # Yoke difficulty level to that of condition 1
		difficultyLevel = levelChangeLog[i]['Level']
		dropIntervalLength = difficultyDict[difficultyLevel]['interval']
		appleDropTime = difficultyDict[difficultyLevel]['drop time']
		appleDecrement = gameAreaHeight/(frameRate*appleDropTime)
		if i+1 < len(levelChangeLog):
			i += 1
			nextLevelChangeTime = levelChangeLog[i]['Time']
		else:
			nextLevelChangeTime = gamePlayLength + 100 # If there are no more level changes, make the next level change time unreachable
	if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
		updateApple()
		updateScore()
	apple.draw()
	basket.draw()
	updateTimerText()
	timerStim.draw()
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
	if levelChangeLog[len(levelChangeLog)-1]['Level'] != difficultyLevel: # If the difficulty level has changed, update the level change log
		updateChangeLog()
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

def updateChangeLog():
	levelChangeLog.append({'Time': gamePlayClock.getTime(), 'Level': difficultyLevel})

def changeLogToCsv():
	output_filename = 'changelog.csv'
	output_filepath = os.path.join(os.getcwd(), output_filename)
	column_labels = ["Time", "Level"]

	with open(output_filepath, 'wb') as new_csvfile:
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		writer.writeheader()
		for entry in levelChangeLog:
			writer.writerow(entry)

def csvToChangeLogDict():
	input_filename = 'changelog.csv'
	input_filepath = os.path.join(os.getcwd(), input_filename)
	with open(input_filepath) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			levelChangeLog.append({'Time': float(row['Time']), 'Level': int(row['Level'])})

def participantDataToCsv():
	output_filename = 'participant data.csv'
	output_filepath = os.path.join(os.getcwd(), output_filename)
	column_labels = ['ID', 'Gender', 'Handedness', 'Condition', 'Q1', 'Q2', 'Q3', 'Q4']

	with open(output_filepath, 'wb') as new_csvfile:
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		writer.writeheader()
		writer.writerow(participantDataDict)

def displayProbeInstructions():
	probeInstructions.draw()
	probeStartButtonBox.draw()
	probeStartButtonText.draw()

def displayProbe():
	global q1Answer
	global q2Answer
	global q3Answer
	global q4Answer
	q1.draw()
	q2.draw()
	q3.draw()
	q4.draw()
	q1Label1.draw()
	q1Label2.draw()
	q1Label3.draw()
	q2Label1.draw()
	q2Label2.draw()
	q2Label3.draw()
	q3Label1.draw()
	q3Label2.draw()
	q3Label3.draw()
	q4Label1.draw()
	q4Label2.draw()
	q4Label3.draw()
	if q1Scale.hasLevelChanged():
		q1Answer = q1Scale.activeLevel
	if q2Scale.hasLevelChanged():
		q2Answer = q2Scale.activeLevel
	if q3Scale.hasLevelChanged():
		q3Answer = q3Scale.activeLevel
	if q4Scale.hasLevelChanged():
		q4Answer = q4Scale.activeLevel
	q1Scale.draw()
	q2Scale.draw()
	q3Scale.draw()
	q4Scale.draw()
	probeSubmitButtonBox.draw()
	probeSubmitButtonText.draw()


# START EXPERIMENT
#win.setRecordFrameIntervals(True)

while not practiseButton.isClicked():
	displayPractiseScreen()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

resetApple() # Initialize apple
gamePlayClock = core.Clock() # Effectively starts the game play timer
while gamePlayClock.getTime() <= practisePlayLength: 
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	playPractise()
	mouse.clickReset()
	win.flip()

while not startButton.isClicked():
	displayInstructions()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

if condition == 3:
	csvToChangeLogDict()
	if i+1 < len(levelChangeLog):
		i += 1
		nextLevelChangeTime = levelChangeLog[i]['Time']
	else:
		nextLevelChangeTime = gamePlayLength + 100 # If there are no more level changes, make the next level change time unreachable

score = 0
scoreDisplay.setText('Score: ' + str(score))
resetApple() # Initialize apple & drop interval timer
gamePlayClock = core.Clock() # Effectively starts the game play timer

if condition == 1:
	levelChangeLog.append({'Time': 0, 'Level': difficultyLevel})
	while gamePlayClock.getTime() <= gamePlayLength or gamePaused: 
		if event.getKeys(keyList = ['q','escape']):
			core.quit()
		playCond1()
		mouse.clickReset()
		win.flip()
	changeLogToCsv()
elif condition == 2:
	while gamePlayClock.getTime() <= gamePlayLength or gamePaused: 
		if event.getKeys(keyList = ['q','escape']):
			core.quit()
		playCond2()
		mouse.clickReset()
		win.flip()
elif condition == 3:
	while gamePlayClock.getTime() <= gamePlayLength or gamePaused: 
		if event.getKeys(keyList = ['q','escape']):
			core.quit()
		playCond3()
		mouse.clickReset()
		win.flip()

while not probeStartButton.isClicked():
	displayProbeInstructions()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

while not probeSubmitButton.isClicked():
	displayProbe()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

participantDataDict.update({'Q1': q1Answer, 'Q2': q2Answer, 'Q3': q3Answer, 'Q4':q4Answer})
participantDataToCsv()
displayEndScreen()

win.close()
# pylab.plot(win.frameIntervals)
# pylab.show()
