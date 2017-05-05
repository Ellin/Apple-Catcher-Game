from psychopy import core, event, gui, visual
from time import strftime
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
participantDlg.addField('Version:')
participantDlg.addText('                                                                                                               ')
participantDlg.show()

participantID = participantDlg.data[0]
gender = participantDlg.data[1]
handedness = participantDlg.data[2]
condition = int(participantDlg.data[3])
yokeID = participantDlg.data[4] # The participant ID that the game is yoked to (relevant only for condition 2)
participantDataDict = {'ID': participantID, 'Gender': gender, 'Handedness': handedness, 'Condition': condition}

# Generate window
win = visual.Window(fullscr = True, color = 'white', units = 'norm')

# Set frame rate
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

# Initialize Level Data Log
# The level data log is an array of dictionaries that will colect data (i.e. gamer timer, level, apples dropped, hits, misses, near misses) for each level that the participant plays
levelDataLog = []
i = 0 # Index for level data log

# Initialize game variables
gamePaused = 0
score = 0 # +1 point for every apple caught (counts for whole game, not per level)
hits = 0 # Number of apples caught per level
nearMisses = 0 # A 'near miss' is when an apple falls within a 3 basket width range (1 basket width from the actual basket on each side)
misses = 0 # A (complete) 'miss' is when an apple falls outside of the near miss range

# Time variables (Unit = seconds)
practisePlayLength = 15 # Practise play time (excluding pauses)
gamePlayLength = 10 # Play time (excluding pauses) should max out at 10 minutes
dropIntervalClock = core.Clock()
pauseClock = core.Clock()

#################################### Instruction / Text Display Screens #################################### 
# Practise Trial Instruction Screen
practiseInstructions = visual.TextStim(win, wrapWidth = 2, text = "Before you start the game, you will have about a minute to practise. Catch as many apples as you can by dragging the basket. Try changing the difficulty of the game by pressing pause to adjust the difficulty level using the scale in the bottom right corner of the screen. Press next to start the practise round.", color = 'black', height = 0.08)
practiseButtonBoxPosX = 0
practiseButtonBoxPosY = -0.5
practiseButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (practiseButtonBoxPosX, practiseButtonBoxPosY))
practiseButtonText = visual.TextStim(win, text = 'Next', color = 'black', height = 0.08, pos = (practiseButtonBoxPosX, practiseButtonBoxPosY))
practiseButton = tools.Button(practiseButtonBox, mouse)

# Game Instruction screen
if condition == 1:
	gameInstructionsText = 'Condition 1 instructions: You have finished the practise round. Like in the practise round, you will be able to change the difficulty level at any time to suit your preference by pressing the pause button to activate the difficulty scale in the bottom right corner. If you want the game to be more difficult, press the right arrow button. If you want the game to be less difficult, press the left arrow button. Press start when you are ready to play.'
	startButtonBoxPosY = -0.5
elif condition == 2:
	gameInstructionsText = 'Condition 2 instructions: You have finished the practise round. Before you start the game, choose how difficult you want the game to be using the scale below. Unlike the practise round, you will *not* be able to change the difficulty of the game once you start. Press start when you are ready to play.'
	startButtonBoxPosY = -0.75
elif condition == 3:
	gameInstructionsText = 'Condition 3 instructions: You have finished the practise round. Unlike the practise round, you will *not* be able to change the difficulty level of the game. The difficulty of the game may or may not change as you play, but you will not be able to choose when these changes happen. Press start when you are ready to play.'
	startButtonBoxPosY = -0.5
