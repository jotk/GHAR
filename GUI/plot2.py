import sys

from PyQt5.QtWidgets import QApplication, QMainWindow,  QSizePolicy,QPushButton

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats

import fbprophet

class PlotCanvasTimeSeriesForecast():
	"""
	Plots the analytics using matplotlib.
	This class creates a figure with time on the x-axis and price out of max price on the y-axis.
	"""
	def __init__(self, region, city, state, homeType):
		"""
		Constructor for PlotCanvas class.

		Init parameters:
			width of plot (default set as 5)
			height of plot (default set as 4)
			dots per inch (default set as 100)

		Returns:
			None.
		"""
		self.homeType = homeType
		if homeType == 'SingleFamily' or homeType == 'None':
			self.filepath = "data/SalesSFR.csv"
		else:
			self.filepath = "data/SalesCondos.csv"
		# self.fig = Figure()
		self.fig = self.plotForecast(region, city, state)

		self.fig.tight_layout()
		self.canvas = FigureCanvas(self.fig)

		# self.plot()
		self.canvas.draw()

	def getPlot(self):
		return self.canvas


	def plotForecast(self, region, state, city):
		"""
			Creates a matplotlib figure which makes predictions based off time series data
			:return:
		"""
		df = pd.read_csv(self.filepath)
		fig, ax = plt.subplots()
		State = state
		City = city
		RegionName = region
		Row = None
		for index, i in df.iterrows():  # i is the row value
			if i["RegionName"] == RegionName and i["City"] == City and i["State"] == State: # find the correct region, city, state
				Row = i
				break
		if Row is None:
			raise Exception("Zillow has no data for your input, sorry")
		columns = []
		count = 0
		for col in df.columns:
			if count >= 7:
				x = col
				x = col + "-01"
				columns.append(x)
			else:
				columns.append(col)
			count += 1
		dict = {'date': [], 'ZHVI': []} # holds the dates and zillow estimates
		for index, val in enumerate(Row):
			if index >= 7:
				if math.isnan(val) != True:
					x = dict["date"]
					x.append(columns[index])
					dict["date"] = x
					x = dict["ZHVI"]
					x.append(val)
					dict["ZHVI"] = x
		dfclean = pd.DataFrame(dict)
		dfclean = dfclean.rename(columns={'date': 'ds', 'ZHVI': 'y'})
		ZHVI_prophet = fbprophet.Prophet(changepoint_prior_scale=0.65)
		ZHVI_prophet.fit(dfclean)
		ZHVI_forcast = ZHVI_prophet.make_future_dataframe(periods=24, freq='M')
		ZHVI_forcast = ZHVI_prophet.predict(ZHVI_forcast)
		x = ZHVI_prophet.plot(ZHVI_forcast, xlabel='Time', ylabel='Zillow House Value Index')
		plt.title('ZHVI for ' + self.homeType + ' in ' + region + ' vs Time with 2 Year Forecast')
		return x



if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
