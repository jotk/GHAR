#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QMenu, QAction, QWidget, QHBoxLayout, QTabWidget
from propertyWidget import PropertyWidget
from customPropWidget import CustomPropWidget
from PyQt5.QtCore import pyqtSignal, Qt
from functools import partial

class Main_widget(QWidget):
	def __init__(self, properties, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.mainLayout = QHBoxLayout(self)
		self.propertiesWidget = None
		self.scroll = None
		self.properties = properties
		self.createProperties()
		# self.mainLayout.addWidget(self.propertiesWidget)
		self.createCustomAdd()
		self.tabs = QTabWidget()
		self.tabs.addTab(self.propertiesWidget, "Property Analysis")
		self.tabs.addTab(self.customWidget, "Try Other Address")
		self.mainLayout.addWidget(self.tabs)


	def createProperties(self):
		self.propertiesWidget = PropertyWidget(self.properties)
		self.propertiesWidget.createPropWidgets()
		# self.scroll.setWidget(self.propertiesWidget)

	def createCustomAdd(self):
		self.customWidget = CustomPropWidget()
		self.customWidget.submitButton.clicked.connect(
			partial(self.customWidget.createPlot, self.customWidget.streetAdEdit, self.customWidget.cityEdit, self.customWidget.stateEdit, self.customWidget.zipcodeEdit,
					self.customWidget.aliasEdit))




