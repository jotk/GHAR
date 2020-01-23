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

class PlotCanvas(FigureCanvas):
    """
    Plots the analytics using matplotlib.
    This class creates a figure with time on the x-axis and price out of max price on the y-axis.
    """
    def __init__(self, filepath="data/SalesSFR.csv",  width=5, height=4, dpi=100):
        """
        Constructor for PlotCanvas class.

        Init parameters:
            width of plot (default set as 5)
            height of plot (default set as 4)
            dots per inch (default set as 100)

        Returns:
            None.
        """
        self.filepath = filepath
        fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
        self.draw()


    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'd-g')
        ax.set_title('Market Change')

    def plotForecast(self):
        filepath = self.filepath
        df = pd.read_csv(filepath)
        State = "TX"
        City = "Dallas"
        RegionName = "Northeast Dallas"
        Row = None
        for index, i in df.iterrows():  # i is the row value
            if i["RegionName"] == RegionName and i["City"] == City and i["State"] == State:
                Row = i
                break
        dict = {'date': [], 'ZHVI': []}
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
        ZHVI_prophet = self.figure.add_subplot(111)
        ZHVI_prophet = fbprophet.Prophet(changepoint_prior_scale=0.65)
        ZHVI_prophet.fit(dfclean)
        ZHVI_forcast = ZHVI_prophet.make_future_dataframe(periods=24, freq='M')
        ZHVI_forcast = ZHVI_prophet.predict(ZHVI_forcast)
        ZHVI_prophet.plot(ZHVI_forcast, xlabel='Time', ylabel='Zillow House Value Index')
        plt.title('ZHVI for SFHs vs Time with 2 Year Forecast')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())