gameInstructions = visual.TextStim(win, wrapWidth = 2, text = gameInstructionsText, color = 'black', height = 0.08)
difficultyScaleCond2 = tools.Scale(win, scaleColor = 'black', activeColor = 'red', startLevel = 4, width = 0.5, height = 0.05, pos = (0, -0.5)) # Difficulty scale for condition 2 where participants set their difficulty level for the game
startButtonBoxPosX = 0
startButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButtonText = visual.TextStim(win, text = 'start', color = 'black', height = 0.08, pos = (startButtonBoxPosX, startButtonBoxPosY))
startButton = tools.Button(startButtonBox, mouse)

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
q1Answer = 4 # Default answer is 4 (middle of the scale)
q2Answer = 4
q3Answer = 4
q4Answer = 4
probeSubmitButtonBoxPosX = 0
probeSubmitButtonBoxPosY = -0.8
probeSubmitButtonBox = visual.Rect(win, lineColor = 'black', fillColor = 'grey', width = 0.3, height = 0.15, pos = (probeSubmitButtonBoxPosX, probeSubmitButtonBoxPosY))
probeSubmitButtonText = visual.TextStim(win, text = 'Submit', color = 'black', height = 0.08, pos = (probeSubmitButtonBoxPosX, probeSubmitButtonBoxPosY))
probeSubmitButton = tools.Button(probeSubmitButtonBox, mouse)

# End Screen
endText = visual.TextStim(win, wrapWidth = 2, text = 'This is the end of the study. Please get the experimenter.', color = 'black', height = 0.08)
#################################### #################################### #################################### 

# Specify game play area (units = norm)
gameAreaWidth = windowWidth
gameAreaHeight = windowHeight * (9.0/10.0) # The game play area is 9/10th the size of the window
gameAreaPosX = 0 
gameAreaPosY = (windowHeight - gameAreaHeight)/2.0
topGameAreaEdge = gameAreaPosY + gameAreaHeight/2.0
bottomGameAreaEdge = gameAreaPosY - gameAreaHeight/2.0
leftGameAreaEdge = gameAreaPosX - gameAreaWidth/2.0
rightGameAreaEdge = gameAreaPosX + gameAreaWidth/2.0

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
difficultyDict = { # difficultyDict is a dictionary containing a dictionary of 'interval' & 'drop time' settings associated with each difficulty level
	1: {'interval': 4, 'drop time': 8}, 
	2: {'interval': 3, 'drop time': 6}, 
	3: {'interval': 2, 'drop time': 4}, 
	4: {'interval': 1, 'drop time': 2},  
	5: {'interval': 0.5, 'drop time': 1}, 
	6: {'interval': 0.25, 'drop time': 0.5}, 
	7: {'interval': 0, 'drop time': 0.25}}
dropIntervalLength = difficultyDict[difficultyLevel]['interval'] # Unit = seconds. Time (excluding pauses) between apple drops from when last apple hit the ground to when the next apple drops
appleDropTime = difficultyDict[difficultyLevel]['drop time'] # Unit = seconds. The time it takes for an apple to hit the ground.
appleDecrement = gameAreaHeight/(frameRate*appleDropTime) # The decrement is how much down the screen the apple should drop per frame
appleStartPosX = random.uniform(leftGameAreaEdge + appleWidth/2.0, rightGameAreaEdge - appleWidth/2.0)
appleStartPosY = topGameAreaEdge + appleHeight/2
applePosX = appleStartPosX
applePosY = appleStartPosY

# Game options box (the area containing pause button, score, difficulty level scale)
optionsBoxWidth = windowWidth
optionsBoxHeight = windowHeight - gameAreaHeight
optionsBoxPosX = 0
optionsBoxPosY = bottomGameAreaEdge - optionsBoxHeight/2.0
optionsBox = visual.Rect(win, fillColor = 'grey', width = optionsBoxWidth, height = optionsBoxHeight, pos = (optionsBoxPosX, optionsBoxPosY))

# Difficulty Scale
difficultyScale = tools.Scale(win, scaleColor = 'white', activeColor = 'red', startLevel = 4, width = 0.5, height = 0.05, pos = (0.6, optionsBoxPosY), opacity = 0.3)

# Score display
scoreDisplay = visual.TextStim(win, text = 'Score: 0', color = 'white', height = 0.1, pos = (0, optionsBoxPosY))

# Game Timer Visual
timerStim = visual.TextStim(win, text = "", color = 'white', height = 0.1, pos = (0, 0.9))

