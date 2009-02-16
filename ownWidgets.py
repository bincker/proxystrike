from PyQt4 import QtCore, QtGui

class QEncTextEdit(QtGui.QTextEdit):
	def __init__(self,a):
		QtGui.QTextEdit.__init__(self,a)
		pass

	def createStandardContextMenu (self):
		print "a"
		return QtGui.QMenu()
