from psychopy import visual, event

class Button(object):
	""" Turns an ImageStim or a shape into a button.
	isClicked() checks whether a left mouse click has been pressed *and released* on a stim. To use, it should be called every frame. """

	def __init__(self, stim, mouse):
		self.stim = stim
		self.mouse = mouse
		self.pressStarted = 0

	def isClicked(self):
		stimClicked = 0
		stimContainsMouse =  self.stim.contains(self.mouse)
		mouseIsPressed = self.mouse.getPressed()[0]

		if (not self.pressStarted) and mouseIsPressed and stimContainsMouse: # Press on stim has been started
			self.pressStarted = 1
		elif self.pressStarted and (not mouseIsPressed) and stimContainsMouse: # Mouse press is released inside of stim; button has been clicked
			self.pressStarted = 0
			stimClicked = 1
		elif self.pressStarted and (not mouseIsPressed) and (not stimContainsMouse): # Mouse press is released outside of stim; button not clicked
			self.pressStarted = 0

		return stimClicked

class Scale(object):
	"""docstring for Scale.. units in norm"""
	def __init__(self, win, color, startLevel, width, height, pos, opacity = 1):
		self.win = win
		self.color = color
		self.activeLevel = startLevel # default active level is the starting level
		self.width = width
		self.height = height
		self.posX = pos[0]
		self.posY = pos[1]
		self.opacity = opacity
		barWidth = self.width* 0.8
		barLeftEdge = self.posX - barWidth/2.0
		barRightEdge = self.posX + barWidth/2.0
		self.bar = visual.Line(self.win, lineColor = self.color, start = (barLeftEdge, self.posY), end = (barRightEdge, self.posY))

		arrowWidth = self.width * 0.1
		self.leftArrow = visual.Polygon(win, lineColor = self.color, fillColor = self.color, edges = 3, radius = arrowWidth/2.0, pos = (barLeftEdge - arrowWidth/2.0, self.posY), ori = -90)
		self.rightArrow = visual.Polygon(win, lineColor = self.color, fillColor = self.color, edges = 3, radius = arrowWidth/2.0, pos = (barRightEdge + arrowWidth/2.0, self.posY), ori = 90)
		mouse = event.Mouse()
		self.leftArrowButton = Button(self.leftArrow, mouse)
		self.rightArrowButton = Button(self.rightArrow, mouse)

		tickIntervalWidth = barWidth/6.0 # 7 ticks => 6 intervals
		tickYStart = self.posY - self.height/2.0
		tickYEnd = self.posY + self.height/2.0
		tick1PosX = barLeftEdge
		tick2PosX = self.posX - (2*tickIntervalWidth)
		tick3PosX = self.posX - (1*tickIntervalWidth)
		tick4PosX = self.posX
		tick5PosX = self.posX + (1*tickIntervalWidth)
		tick6PosX = self.posX + (2*tickIntervalWidth)
		tick7PosX = barRightEdge
		self.tick1 = visual.Line(self.win, lineColor = self.color, start = (tick1PosX, tickYStart), end = (tick1PosX, tickYEnd))
		self.tick2 = visual.Line(self.win, lineColor = self.color, start = (tick2PosX, tickYStart), end = (tick2PosX, tickYEnd))
		self.tick3 = visual.Line(self.win, lineColor = self.color, start = (tick3PosX, tickYStart), end = (tick3PosX, tickYEnd))
		self.tick4 = visual.Line(self.win, lineColor = self.color, start = (tick4PosX, tickYStart), end = (tick4PosX, tickYEnd))
		self.tick5 = visual.Line(self.win, lineColor = self.color, start = (tick5PosX, tickYStart), end = (tick5PosX, tickYEnd))
		self.tick6 = visual.Line(self.win, lineColor = self.color, start = (tick6PosX, tickYStart), end = (tick6PosX, tickYEnd))
		self.tick7 = visual.Line(self.win, lineColor = self.color, start = (tick7PosX, tickYStart), end = (tick7PosX, tickYEnd))

		tickLabelPosY = self.posY - self.height # Prevents scale labels from overlapping the scale
		self.tick1Label = visual.TextStim(self.win, text = '1', height = self.height, color = self.color, pos = (tick1PosX, tickLabelPosY))
		self.tick2Label = visual.TextStim(self.win, text = '2', height = self.height, color = self.color, pos = (tick2PosX, tickLabelPosY))
		self.tick3Label = visual.TextStim(self.win, text = '3', height = self.height, color = self.color, pos = (tick3PosX, tickLabelPosY))
		self.tick4Label = visual.TextStim(self.win, text = '4', height = self.height, color = self.color, pos = (tick4PosX, tickLabelPosY))
		self.tick5Label = visual.TextStim(self.win, text = '5', height = self.height, color = self.color, pos = (tick5PosX, tickLabelPosY))
		self.tick6Label = visual.TextStim(self.win, text = '6', height = self.height, color = self.color, pos = (tick6PosX, tickLabelPosY))
		self.tick7Label = visual.TextStim(self.win, text = '7', height = self.height, color = self.color, pos = (tick7PosX, tickLabelPosY))

	def hasLevelChanged(self):
		if self.leftArrowButton.isClicked():
			if self.activeLevel > 1:
				self.activeLevel -= 1
				return True
		if self.rightArrowButton.isClicked():
			if self.activeLevel < 7:
				self.activeLevel += 1
				return True
		return False

	def draw(self):
		self.leftArrow.draw()
		self.rightArrow.draw()
		self.bar.draw()
		self.tick1.draw()
		self.tick2.draw()
		self.tick3.draw()
		self.tick4.draw()
		self.tick5.draw()
		self.tick6.draw()
		self.tick7.draw()
		self.tick1Label.draw()
		self.tick2Label.draw()
		self.tick3Label.draw()
		self.tick4Label.draw()
		self.tick5Label.draw()
		self.tick6Label.draw()
		self.tick7Label.draw()
		