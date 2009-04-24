#Covered by GPL V2.0
#Coded by Carlos del Ojo Elias (deepbit@gmail.com)

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainform.ui'
#
# Created: Tue Aug 29 19:57:46 2006
#      by: PyQt4 UI code generator 4.0.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui
from Proxynet import *
from string import *
import cPickle as pickl
from mainGUI import *
import logging
import urllib
from injector import Injector
import re
import md5
import difflib
import webbrowser

logging.basicConfig(level=logging.INFO,format='%(message)s')


class Ui_MainWindow(mainGUI):
	def __init__(self):
		self.targetSelect="All"
		self.pathSelect="All"
		self.variableSelect="All"
		self.timer = QtCore.QTimer()
		QtCore.QObject.connect(self.timer,QtCore.SIGNAL("timeout()"),self.timerFunc)
		self.timer.start(1000)

		self.lastResponse=None
		self.newResponse=None

		self.controller=None
		self.resultsWidgets={}

	def __getattr__(self,value): 
		if value=="numRequests": 
			return len(self.controller.getRequests()) 
		else: 
			raise AttributeError 


	def setController(self,crllr):
		self.controller=crllr


	def setupUi(self, MainWindow):
		mainGUI.setupUi(self,MainWindow)

		self.retranslateUi(MainWindow)
		
		QtCore.QObject.connect(self.actionOpen_2, QtCore.SIGNAL("triggered()"), self.funcion_Open)
		QtCore.QObject.connect(self.actionSave_session, QtCore.SIGNAL("triggered()"), self.funcion_Save)
		QtCore.QObject.connect(self.actionExit_2, QtCore.SIGNAL("triggered()"), self.salir)
		QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL("clicked(bool)"), self.updateTable)
		QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL("clicked(bool)"), self.updateTable)
		QtCore.QObject.connect(self.radioButton_3, QtCore.SIGNAL("clicked(bool)"), self.updateTable)
		QtCore.QObject.connect(self.comboBox, QtCore.SIGNAL("activated(QString)"), self.targetSelected)
		QtCore.QObject.connect(self.comboBox_2, QtCore.SIGNAL("activated(QString)"), self.pathSelected)
		QtCore.QObject.connect(self.tableWidget, QtCore.SIGNAL("currentCellChanged(int,int,int,int)"), self.cambiaPeticion)
		QtCore.QObject.connect(self.varStatsTreeWidget, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem *,int)"), self.slotTree)
		QtCore.QObject.connect(self.updateVarStatsButton, QtCore.SIGNAL("clicked()"), self.updateVarStatsTree)
		QtCore.QObject.connect(self.updateReqStatsButton, QtCore.SIGNAL("clicked()"), self.updateReqStatsTree)
		QtCore.QObject.connect(self.deleteInViewButton, QtCore.SIGNAL("clicked()"), self.deleteInView)
		QtCore.QObject.connect(self.deleteSelectedButton, QtCore.SIGNAL("clicked()"), self.deleteSelected)
		QtCore.QObject.connect(self.editRequestsButton, QtCore.SIGNAL("clicked()"), self.toogleEditor)
		QtCore.QObject.connect(self.doneButton, QtCore.SIGNAL("clicked()"), self.toogleEditor)
		QtCore.QObject.connect(self.setCookieButton, QtCore.SIGNAL("clicked()"), self.setNewCookie)
		QtCore.QObject.connect(self.substButton, QtCore.SIGNAL("clicked()"), self.applyRegex)
		QtCore.QObject.connect(self.configApplyButton, QtCore.SIGNAL("clicked()"), self.applyConfig)
		QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL("triggered()"), self.funcion_About)
		QtCore.QObject.connect(self.interceptCheck, QtCore.SIGNAL("toggled(bool)"), self.controller.setIntercept)
		QtCore.QObject.connect(self.reqperformButton, QtCore.SIGNAL("clicked()"), self.performRepeater)
		QtCore.QObject.connect(self.repeatButton, QtCore.SIGNAL("clicked()"), self.sendRepeater)
		QtCore.QObject.connect(self.diffButton, QtCore.SIGNAL("toggled(bool)"), self.showResponse)
		QtCore.QObject.connect(self.pluginCombo, QtCore.SIGNAL("activated(int)"), self.changePlugin)

		QtCore.QObject.connect(self.startCrawlButton, QtCore.SIGNAL("toggled(bool)"), self.startStopCrawling)
		QtCore.QObject.connect(self.crawlPluginCheck, QtCore.SIGNAL("toggled(bool)"), self.controller.setCrawlerForward)
		QtCore.QObject.connect(self.crawlFormsList, QtCore.SIGNAL("itemDoubleClicked (QListWidgetItem *)"), self.uniqFormClicked)
		QtCore.QObject.connect(self.crawlResetButton, QtCore.SIGNAL("clicked()"), self.resetCrawler)

		QtCore.QObject.connect(self.resetCacheButton, QtCore.SIGNAL("clicked()"), self.resetPluginCache)
		QtCore.QObject.connect(self.ToHTMLButton, QtCore.SIGNAL("clicked()"), self.pluginToHTML)
		QtCore.QObject.connect(self.ToXMLButton, QtCore.SIGNAL("clicked()"), self.pluginToXML)

		
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		self.startPlugins()


