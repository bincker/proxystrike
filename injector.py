# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'injector.ui'
#
# Created: Tue May 13 17:04:02 2008
#	  by: PyQt4 UI code generator 4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Injector(object):
	def __init__(self):
		self.state="drop"
		self.dialog=None


	def setupUi(self, Dialog):
		self.dialog=Dialog
		Dialog.setObjectName("Dialog")
		Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(Dialog.minimumSizeHint()))

		self.vboxlayout = QtGui.QVBoxLayout(Dialog)
		self.vboxlayout.setObjectName("vboxlayout")

		self.hboxlayout = QtGui.QHBoxLayout()
		self.hboxlayout.setObjectName("hboxlayout")

		self.followButton = QtGui.QPushButton(Dialog)
		self.followButton.setObjectName("followButton")
		self.hboxlayout.addWidget(self.followButton)

		spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		self.hboxlayout.addItem(spacerItem)

		self.dropButton = QtGui.QPushButton(Dialog)
		self.dropButton.setObjectName("dropButton")
		self.hboxlayout.addWidget(self.dropButton)

		spacerItem1 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
		self.hboxlayout.addItem(spacerItem1)

		self.stopButton = QtGui.QPushButton(Dialog)
		self.stopButton.setObjectName("stopButton")
		self.hboxlayout.addWidget(self.stopButton)
		self.vboxlayout.addLayout(self.hboxlayout)

		self.rawreqEdit = QtGui.QTextEdit(Dialog)
		self.rawreqEdit.setObjectName("rawreqEdit")
		self.vboxlayout.addWidget(self.rawreqEdit)

		self.retranslateUi(Dialog)

		QtCore.QObject.connect(self.followButton, QtCore.SIGNAL("clicked()"), self.follow)
		QtCore.QObject.connect(self.dropButton, QtCore.SIGNAL("clicked()"), self.drop)
		QtCore.QObject.connect(self.stopButton, QtCore.SIGNAL("clicked()"), self.stop)

		QtCore.QMetaObject.connectSlotsByName(Dialog)


	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Request intercept", None, QtGui.QApplication.UnicodeUTF8))
		self.followButton.setText(QtGui.QApplication.translate("Dialog", "Follow", None, QtGui.QApplication.UnicodeUTF8))
		self.dropButton.setText(QtGui.QApplication.translate("Dialog", "Drop", None, QtGui.QApplication.UnicodeUTF8))
		self.stopButton.setText(QtGui.QApplication.translate("Dialog", "Stop intercept", None, QtGui.QApplication.UnicodeUTF8))

	def setReq(self,raw):
		self.rawreqEdit.setText(raw)

	def follow(self):
		self.state="follow"
		self.dialog.done(0)

	def drop(self):
		self.state="drop"
		self.dialog.done(0)

	def stop(self):
		self.state="stop"
		self.dialog.done(0)

	def getState(self):
		return self.state

	def getRawReq(self):
		return str(self.rawreqEdit.toPlainText())
