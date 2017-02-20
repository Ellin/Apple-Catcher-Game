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