# Pause button
pauseButtonBoxPosX = -0.75
pauseButtonBoxPosY = optionsBoxPosY
pauseButtonBox = visual.Rect(win, fillColor ='darkgrey', width = 0.3, height = 0.15, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
pauseButtonText = visual.TextStim(win, text = 'Pause', color = 'white', height = 0.08, pos = (pauseButtonBoxPosX, pauseButtonBoxPosY))
pauseButton = tools.Button(pauseButtonBox, mouse)

def displayGameInstructions():
	gameInstructions.draw()
	if condition == 2:
		if difficultyScaleCond2.hasLevelChanged():
			changeDifficulty(difficultyScaleCond2.activeLevel)
		difficultyScaleCond2.draw()
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

# Checks for near misses & misses. Update these counts.
def updateMisses():
	global nearMisses
	global misses
	basketEdges = getBasketEdges()
	appleEdges = getAppleEdges()
	if isAppleCaught() == False & isAppleTouchingGround(): # If the apple hit the ground not in the basket, then check whether it is a near miss or a (complete) miss
		if (appleEdges['left'] <= basketEdges['right'] + basketWidth) & (appleEdges['right'] >= basketEdges['left'] - basketWidth):
			nearMisses += 1
		else:
			misses +=1

# Update score & hit counts if apple has been caught.
def updateScoreAndHits():
	global score
	global hits
	if isAppleCaught():
		score += 1
		hits +=1
		scoreDisplay.setText('Score: ' + str(score))

# Reset apple position to top of screen. Also reset the drop interval clock.
def resetApple():
	global applePosX
	global applePosY
	dropIntervalClock.reset()
	applePosY = appleStartPosY
	applePosX = random.uniform(leftGameAreaEdge + appleWidth/2.0, rightGameAreaEdge - appleWidth/2.0)
	while abs(applePosX - basketPosX) < basketWidth + appleWidth/2.0: # Make sure the new apple drops at least a basket width + half the apple's width away from the participant's basket to force the participant to move at least half a basket width to catch the next apple
		applePosX = random.uniform(leftGameAreaEdge + appleWidth/2.0, rightGameAreaEdge - appleWidth/2.0)
	apple.setPos([applePosX, applePosY])

# Move the apple's position down
def decrementApple():
	global applePosY
	applePosY -= appleDecrement
	apple.setPos([applePosX, applePosY])

# Checks for and updates hits/misses. Update apple position.
def updateApple():
	if isAppleCaught() or isAppleTouchingGround():
		updateMisses()
		updateScoreAndHits()
		resetApple()
	else:
		decrementApple()

# Change difficulty level of game (including how fast the apple falls and interval between apple drops)
def changeDifficulty(newDifficultyLevel):
	global difficultyLevel
	global dropIntervalLength
	global appleDropTime
	global appleDecrement
	difficultyLevel = newDifficultyLevel
	dropIntervalLength = difficultyDict[difficultyLevel]['interval']
	appleDropTime = difficultyDict[difficultyLevel]['drop time']
	appleDecrement = gameAreaHeight/(frameRate*appleDropTime)

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

# Update the levelDataLog with the number of apples dropped, caught (hit), missed, and near-missed during the level. Then reset the apple catch data variables.
def logAppleCatchData():
	global hits
	global misses
	global nearMisses
	applesDropped = hits + misses + nearMisses
	levelDataLog[i].update({'Apples Dropped': applesDropped, 'Hits': hits, 'Misses': misses, 'Near Misses': nearMisses})
	hits = 0
	misses = 0
	nearMisses = 0

# Draw game graphics common to practise trial and all conditions
def drawCommonGameGraphics():
	bkg.draw()
	apple.draw()
	basket.draw()
	optionsBox.draw()
	difficultyScale.draw()
	scoreDisplay.draw()

# Play practise trial for participant
def playPractise():
	global gamePaused

	if (not gamePaused):
		moveBasket()
		if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
			updateApple()
	elif difficultyScale.hasLevelChanged():
		changeDifficulty(difficultyScale.activeLevel)

	if pauseButton.isClicked():
		gamePaused = 1 - gamePaused # Flip pause status of game from 0 to 1 or vice versa
		if gamePaused:
			pauseGame()
		else:
			resumeGame()

	drawCommonGameGraphics()
	pauseButtonBox.draw()
	pauseButtonText.draw()
	bkgPauseOverlay.draw()

def playCond1():
	global gamePaused
	global i

	if (not gamePaused):
		moveBasket()
		if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
			updateApple()
		updateTimerText()
	elif difficultyScale.hasLevelChanged():
		changeDifficulty(difficultyScale.activeLevel)

	if pauseButton.isClicked():
		gamePaused = 1 - gamePaused # Flip pause status of game from 0 to 1 or vice versa
		if gamePaused:
			pauseGame()
		else:
			resumeGame()
			if levelDataLog[i]['Level'] != difficultyLevel: # Relevant only to Condition 1: If the difficulty level has changed upon resume, update the level data log.
				logAppleCatchData()
				levelDataLog.append({'Game Timer': gamePlayClock.getTime(), 'Level': difficultyLevel})
				i += 1

	drawCommonGameGraphics()
	timerStim.draw()
	pauseButtonBox.draw()
	pauseButtonText.draw()
	bkgPauseOverlay.draw()

def playCond2():
	moveBasket()
	if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
		updateApple()

	updateTimerText()
	drawCommonGameGraphics()
	timerStim.draw()

def playCond3():
	global i
	global nextLevelChangeTime

	moveBasket()
	if gamePlayClock.getTime() >= nextLevelChangeTime: 
		logAppleCatchData()
		i += 1
		changeDifficulty(levelDataLog[i]['Level']) # Yoke difficulty level to that of condition 1
		difficultyScale.setLevel(difficultyLevel)
		if i+1 < len(levelDataLog):
			nextLevelChangeTime = levelDataLog[i+1]['Game Timer']
		else:
			nextLevelChangeTime = gamePlayLength + 100 # If there are no more level changes, make the next level change time unreachable

	if (applePosY != appleStartPosY) or (dropIntervalClock.getTime() >= dropIntervalLength): # This allows the apple to start its drop only after the drop interval has passed. If the drop interval is changed mid-fall, then the apple continues falling.
		updateApple()

	updateTimerText()
	drawCommonGameGraphics()
	timerStim.draw()

# Create a csv file containing level change data. Used only in Condition 1 to save the participant's level changes to a csv (which will later be used for yoking in Condition 3).
def createChangeLogCsv():
	output_filename = participantID + '.csv'
	foldername = 'Condition-1_Level-Change-Logs'
	output_filepath = os.path.join(os.getcwd(), foldername, output_filename)
	column_labels = ['Game Timer', 'Level']

	with open(output_filepath, 'wb') as new_csvfile:
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		writer.writeheader()
		for entry in levelDataLog:
			levelChangeDict = {'Game Timer': entry['Game Timer'], 'Level': entry['Level']} # Extract just the 'Game Timer' and 'Level' data from levelDataLog
			writer.writerow(levelChangeDict)

# Converts csv containing level changes (from participant in Condition 1) to an array of dictionaries. Used only in Condition 3 for yoking.
def changeLogCsvToDict():
	input_filename = yokeID + '.csv'
	foldername = 'Condition-1_Level-Change-Logs'
	input_filepath = os.path.join(os.getcwd(), foldername, input_filename)
	with open(input_filepath) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			levelDataLog.append({'Game Timer': float(row['Game Timer']), 'Level': int(row['Level'])})

# Write participant data to two csv files (individual participant file and master file with data of all participants)
def participantDataToCsv():
	output_filename = date + '_' + strftime('%H%M%S') + '_' + 'PID' + '-'+ participantID + '.csv'
	output_foldername = 'Individual-Participant-Data'
	output_filepath = os.path.join(os.getcwd(), output_foldername, output_filename) # filepath for individual participant data files
	master_filename = 'Master-Participant-Data.csv'
	master_filepath = os.path.join(os.getcwd(), master_filename) # filepath for the master participant data file (holds data of all participants in 1 file)
	column_labels = ['Date', 'Time', 'ID', 'Gender', 'Handedness', 'Condition', 'Q1', 'Q2', 'Q3', 'Q4', 'Game Timer', 'Level', 'Apples Dropped', 'Hits', 'Misses', 'Near Misses']

	with open(output_filepath, 'wb') as new_csvfile: # writes to new file (individual participant data file)
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		writer.writeheader()
		for entry in levelDataLog:
			participantDataDict.update(entry)
			writer.writerow(participantDataDict)

	masterFileExists = os.path.isfile(master_filepath) # Boolean variable for whether the master file already exists
	with open(master_filepath, 'ab') as new_csvfile: # appends the same data as above to master participant data file
		writer = csv.DictWriter(new_csvfile, fieldnames = column_labels)
		if not masterFileExists: # if master participant file does not already exist, create a new file with headers (otherwise, do nothing & just append data to existing file)
			writer.writeheader()
		for entry in levelDataLog:
			participantDataDict.update(entry)
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

#################################### START EXPERIMENT ####################################
#win.setRecordFrameIntervals(True)

# Get date & time
date = strftime("%Y-%m-%d") # Get current date
time = strftime("%H:%M") # Get current time (the time when the data in the dialog box is submitted)

# Display instruction screen for the practise trial
while not practiseButton.isClicked():
	displayPractiseScreen()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

# Initializations for practise trial
resetApple() # Initialize apple (drop interval timer is also reset here)
gamePlayClock = core.Clock() # Effectively starts the game play timer

# Run practise trial
while gamePlayClock.getTime() <= practisePlayLength or gamePaused: 
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	playPractise()
	mouse.clickReset()
	win.flip()

# Display instruction screen for the actual game
while not startButton.isClicked():
	displayGameInstructions()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

# If Condition 1 or 3, reset difficulty level of game back to 4 (in Condition 2, participant chooses the difficulty level via a scale in the game instructions screen)
if condition == 1 or condition == 3:
	changeDifficulty(4)

# If Condition 3, get the time that the next level change should occur
if condition == 3:
	changeLogCsvToDict()
	if i+1 < len(levelDataLog):
		nextLevelChangeTime = levelDataLog[i+1]['Game Timer']
	else:
		nextLevelChangeTime = gamePlayLength + 100 # If there are no more level changes, make the next level change time unreachable

# Reset game variables (since the trial round has finished and the real game will be starting)
score = 0
hits = 0
misses = 0
nearMisses = 0
scoreDisplay.setText('Score: ' + str(score))
difficultyScale.setLevel(difficultyLevel) # Visually set active level of difficulty scale to proper difficulty level
resetApple() # Initialize apple (drop interval timer is also reset here)
gamePlayClock = core.Clock() # Effectively starts the game play timer

# Run the appropriate game for the condition
if condition == 1:
	levelDataLog.append({'Game Timer': 0, 'Level': difficultyLevel})
	while gamePlayClock.getTime() <= gamePlayLength or gamePaused: 
		if event.getKeys(keyList = ['q','escape']):
			core.quit()
		playCond1()
		mouse.clickReset()
		win.flip()
	createChangeLogCsv()
elif condition == 2:
	levelDataLog.append({'Game Timer': 0, 'Level': difficultyLevel})
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
logAppleCatchData()

# Display instruction screen for the probe
while not probeStartButton.isClicked():
	displayProbeInstructions()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

# Display screen containing the probes
while not probeSubmitButton.isClicked():
	displayProbe()
	if event.getKeys(keyList = ['q','escape']):
		core.quit()
	mouse.clickReset()
	win.flip()

participantDataDict.update({'Date': date, 'Time': time,'Q1': q1Answer, 'Q2': q2Answer, 'Q3': q3Answer, 'Q4':q4Answer})

# Write all participant data collected over the duration of the experiment to csv files
participantDataToCsv()

# Display end screen
displayEndScreen()

win.close()
# pylab.plot(win.frameIntervals)
# pylab.show()
