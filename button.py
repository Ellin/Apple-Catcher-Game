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
	def __init__(self, win, scaleColor, activeColor, startLevel, width, height, pos, opacity = 1):
		self.win = win
		self.scaleColor = scaleColor
		self.activeColor = activeColor
		self.activeLevel = startLevel # default active level is the starting level
		self.width = width
		self.height = height
		self.posX = pos[0]
		self.posY = pos[1]
		self.opacity = opacity

		# Create scale bar
		barWidth = self.width* 0.8
		barLeftEdge = self.posX - barWidth/2.0
		barRightEdge = self.posX + barWidth/2.0
		self.bar = visual.Line(self.win, lineColor = self.scaleColor, start = (barLeftEdge, self.posY), end = (barRightEdge, self.posY), opacity = self.opacity)

		# Create scale arrows
		arrowWidth = self.width * 0.1
		self.leftArrow = visual.Polygon(win, lineColor = self.scaleColor, fillColor = self.scaleColor, edges = 3, radius = arrowWidth/2.0, pos = (barLeftEdge - arrowWidth/2.0, self.posY), ori = -90, opacity = self.opacity)
		self.rightArrow = visual.Polygon(win, lineColor = self.scaleColor, fillColor = self.scaleColor, edges = 3, radius = arrowWidth/2.0, pos = (barRightEdge + arrowWidth/2.0, self.posY), ori = 90, opacity = self.opacity)
		
		# Make the scale arrows function as buttons
		mouse = event.Mouse()
		self.leftArrowButton = Button(self.leftArrow, mouse)
		self.rightArrowButton = Button(self.rightArrow, mouse)

		# Calculate the space between each tick
		tickIntervalWidth = barWidth/6.0 # 7 ticks => 6 intervals

		# Calculate the end points of the tick bars
		tickYStart = self.posY - self.height/2.0
		tickYEnd = self.posY + self.height/2.0
		tick1PosX = barLeftEdge
		tick2PosX = self.posX - (2*tickIntervalWidth)
		tick3PosX = self.posX - (1*tickIntervalWidth)
		tick4PosX = self.posX
		tick5PosX = self.posX + (1*tickIntervalWidth)
		tick6PosX = self.posX + (2*tickIntervalWidth)
		tick7PosX = barRightEdge

		# Create tick bars
		self.tick1 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick1PosX, tickYStart), end = (tick1PosX, tickYEnd), opacity = self.opacity)
		self.tick2 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick2PosX, tickYStart), end = (tick2PosX, tickYEnd), opacity = self.opacity)
		self.tick3 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick3PosX, tickYStart), end = (tick3PosX, tickYEnd), opacity = self.opacity)
		self.tick4 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick4PosX, tickYStart), end = (tick4PosX, tickYEnd), opacity = self.opacity)
		self.tick5 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick5PosX, tickYStart), end = (tick5PosX, tickYEnd), opacity = self.opacity)
		self.tick6 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick6PosX, tickYStart), end = (tick6PosX, tickYEnd), opacity = self.opacity)
		self.tick7 = visual.Line(self.win, lineColor = self.scaleColor, start = (tick7PosX, tickYStart), end = (tick7PosX, tickYEnd), opacity = self.opacity)

		tickLabelPosY = self.posY - self.height # Prevents scale labels from overlapping the scale

		# Create tick labels
		self.tick1Label = visual.TextStim(self.win, text = '1', height = self.height, color = self.scaleColor, pos = (tick1PosX, tickLabelPosY), opacity = self.opacity)
		self.tick2Label = visual.TextStim(self.win, text = '2', height = self.height, color = self.scaleColor, pos = (tick2PosX, tickLabelPosY), opacity = self.opacity)
		self.tick3Label = visual.TextStim(self.win, text = '3', height = self.height, color = self.scaleColor, pos = (tick3PosX, tickLabelPosY), opacity = self.opacity)
		self.tick4Label = visual.TextStim(self.win, text = '4', height = self.height, color = self.scaleColor, pos = (tick4PosX, tickLabelPosY), opacity = self.opacity)
		self.tick5Label = visual.TextStim(self.win, text = '5', height = self.height, color = self.scaleColor, pos = (tick5PosX, tickLabelPosY), opacity = self.opacity)
		self.tick6Label = visual.TextStim(self.win, text = '6', height = self.height, color = self.scaleColor, pos = (tick6PosX, tickLabelPosY), opacity = self.opacity)
		self.tick7Label = visual.TextStim(self.win, text = '7', height = self.height, color = self.scaleColor, pos = (tick7PosX, tickLabelPosY), opacity = self.opacity)

		# Create tick dictionary
		self.tickDict = {1: {'tick': self.tick1, 'label': self.tick1Label}, 2: {'tick': self.tick2, 'label': self.tick2Label}, 3: {'tick': self.tick3, 'label': self.tick3Label}, 4: {'tick': self.tick4, 'label': self.tick4Label}, 5: {'tick': self.tick5, 'label': self.tick5Label}, 6: {'tick': self.tick6, 'label': self.tick6Label}, 7: {'tick': self.tick7, 'label': self.tick7Label}}
		
		# Set active colors
		self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
		self.tickDict[self.activeLevel]['label'].color = self.activeColor

	def hasLevelChanged(self):
		if self.leftArrowButton.isClicked():
			if self.activeLevel > 1:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel -= 1
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
				return True
		if self.rightArrowButton.isClicked():
			if self.activeLevel < 7:
				self.tickDict[self.activeLevel]['tick'].lineColor = self.scaleColor
				self.tickDict[self.activeLevel]['label'].color = self.scaleColor
				self.activeLevel += 1
				self.tickDict[self.activeLevel]['tick'].lineColor = self.activeColor
				self.tickDict[self.activeLevel]['label'].color = self.activeColor
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

	def setOpacity(self, newOpacity):
		self.leftArrow.opacity = newOpacity
		self.rightArrow.opacity = newOpacity
		self.bar.opacity = newOpacity
		self.tick1.opacity = newOpacity
		self.tick2.opacity = newOpacity
		self.tick3.opacity = newOpacity
		self.tick4.opacity = newOpacity
		self.tick5.opacity = newOpacity
		self.tick6.opacity = newOpacity
		self.tick7.opacity = newOpacity
		self.setTextOpacity(self.tick1Label, newOpacity)
		self.setTextOpacity(self.tick2Label, newOpacity)
		self.setTextOpacity(self.tick3Label, newOpacity)
		self.setTextOpacity(self.tick4Label, newOpacity)
		self.setTextOpacity(self.tick5Label, newOpacity)
		self.setTextOpacity(self.tick6Label, newOpacity)
		self.setTextOpacity(self.tick7Label, newOpacity)

	def setTextOpacity(self, textStim, newOpacity): # Need this to change text opacity b/c of stupid psychopy bug (see github.com/psychopy/psychopy/issues/1045)
		originalText = textStim.text
		textStim.setOpacity(newOpacity)
		textStim.setText('') # Change the text to force psychopy to update the textstim's properties (opacity) instead of relying on a cached version
		textStim.setText(originalText)