####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################

	def resetPluginCache(self):
		plugname=str(self.pluginCombo.currentText())
		self.controller.resetPluginCache(plugname)

	def updatePluginStatus(self):
		st=self.controller.getPluginStatus()
		a=0
		self.pluginStatusTable.clearContents()
		self.pluginStatusTable.setRowCount(0)
		for i,j in st.items():
			self.pluginStatusTable.insertRow(a)
			self.pluginStatusTable.setItem(a,0,QtGui.QTableWidgetItem(i))
			self.pluginStatusTable.setItem(a,1,QtGui.QTableWidgetItem(str(j)))
			a+=1
		
	def pluginToHTML(self):
		plugname=str(self.pluginCombo.currentText())
		fileName = QtGui.QFileDialog.getSaveFileName()
		if len(fileName)>0:
			try:
				self.controller.saveHTML(plugname,fileName)
			except Exception,r:
				mb = QtGui.QMessageBox ("Error",str(r),QtGui.QMessageBox.Critical,QtGui.QMessageBox.Ok,0,0)
				mb.exec_()

	def pluginToXML(self):
		plugname=str(self.pluginCombo.currentText())
		fileName = QtGui.QFileDialog.getSaveFileName()
		if len(fileName)>0:
			try:
				self.controller.saveXML(plugname,fileName)
			except Exception,r:
				mb = QtGui.QMessageBox ("Error",str(r),QtGui.QMessageBox.Critical,QtGui.QMessageBox.Ok,0,0)
				mb.exec_()

	def changePlugin(self,dest):
		self.stackedWidget_2.setCurrentIndex(dest+1)

	def enablePlugin(self,bl):
		plugname=str(self.pluginCombo.currentText())
		self.controller.enablePlugin(plugname,bl)

	def setPluginThreads(self,n):
		plugname=str(self.pluginCombo.currentText())
		self.controller.setPluginThreads(plugname,n)

	def getPluginResult(self,w,n):
		plugname=str(self.pluginCombo.currentText())
		w=self.resultsWidgets[plugname].indexOfTopLevelItem(w)
		req=self.controller.getPluginResult(plugname,w)
		if req:
			self.requrlEdit.setText(req.schema)
			self.reqTextEdit.setText(req.getAll())
			self.tabWidget.setCurrentIndex(6)
			

	def startPlugins(self):
		props=self.controller.getPluginProperties()
		number=1
		for pluginame,j in props.items():
			self.pluginCombo.addItem(pluginame,QtCore.QVariant(number))

			page = QtGui.QWidget()
			page.setGeometry(QtCore.QRect(0,0,919,622))
			page.setObjectName("page_"+str(number))
			verticalLayout = QtGui.QVBoxLayout(page)
			verticalLayout.setMargin(1)
			horizontalLayout_3 = QtGui.QHBoxLayout()
			horizontalLayout_3.setObjectName("horizontalLayout_3")
			enableCheck = QtGui.QCheckBox(page)
			enableCheck.setObjectName("enableCheck")
			horizontalLayout_3.addWidget(enableCheck)
			spacerItem14 = QtGui.QSpacerItem(88,17,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
			horizontalLayout_3.addItem(spacerItem14)
			horizontalLayout = QtGui.QHBoxLayout()
			horizontalLayout.setObjectName("horizontalLayout")
			label= QtGui.QLabel(page)
			label.setObjectName("label_"+str(number))
			horizontalLayout.addWidget(label)
			attackRequestThreadsSpin = QtGui.QSpinBox(page)
			attackRequestThreadsSpin.setMinimum(1)
			attackRequestThreadsSpin.setMaximum(20)
			attackRequestThreadsSpin.setObjectName("attackRequestThreadsSpin")
			horizontalLayout.addWidget(attackRequestThreadsSpin)
			horizontalLayout_3.addLayout(horizontalLayout)
			verticalLayout.addLayout(horizontalLayout_3)

			enableCheck.setText(QtGui.QApplication.translate("MainWindow", "enable", None, QtGui.QApplication.UnicodeUTF8))
			label.setText(QtGui.QApplication.translate("MainWindow", "Request threads", None, QtGui.QApplication.UnicodeUTF8))

			QtCore.QObject.connect(enableCheck, QtCore.SIGNAL("toggled(bool)"), self.enablePlugin)
			QtCore.QObject.connect(attackRequestThreadsSpin, QtCore.SIGNAL("valueChanged (int)"), self.setPluginThreads)

			if j["type"]=="tree":
				tree = QtGui.QTreeWidget(page)
				tree.setAlternatingRowColors(True)
				tree.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
				tree.setObjectName("tree_"+str(number))
				tree.setColumnCount(len(j["fields"]))
				verticalLayout.addWidget(tree)

				k=0
				for i in j["fields"]:
					tree.headerItem().setText(k,QtGui.QApplication.translate("MainWindow", i, None, QtGui.QApplication.UnicodeUTF8))
					tree.headerItem().setText(k,QtGui.QApplication.translate("MainWindow", i, None, QtGui.QApplication.UnicodeUTF8))
					tree.headerItem().setText(k,QtGui.QApplication.translate("MainWindow", i, None, QtGui.QApplication.UnicodeUTF8))
					tree.headerItem().setText(k,QtGui.QApplication.translate("MainWindow", i, None, QtGui.QApplication.UnicodeUTF8))
					k+=1

				WIDGETRESULT=tree
				QtCore.QObject.connect(tree, QtCore.SIGNAL("itemDoubleClicked(QTreeWidgetItem *,int)"), self.getPluginResult)

			elif j["type"]=="text":
				text = QtGui.QTextEdit(page)
				text.setReadOnly(True)
				text.setObjectName("text_"+str(number))
				verticalLayout.addWidget(text)
				WIDGETRESULT=text

			self.resultsWidgets[pluginame]=WIDGETRESULT
				
			self.stackedWidget_2.addWidget(page)

			number+=1

		self.stackedWidget_2.setCurrentIndex(1)



	def funcion_Save(self):
		fileName = QtGui.QFileDialog.getSaveFileName()
		if len(fileName)>0:
			self.timer.stop()
			self.controller.save(fileName)
			self.timer.start(1000)
      
	def funcion_Open(self):
		fileName = QtGui.QFileDialog.getOpenFileName()
		if len(fileName)>0:
			self.timer.stop()
			self.comboBox.clear()
			self.comboBox.addItem("All")
			self.comboBox_2.clear()
			self.comboBox_2.addItem("All")


			self.tableWidget.clearContents()
			self.tableWidget_2.clearContents()
			self.treeXss.clear()
			self.treeSql.clear()
			self.controller.load(fileName)

			self.timer.start(1000)


#	def __getattr__(self,value):
#		if value=="numRequests":
#			return len(self.controller.getRequests())
#		else:
#			raise AttributeError

	def updateVarStatsTree(self):
		self.varStatsTreeWidget.clear()
		self.varStatsTreeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Variable", None, QtGui.QApplication.UnicodeUTF8))
		self.varStatsTreeWidget.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Values", None, QtGui.QApplication.UnicodeUTF8))

		variableStats=self.controller.getVariableStats()
		sort1=variableStats.keys()
		sort1.sort()
		for tg in sort1:
			target=QtCore.QStringList()
			target.append(tg)
			targetTree=QtGui.QTreeWidgetItem(target)
			self.varStatsTreeWidget.addTopLevelItem(targetTree)
			sort2=variableStats[tg].keys()
			sort2.sort()
			for pt in sort2:
				path=QtCore.QStringList()
				path.append(pt)
				pathTree=QtGui.QTreeWidgetItem(path)
				pathTree.setTextColor(0,QtGui.QColor(0,0,200))
				font=pathTree.font(0)
				font.setBold(True)
				pathTree.setFont(0,font)
				targetTree.addChild(pathTree)
				sort3=variableStats[tg][pt].keys()
				sort3.sort()
				for vr in sort3:
					variable=QtCore.QStringList()
					variable.append(vr)
					values=""					
					for vls in variableStats[tg][pt][vr].keys():
						values+=urllib.unquote(vls)+"\n"
					variable.append(values)
					variableTree=QtGui.QTreeWidgetItem(variable)
					pathTree.addChild(variableTree)
		

	def updateReqStatsTree(self):
		self.reqStatsTreeWidget.clear()
		self.reqStatsTreeWidget.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Request", None, QtGui.QApplication.UnicodeUTF8))
		self.reqStatsTreeWidget.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Variable set", None, QtGui.QApplication.UnicodeUTF8))
	
		reqStats=self.controller.getReqStats()
		sort1=reqStats.keys()
		sort1.sort()
		for tg in sort1:
			target=QtCore.QStringList()
			target.append(tg)
			targetTree=QtGui.QTreeWidgetItem(target)
			self.reqStatsTreeWidget.addTopLevelItem(targetTree)
			sort2=reqStats[tg].items()
			sort2.sort()
			for k,l in sort2:
				path=QtCore.QStringList()
				path.append(k)
				sets=""
				for set in l:
					sets+=join(set[0],',')+'\n'
				path.append(sets)
				pathTree=QtGui.QTreeWidgetItem(path)
				pathTree.setTextColor(0,QtGui.QColor(0,0,200))
				font=pathTree.font(0)
				font.setBold(True)
				pathTree.setFont(0,font)
				targetTree.addChild(pathTree)

	

	def limpiatablas(self):
		self.tableWidget.clear()
		self.tableWidget.setColumnCount(4)
		self.tableWidget.setRowCount(0)
		headerItem = QtGui.QTableWidgetItem()
		headerItem.setText(QtGui.QApplication.translate("MainWindow", "Method", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget.setHorizontalHeaderItem(0,headerItem)
		
		headerItem1 = QtGui.QTableWidgetItem()
		headerItem1.setText(QtGui.QApplication.translate("MainWindow", "Target", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget.setHorizontalHeaderItem(1,headerItem1)
		
		headerItem2 = QtGui.QTableWidgetItem()
		headerItem2.setText(QtGui.QApplication.translate("MainWindow", "Url", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget.setHorizontalHeaderItem(2,headerItem2)
		
		headerItem3 = QtGui.QTableWidgetItem()
		headerItem3.setText(QtGui.QApplication.translate("MainWindow", "Cookies", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget.setHorizontalHeaderItem(3,headerItem3)

		self.tableWidget_2.clear()
		self.tableWidget_2.setColumnCount(2)
		self.tableWidget_2.setRowCount(0)
		
		headerItem4 = QtGui.QTableWidgetItem()
		headerItem4.setText(QtGui.QApplication.translate("MainWindow", "Variable", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget_2.setHorizontalHeaderItem(0,headerItem4)
		
		headerItem5 = QtGui.QTableWidgetItem()
		headerItem5.setText(QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
		self.tableWidget_2.setHorizontalHeaderItem(1,headerItem5)

	def updateTable(self):
		requests=self.controller.getRequests()

		if self.radioButton.isChecked()==True:
			method="GET"
		elif self.radioButton_2.isChecked()==True:
			method="POST"	
		else:
			method="BOTH"
			
		a=0
		for i in requests:
			if method=="BOTH":
				self.tableWidget.showRow(a)
			elif method==i.method:
				self.tableWidget.showRow(a)
			else:
				self.tableWidget.hideRow(a)

			
			if self.targetSelect!="All":
				if i.urlWithoutPath!=self.targetSelect:
					self.tableWidget.hideRow(a)
				elif self.pathSelect!="All":
					if i.path!=self.pathSelect:
						self.tableWidget.hideRow(a)
					elif self.variableSelect!="All":
						if not ( i.existsGETVar(self.variableSelect) or i.existsPOSTVar(self.variableSelect) ):
							self.tableWidget.hideRow(a)

			a+=1

		self.tableWidget.resizeColumnsToContents()
		self.tableWidget.resizeRowsToContents()
		#Al actualizar pueden visualizarse rows cuyas anchuras no han sido ajstadas, por eso lo de aqui arriba )
					

		
	def targetSelected(self,qstring):

		variableStats=self.controller.getVariableStats()

		self.targetSelect=str(qstring)
		self.comboBox_2.clear()
		self.comboBox_2.addItem("All")

		if self.targetSelect!="All" and self.targetSelect!='':
			list=variableStats[self.targetSelect].keys()
			list.sort()
			for i in list:
				self.comboBox_2.addItem(i)

		self.variableSelect="All"
		self.pathSelect="All"

		self.updateTable()
		
	def pathSelected(self,qstring):
		variableStats=self.controller.getVariableStats()
		self.pathSelect=str(qstring)
		
		self.variableSelect="All"
		self.updateTable()
		

	def cambiaPeticion(self,row,col,row2,col2):
		"Cada vez que se aprieta una peticion de la tabla. row2 y col 2 no se utilizan"
		requests=self.controller.getRequests()

		if self.numRequests:	
			self.requestEdit.clear()
			self.requestEdit.append(requests[row].getAll())
			self.responseEdit.clear()
			self.responseEdit.setText(requests[row].response.getAll())
			
			self.tableWidget_2.clear()
			self.tableWidget_2.setColumnCount(2)
			self.tableWidget_2.setRowCount(0)
			
			headerItem4 = QtGui.QTableWidgetItem()
			headerItem4.setText(QtGui.QApplication.translate("MainWindow", "Variable", None, QtGui.QApplication.UnicodeUTF8))
			self.tableWidget_2.setHorizontalHeaderItem(0,headerItem4)
			
			headerItem5 = QtGui.QTableWidgetItem()
			headerItem5.setText(QtGui.QApplication.translate("MainWindow", "Value", None, QtGui.QApplication.UnicodeUTF8))
			self.tableWidget_2.setHorizontalHeaderItem(1,headerItem5)
		
			a=0
			for i in requests[row].getGETVars():
				self.tableWidget_2.insertRow(a)
				self.tableWidget_2.setItem(a,0,QtGui.QTableWidgetItem(i.name))
				self.tableWidget_2.setItem(a,1,QtGui.QTableWidgetItem(i.value))
				a+=1
	
			for i in requests[row].getPOSTVars():
				self.tableWidget_2.insertRow(a)
				self.tableWidget_2.setItem(a,0,QtGui.QTableWidgetItem(i.name))
				self.tableWidget_2.setItem(a,1,QtGui.QTableWidgetItem(i.value))
				a+=1
	
			self.tableWidget_2.resizeColumnToContents(0)
			self.tableWidget_2.resizeColumnToContents(1)
			self.tableWidget_2.resizeRowsToContents()
			

	def slotTree (self,item,a):
		if item.parent()!=None and item.parent().parent()!=None:

			self.targetSelected(item.parent().parent().text(0))
			self.pathSelected(item.parent().text(0))
			
			indexpath=self.comboBox_2.findText(item.parent().text(0))
			indextarget=self.comboBox.findText(item.parent().parent().text(0))

			self.comboBox.setCurrentIndex(indextarget)
			self.comboBox_2.setCurrentIndex(indexpath)


	def salir(self):
		sys.exit(0)

	def updateResults(self):
		results=self.controller.getNewResults()
		for plugin,j in results.items():
			if j[0]=="tree":
				trinfo=j[1]

				for i in trinfo:
					target=QtCore.QStringList()
					target.append(i[0])
					targetTree=QtGui.QTreeWidgetItem(target)
					self.resultsWidgets[plugin].addTopLevelItem(targetTree)
					for j in i[1]:
						target2=QtCore.QStringList()
						target2.append("")
						for k in j:
							if k:
								target2.append(k)
							else:
								target2.append("")
						targetTree2=QtGui.QTreeWidgetItem(target2)
						targetTree.addChild(targetTree2)
			elif j[0]=="text":
				self.resultsWidgets[plugin].append("".join(j[1]))



	def timerFunc(self):

		self.controller.timer()
		self.updateResults()
		self.updatePluginStatus()
		self.updateCrawlInfo()
		self.updateLogData()

		reqs=self.controller.getNewRequests()
		if reqs:
			a=self.tableWidget.rowCount()
			for i in reqs:

				self.tableWidget.insertRow(a)
				self.tableWidget.setItem(a,0,QtGui.QTableWidgetItem(i.method))
				self.tableWidget.setItem(a,1,QtGui.QTableWidgetItem(i.urlWithoutPath))
				self.tableWidget.setItem(a,2,QtGui.QTableWidgetItem(i.pathWithVariables))
				if i["Cookie"]:
					self.tableWidget.setItem(a,3,QtGui.QTableWidgetItem(i["Cookie"]))
				
				self.updateCombos(i)
				a+=1

			self.updateTable()
			self.tableWidget.setRowCount(self.numRequests)  
	
			a=self.comboBox.currentText()
			b=self.comboBox_2.currentText()
	
			self.targetSelected(a)
			self.pathSelected(b)
			
			indexpath=self.comboBox_2.findText(b)
			indextarget=self.comboBox.findText(a)

			self.comboBox.setCurrentIndex(indextarget)
			self.comboBox_2.setCurrentIndex(indexpath)

		if self.controller.interceptON():
			r=self.controller.getIntercepted()
			if r:
				dialog = QtGui.QDialog()
				inj=Injector()
				inj.setupUi(dialog)
				inj.setReq(r.getRawRequest())
				dialog.exec_()

				state=inj.getState()
				if state=="drop":
					self.controller.destroyIntercepted(r)
				elif state=="follow":
					str=inj.getRawReq()
					r.setRawRequest(str)
					self.controller.processIntercepted(r)
				else:
					self.controller.processIntercepted(r)
					self.interceptCheck.setChecked(False)
					

					


	

		
	def updateCombos (self,req):
		if self.comboBox.findText(req.urlWithoutPath)==-1:
			self.comboBox.addItem(req.urlWithoutPath)

	def deleteSelected(self):
		a=[]
		for i in self.tableWidget.selectedRanges():
			a+=range (i.topRow(),i.bottomRow()+1)
		a.sort(reverse=True)
	
		self.deleteRequests(a)


	def deleteInView(self):
		indexes=[]

		n=self.tableWidget.rowCount()
		for i in range(n):
			if not self.tableWidget.isRowHidden(i):
				indexes.append(i)

		indexes.reverse()
		self.deleteRequests(indexes)


	def deleteRequests(self,indexes):
		requests=self.controller.getRequests()
		mb = QtGui.QMessageBox ("Deleting Requests","Are you sure you want to delete selected requests ?",QtGui.QMessageBox.Warning,QtGui.QMessageBox.Cancel,QtGui.QMessageBox.Ok,0)
		if mb.exec_()==QtGui.QMessageBox.Ok:
			for i in indexes:
				del requests[i]
				self.tableWidget.removeRow(i)

			self.updateAllStats()
	
	def updateAllStats(self):
		self.controller.updateAllStats()
		requests=self.controller.getRequests()

		self.comboBox.clear()
		self.comboBox.addItem("All")
		
		for i in requests:
			self.updateCombos(i)

		self.targetSelected("All")


	def setNewCookie(self):
		requests=self.controller.getRequests()
		indexes=[]

		n=self.tableWidget.rowCount()
		for i in range(n):
			if not self.tableWidget.isRowHidden(i):
				indexes.append(i)

		for i in indexes:
			requests[i].addHeader("Cookie",str(self.cookieEdit.text()))
			self.tableWidget.setItem(i,3,QtGui.QTableWidgetItem(str(self.cookieEdit.text())))


		
	
	def toogleEditor(self):	
		number= self.stackedWidget.currentIndex()
		if number:
			number= self.stackedWidget.setCurrentIndex(0)
		else:
			number= self.stackedWidget.setCurrentIndex(1)

	def applyRegex (self):
		requests=self.controller.getRequests()
		if str(self.substSrcEdit.text()):
			indexes=[]
	
			n=self.tableWidget.rowCount()
			for i in range(n):
				if not self.tableWidget.isRowHidden(i):
					indexes.append(i)
	
			for i in indexes:
				try:
					requests[i].Substitute(str(self.substSrcEdit.text()),str(self.substDstEdit.text()))
					self.tableWidget.setItem(i,1,QtGui.QTableWidgetItem(requests[i].urlWithoutPath))
					self.tableWidget.setItem(i,2,QtGui.QTableWidgetItem(requests[i].pathWithVariables))
					if requests[i]["Cookie"]:
						self.tableWidget.setItem(i,3,QtGui.QTableWidgetItem(requests[i]["Cookie"]))
				except Exception,a:
					mb = QtGui.QMessageBox ("Error in substitution","ERROR !",QtGui.QMessageBox.Warning,QtGui.QMessageBox.Ok,0,0)
					mb.exec_()
					return

			self.updateAllStats()
					

	def applyConfig (self):
		getsign=str(self.getsignEdit.text())
		headersign=str(self.headersignEdit.text())
		valuesign=str(self.valuesignEdit.text())
		limitpath=str(self.pathlimitEdit.text())
		proxy=str(self.proxyEdit.text())
		proxyport=self.portSpin.value()

		try:
			Proxynet.changePort(proxyport)
		except Exception,a:
			Proxynet.changePort(8008)
			Proxynet.init()
			self.portSpin.setValue(8008)
			mb = QtGui.QMessageBox ("Error",str(a),QtGui.QMessageBox.Critical,QtGui.QMessageBox.Ok,0,0)
			mb.exec_()
			
			
			
		Proxynet.signGET(getsign)
		Proxynet.signHeaders(headersign, valuesign)
		self.controller.limitPath(limitpath)
		if proxy:
			Proxynet.setProxy(proxy)
			self.controller.setProxy(proxy)
		else:
			Proxynet.setProxy(None)
			self.controller.setProxy(None)

	def updateLogData(self):
		data=[]
		for i in self.controller.getPluginLogs():
			i=i.rstrip()
			if len(i):
				data.append(i)
		if len(data):
			self.bgLogTextEdit.append("\r\n".join(data))

##############################################################################################################################
##############################################################################################################################
#########################################       CRAWLER - CRAWLER - CRAWLER        ###########################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

	def startStopCrawling (self,start):
		if start:
			domain=str(self.domainLimitEdit.text()).strip()
			if not domain:
				self.startCrawlButton.setChecked(False)
				mb = QtGui.QMessageBox ("Error","You must specify a domain!!",QtGui.QMessageBox.Critical,QtGui.QMessageBox.Ok,0,0)
				mb.exec_()
				return
			self.controller.startCrawler(domain)
			self.domainLimitEdit.setEnabled(False)
			self.startCrawlButton.setText("Running")
		else:
			self.controller.stopCrawler()
			self.domainLimitEdit.setEnabled(True)
			self.startCrawlButton.setText("Stopped")

	def updateCrawlInfo(self):
		a,b=self.controller.getCrawlerStatus()
		if b==0:
			self.crawlProgress.setValue(0)
			self.progressLabel.setText("Not Running")
		else:
			self.crawlProgress.setValue((a*100)/b)
			self.progressLabel.setText("%d/%d" % (a,b))

		lst=self.controller.getUniqForms()
		if lst:
			for i in lst:
				self.crawlFormsList.addItem(i)

	def uniqFormClicked(self,it):
		webbrowser.open(it.text())

	def resetCrawler(self):
		self.controller.resetCrawler()
		self.startCrawlButton.setChecked(False)
		self.domainLimitEdit.setEnabled(True)
		self.crawlProgress.setValue(0)
		self.crawlFormsList.clear()
		


##############################################################################################################################
##############################################################################################################################
#########################################       REPEATER - REPEATER - REPEATER     ###########################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

	def sendRepeater(self):
		row=self.tableWidget.currentRow()
		if row > -1:
			req=self.controller.getRequests()[row]
			self.requrlEdit.setText(req.schema)
			self.reqTextEdit.setText(req.getAll())
			self.tabWidget.setCurrentIndex(6)

	def performRepeater(self):
		try:
			resp=self.controller.performRepeater(self.requrlEdit.text(),self.reqTextEdit.toPlainText())
		except Exception,a:
			mb = QtGui.QMessageBox ("Error",str(a),QtGui.QMessageBox.Critical,QtGui.QMessageBox.Ok,0,0)
			mb.exec_()
			return


		content=resp.getContent()
		if self.lastResponse==None:
			self.lastResponse=resp.getAll()
		else:
			self.lastResponse=self.newResponse

		self.newResponse=resp.getAll()


		leng=len(content)
		lines=content.count("\n")
		words=len(re.findall("\S+",content))

		m=md5.new()
		m.update(content)
		md5txt=m.hexdigest()

		self.responselenghtEdit.setText(str(leng))
		self.responselinesEdit.setText(str(lines))
		self.responsewordsEdit.setText(str(words))
		self.responsemd5Edit.setText(md5txt)
		
		self.showResponse()

	def showResponse(self):
		if self.newResponse:
			if not self.diffButton.isChecked():
				self.responseTextEdit.setText(self.newResponse)
			else:
				self.responseTextEdit.setHtml(textDiff(self.lastResponse,self.newResponse))
			
			

		
	def funcion_About(self):
		mb = QtGui.QMessageBox ("About","About ProxyStrike v2.1\n\nAUTHOR\n\nCarlos del Ojo Elias (deepbit)\ncdelojo@edge-security.com\n\nEDGE-SECURITY 2009",QtGui.QMessageBox.Information,QtGui.QMessageBox.Ok,0,0)
		mb.exec_()

	def close(self):
		print "Closing..."






def textDiff(a, b):
	"""Takes in strings a and b and returns a human-readable HTML diff."""

	a=a.replace("<","&lt;")
	b=b.replace("<","&lt;")
	a=a.replace(">","&gt;")
	b=b.replace(">","&gt;")

	out = []
	a, b = html2list(a), html2list(b)
	s = difflib.SequenceMatcher(None, a, b)
	for e in s.get_opcodes():
		if e[0] == "replace":
			# @@ need to do something more complicated here
			# call textDiff but not for html, but for some html... ugh
			# gonna cop-out for now
			out.append('<font style="BACKGROUND-COLOR: red">'+''.join(a[e[1]:e[2]]) + '</font><font style="BACKGROUND-COLOR: green">'+''.join(b[e[3]:e[4]])+"</font>")
		elif e[0] == "delete":
			out.append('<font style="BACKGROUND-COLOR: red">'+ ''.join(a[e[1]:e[2]]) + "</font>")
		elif e[0] == "insert":
			out.append('<font style="BACKGROUND-COLOR: green">'+''.join(b[e[3]:e[4]]) + "</font>")
		elif e[0] == "equal":
			out.append(''.join(b[e[3]:e[4]]))
		else: 
			raise "Um, something's broken. I didn't expect a '" + `e[0]` + "'."
	
	html=''.join(out)
	html=html.replace("\n","<br>")
	html=html.replace("\t","&nbsp;&nbsp;&nbsp;&nbsp;")
	return html

def html2list(x, b=0):
	mode = 'char'
	cur = ''
	out = []
	for c in x:
		if mode == 'tag':
			if c == '>': 
				if b: cur += ']'
				else: cur += c
				out.append(cur); cur = ''; mode = 'char'
			else: cur += c
		elif mode == 'char':
			if c == '<': 
				out.append(cur)
				if b: cur = '['
				else: cur = c
				mode = 'tag'
			elif c in string.whitespace: out.append(cur+c); cur = ''
			else: cur += c
	out.append(cur)
	return filter(lambda x: x is not '', out)

