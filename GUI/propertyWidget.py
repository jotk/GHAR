
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGroupBox, QGraphicsPixmapItem, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from plot2 import PlotCanvasTimeSeriesForecast
from PyQt5.QtCore import pyqtSignal
import locale  # helps with currency formatting

class PropertyWidget(QWidget):

    def __init__(self, properties, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainLayout = QHBoxLayout(self)
        self.properties = properties # list of Property Objects
        self.goToSite = QPushButton("Click here to go to open in browser")
        self.closeOut = QPushButton("Close")
        # self.setStyleSheet("background-color: #2e67d1")
        widg_width = self.frameGeometry().width()
        pic_width = int((widg_width * .25))

        self.logo_pic = QPixmap('images/house_logo.png')
        self.logo_pic = self.logo_pic.scaled(pic_width, pic_width, Qt.KeepAspectRatio)
        self.propertyWidgets = []



    def createPropWidgets(self):
        print("props:", self.properties)
        if self.properties is None or self.properties == []:
            self.picLabel = QLabel()
            self.picLabel.setPixmap(self.logo_pic)
            self.mainLayout.addWidget(self.picLabel)
            self.noProp = QLabel()
            self.noProp.setText("No properties yet. Navigate to the GHAR site and register properties to begin using this tool.")
            self.VLayout = QVBoxLayout(self)
            self.VLayout.addWidget(self.noProp)
            self.HLayout = QHBoxLayout(self)
            self.HLayout.addWidget(self.goToSite)
            self.HLayout.addWidget(self.closeOut)
            self.VLayout.addLayout(self.HLayout)
            self.mainLayout.addLayout(self.VLayout)

        else:
            for prop in self.properties:  # iterate through properties and make a widget for each
                propBox = propertyBox(prop)  # prop = Property object
                propBox.createBox()
                self.propertyWidgets.append(propBox)  # add widget to list of prop widgets
                self.mainLayout.addWidget(propBox)  # display on main Widget


class propertyBox(QWidget):
    """
    QGroupBox with a market forecast chart based off Zillow data and listed information
            :param propertyObj: Property object of the property to create box for
            :param `*args`: The variable args are used for..
            :param `**kwargs`: The keyword arguments are used for..
    """
    api_fail = pyqtSignal()  # init signal that will be emitted on API error
    def __init__(self, propertyObj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainLayout = QVBoxLayout(self)
        self.propertyObj = propertyObj
        self.name = self.propertyObj.propName
        self.groupBox = None
        self.zesWidget = None  # the current home's zestimate info in a widget
        self.vbox = None  # will be the box's layout
        self.similarHomeZesWidget = None  # widget which shows similar avg home info
        self.buttonDisplaySimilarHomeZes = None  # toggle button to show sim avg home info
        self.forecastPlot = None  # holds Canvas with forecast plot
        self.api_fail.connect(self.showError)

        locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )  # need to do to change floats to dollar formatting



    def showError(self):
        """
        Message box that pop up to show that api failed to get info
        :return Nothing:
        """
        print("ERROR")
        QMessageBox.about(self, "Error", "Sorry! API cannot get analytics. Check if address is valid.")


    def createBox(self):
        """
        Creates the QGroupBox which holds property analytics info
        Has QVBoxLayout, adds forecast plots, displays buttons to display zillow information which is stored in propObject
        :return Nothing:
        """
        self.groupBox = QGroupBox(self.propertyObj.propName) # groups widgets with nice shade behind and border
        self.mainLayout.addWidget(self.groupBox)
        self.vbox = QVBoxLayout(self)
        self.groupBox.setLayout(self.vbox)

        # create forecast plot
        self.forecastPlot = self.createForecastPlot() # plot forecast data
        # self.forecastPlot = QLabel()
        self.zesWidget = self.curZesDisplay() # display current zestimate info

        # create widget which holds sim avg home info
        self.similarHomeZesWidget = self.similarHomeZesDisplay()
        self.similarHomeZesWidget.hide() # hide it

        # create button which toggles the similarHomeZesWidget
        self.buttonDisplaySimilarHomeZes = QPushButton('Show Similar Home AVG Zestimate')
        self.buttonDisplaySimilarHomeZes.setCheckable(True)
        self.buttonDisplaySimilarHomeZes.toggle()
        self.buttonDisplaySimilarHomeZes.clicked.connect(self.toggleSimZes)

        # add plot, add button, add sim avg home info
        self.vbox.addWidget(self.forecastPlot)
        self.vbox.addWidget(self.zesWidget)
        self.vbox.addWidget(self.buttonDisplaySimilarHomeZes)
        self.vbox.addWidget(self.similarHomeZesWidget)


    def toggleSimZes(self):
        """
        Handles toggling of the button to display similar home zes and hides/shows similar zes widget
        :return Nothing:
        """
        if self.buttonDisplaySimilarHomeZes.isChecked():
            self.buttonDisplaySimilarHomeZes.setText('Show Similar Home AVG Zestimate')
            self.similarHomeZesWidget.hide()
        else:
            self.buttonDisplaySimilarHomeZes.setText('Hide Similar Home AVG Zestimate')
            self.similarHomeZesWidget.show()

    def similarHomeZesDisplay(self):
        """
        Returns a widget which holds information about the average similar home in the area. Similarity is measured through
        Zillow's api, zillowAPI calculates a weighted average based off scores and values
        :return widget: Widget with grid layout and labels describing similar avg home zestimates, upper_val, lower_val, and change
        """
        widget = QGroupBox()
        gridLayout = QGridLayout()

        simZes = QLabel()
        myFont = QFont()
        myFont.setBold(True)
        simZes.setFont(myFont)
        simZes.setText("Similar home's avg value") # Similar to title, bold

        gridLayout.addWidget(simZes, 0, 0) # add to 0,0

        # Initialize column titles
        typ = QLabel('Type')
        amount = QLabel('Amount in Dollars')
        dif = QLabel('Difference')
        gridLayout.addWidget(typ, 1, 0) # first col
        gridLayout.addWidget(amount, 1, 1) # second col
        gridLayout.addWidget(dif, 1, 2) # third col

        row2Lab = QLabel("Zestimate:") # Row title as label
        zillowZestimate = QLabel() # Row value at col 1
        zillowZestimate.setText(str(self.propertyObj.zillowAnalysis.comp_mean_weighted_sim))
        d2lab = QLabel()  # convert diff to string and round to 2 dec places
        if self.propertyObj.zillowAnalysis.price is not None and self.propertyObj.zillowAnalysis.comp_mean_weighted_sim is not None:
            d2 = self.propertyObj.zillowAnalysis.price - self.propertyObj.zillowAnalysis.comp_mean_weighted_sim # difference between avg and actual home
            d2lab.setText(locale.currency(d2, grouping=True))
        else:
            d2 = "None"
            d2lab.setText(d2)
        if d2 == "None":
            print("Diff is none.")
        elif d2 > 0:
            d2lab.setStyleSheet("color: green;") # green if your home is more expensive
        else:
            d2lab.setStyleSheet("color: red;") # red if your house is less expensive
        gridLayout.addWidget(row2Lab, 2, 0)
        gridLayout.addWidget(zillowZestimate, 2, 1)
        gridLayout.addWidget(d2lab, 2, 2)

        # Repeat above for every row

        row3Lab = QLabel("Upper Valuation:")
        zillowUpper = QLabel()
        zillowUpper.setText(str(self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_high))
        d3lab = QLabel()
        if self.propertyObj.zillowAnalysis.upper_val is not None and self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_high is not None:
            d3 = self.propertyObj.zillowAnalysis.upper_val - self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_high
            d3lab.setText(locale.currency(d3, grouping=True))
        else:
            d3 = "None"
            d3lab.setText(d3)

        if d3 == "None":
            print("Diff is none.")
        elif d3 > 0:
            d3lab.setStyleSheet("color: green;")
        else:
            d3lab.setStyleSheet("color: red;")
        gridLayout.addWidget(row3Lab, 3, 0)
        gridLayout.addWidget(zillowUpper, 3, 1)
        gridLayout.addWidget(d3lab, 3, 2)

        row4Lab = QLabel("Lower Valuation: ")
        zillowLower = QLabel()
        zillowLower.setText(str(self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_low))
        d4lab = QLabel()
        if self.propertyObj.zillowAnalysis.lower_val is not None and self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_low is not None:
            d4 = self.propertyObj.zillowAnalysis.lower_val - self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_low
            d4lab.setText(locale.currency(d4, grouping=True))
        else:
            d4 = "None"
            d4lab.setText(d4)

        if d4 == "None":
            print("Diff is none.")
        elif d4 > 0:
            d4lab.setStyleSheet("color: green;")
        else:
            d4lab.setStyleSheet("color: red;")

        gridLayout.addWidget(row4Lab, 4, 0)
        gridLayout.addWidget(zillowLower, 4, 1)
        gridLayout.addWidget(d4lab, 4, 2)

        row5Lab = QLabel("30 Day Change: ")
        zillowChange = QLabel()
        zillowChange.setText(str(self.propertyObj.zillowAnalysis.comp_change_mean_weighted_sim))
        d5lab = QLabel()
        if self.propertyObj.zillowAnalysis.change_30_days is not None and self.propertyObj.zillowAnalysis.comp_change_mean_weighted_sim is not None:
            d5 = self.propertyObj.zillowAnalysis.change_30_days - self.propertyObj.zillowAnalysis.comp_change_mean_weighted_sim
            d5lab.setText(locale.currency(d5, grouping=True))
        else:
            d5 = "None"
            d5lab.setText(d5)
        if d5 == "None":
            print("Diff is none.")
        elif d5 > 0:
            d5lab.setStyleSheet("color: green;")
        else:
            d5lab.setStyleSheet("color: red;")
        gridLayout.addWidget(row5Lab, 5, 0)
        gridLayout.addWidget(zillowChange, 5, 1)
        gridLayout.addWidget(d5lab, 5, 2)

        widget.setLayout(gridLayout) # add grid to widget
        return widget



    def similarHomeZesDisplay_NOGRID(self):
        """
        Group Box which displays zestimate info for homes which are similar to the currect and their difference
        :return:
        """
        widget = QGroupBox()
        titlerow = QHBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()

        vlayout = QVBoxLayout()

        simZes = QLabel()
        myFont = QFont()
        myFont.setBold(True)
        simZes.setFont(myFont)
        simZes.setText("Similar home's avg value")

        filler1 = QLabel()
        filler2 = QLabel()
        diff = QLabel('Difference Between Own and Avg Similar Home')
        titlerow.addWidget(filler1)
        titlerow.addWidget(filler2)
        titlerow.addWidget(diff)


        row1Lab = QLabel("Zestimate:")
        zillowZestimate = QLabel()
        zillowZestimate.setText(locale.currency(self.propertyObj.zillowAnalysis.comp_mean_weighted_sim, grouping=True))
        if self.propertyObj.zillowAnalysis.price is not None and self.propertyObj.zillowAnalysis.comp_mean_weighted_sim is not None:
            d1 = str(self.propertyObj.zillowAnalysis.price - self.propertyObj.zillowAnalysis.comp_mean_weighted_sim)
        else:
            d1 = "None"
        d1lab = QLabel(d1)
        row1.addWidget(d1lab)
        row1.addWidget(row1Lab)
        row1.addWidget(zillowZestimate)


        row2Lab = QLabel("Upper Valuation:")
        zillowUpper = QLabel()
        zillowUpper.setText(locale.currency(self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_high, grouping=True))
        row2.addWidget(row2Lab)
        row2.addWidget(zillowUpper)

        row3Lab = QLabel("Lower Valuation: ")
        zillowLower = QLabel()
        zillowLower.setText(locale.currency(self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_low, grouping=True))
        row3.addWidget(row3Lab)
        row3.addWidget(zillowLower)

        row4Lab = QLabel("30 Day Change: ")
        zillowChange = QLabel()
        zillowChange.setText(locale.currency(self.propertyObj.zillowAnalysis.comp_change_mean_weighted_sim, grouping=True))
        row4.addWidget(row4Lab)
        row4.addWidget(zillowChange)

        vlayout.addWidget(simZes)
        vlayout.addLayout(titlerow)
        vlayout.addLayout(row1)
        vlayout.addLayout(row2)
        vlayout.addLayout(row3)
        vlayout.addLayout(row4)
        widget.setLayout(vlayout)

        return widget

    def zesDisplay(self):
        """
        Returns a widget which holds information about the average similar home in the area. Similarity is measured through
        Zillow's api, zillowAPI calculates a weighted average based off scores and values
        :return widget: Widget with grid layout and labels describing similar avg home zestimates, upper_val, lower_val, and change
        """
        widget = QGroupBox()
        gridLayout = QGridLayout()

        simZes = QLabel()
        myFont = QFont()
        myFont.setBold(True)
        simZes.setFont(myFont)
        simZes.setText("Home's Zestimate Value") # Similar to title, bold

        gridLayout.addWidget(simZes, 0, 0) # add to 0,0

        # Initialize column titles
        typ = QLabel('Type')
        amount = QLabel('Amount in Dollars')
        dif = QLabel('Difference')
        gridLayout.addWidget(typ, 1, 0) # first col
        gridLayout.addWidget(amount, 1, 1) # second col
        gridLayout.addWidget(dif, 1, 2) # third col

        row2Lab = QLabel("Zestimate:") # Row title as label
        zillowZestimate = QLabel() # Row value at col 1
        zillowZestimate.setText(str(self.propertyObj.zillowAnalysis.comp_mean_weighted_sim))
        d2lab = QLabel()  # convert diff to string and round to 2 dec places
        if self.propertyObj.zillowAnalysis.price is not None and self.propertyObj.zillowAnalysis.comp_mean_weighted_sim is not None:
            d2 = self.propertyObj.zillowAnalysis.price - self.propertyObj.zillowAnalysis.comp_mean_weighted_sim # difference between avg and actual home
            d2lab.setText(locale.currency(d2, grouping=True))
        else:
            d2 = "None"
            d2lab.setText(d2)
        if d2 == "None":
            print("Diff is none.")
        elif d2 > 0:
            d2lab.setStyleSheet("color: green;") # green if your home is more expensive
        else:
            d2lab.setStyleSheet("color: red;") # red if your house is less expensive
        gridLayout.addWidget(row2Lab, 2, 0)
        gridLayout.addWidget(zillowZestimate, 2, 1)
        gridLayout.addWidget(d2lab, 2, 2)

        # Repeat above for every row

        row3Lab = QLabel("Upper Valuation:")
        zillowUpper = QLabel()
        zillowUpper.setText(str(self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_high))
        d3lab = QLabel()
        if self.propertyObj.zillowAnalysis.upper_val is not None and self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_high is not None:
            d3 = self.propertyObj.zillowAnalysis.upper_val - self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_high
            d3lab.setText(locale.currency(d3, grouping=True))
        else:
            d3 = "None"
            d3lab.setText(d3)

        if d3 == "None":
            print("Diff is none.")
        elif d3 > 0:
            d3lab.setStyleSheet("color: green;")
        else:
            d3lab.setStyleSheet("color: red;")
        gridLayout.addWidget(row3Lab, 3, 0)
        gridLayout.addWidget(zillowUpper, 3, 1)
        gridLayout.addWidget(d3lab, 3, 2)

        row4Lab = QLabel("Lower Valuation: ")
        zillowLower = QLabel()
        zillowLower.setText(str(self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_low))
        d4lab = QLabel()
        if self.propertyObj.zillowAnalysis.lower_val is not None and self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_low is not None:
            d4 = self.propertyObj.zillowAnalysis.lower_val - self.propertyObj.zillowAnalysis.comp_mean_weighted_sim_low
            d4lab.setText(locale.currency(d4, grouping=True))
        else:
            d4 = "None"
            d4lab.setText(d4)

        if d4 == "None":
            print("Diff is none.")
        elif d4 > 0:
            d4lab.setStyleSheet("color: green;") # green for pos
        else:
            d4lab.setStyleSheet("color: red;")

        gridLayout.addWidget(row4Lab, 4, 0)
        gridLayout.addWidget(zillowLower, 4, 1)
        gridLayout.addWidget(d4lab, 4, 2)

        row5Lab = QLabel("30 Day Change: ")
        zillowChange = QLabel()
        zillowChange.setText(str(self.propertyObj.zillowAnalysis.comp_change_mean_weighted_sim))
        d5lab = QLabel()
        if self.propertyObj.zillowAnalysis.change_30_days is not None and self.propertyObj.zillowAnalysis.comp_change_mean_weighted_sim is not None:
            d5 = self.propertyObj.zillowAnalysis.change_30_days - self.propertyObj.zillowAnalysis.comp_change_mean_weighted_sim
            d5lab.setText(locale.currency(d5, grouping=True))
        else:
            d5 = "None"
            d5lab.setText(d5)
        if d5 == "None":
            print("Diff is none.")
        elif d5 > 0:
            d5lab.setStyleSheet("color: green;")
        else:
            d5lab.setStyleSheet("color: red;")
        gridLayout.addWidget(row5Lab, 5, 0)
        gridLayout.addWidget(zillowChange, 5, 1)
        gridLayout.addWidget(d5lab, 5, 2)

        widget.setLayout(gridLayout) # add grid to widget
        return widget

    def curZesDisplay(self):
        """
        Creates and returns a widget which holds the zestimate information for the current home
        :return myWidget: widget which holds home zestimate info
        """
        myWidget = QWidget()
        vlayout = QVBoxLayout()

        cureentHomeZes = QLabel()
        myFont=QFont()
        myFont.setBold(True)
        cureentHomeZes.setFont(myFont)
        cureentHomeZes.setText("Home's current value")

        zillowZestimate = QLabel()
        if self.propertyObj.zillowAnalysis.price is not None:
            zillowZestimate.setText("Zestimate: " + locale.currency(self.propertyObj.zillowAnalysis.price, grouping=True ))
        else:
            zillowZestimate.setText("Zestimate: None")

        zillowUpper = QLabel()
        if self.propertyObj.zillowAnalysis.upper_val is not None:
            zillowUpper.setText("Upper Valuation: " + locale.currency(self.propertyObj.zillowAnalysis.upper_val, grouping=True))
        else:
            zillowZestimate.setText("Upper Valuation: None")

        zillowLower = QLabel()
        if self.propertyObj.zillowAnalysis.lower_val is not None:
            zillowLower.setText("Lower Valuation: "+ locale.currency(self.propertyObj.zillowAnalysis.lower_val, grouping=True))
        else:
            zillowZestimate.setText("Lower Valuation: None")

        zillowChange = QLabel()
        if self.propertyObj.zillowAnalysis.change_30_days is not None:
            zillowChange.setText("30 Day Change: "+ locale.currency(self.propertyObj.zillowAnalysis.change_30_days, grouping=True))
        else:
            zillowZestimate.setText("30 Day Change: None")


        vlayout.addWidget(cureentHomeZes)
        vlayout.addWidget(zillowZestimate)
        vlayout.addWidget(zillowUpper)
        vlayout.addWidget(zillowLower)
        vlayout.addWidget(zillowChange)
        myWidget.setLayout(vlayout)
        return myWidget

    def createForecastPlot(self):
        """
        Creates a canvas which holds the future prediction of market after 2 years given
        property neighborhood (as returned by zillow api), city, and state
        :return Widget(Canvas or Label): Canvas is successful, Label if failed
        """
        neighborhood = self.propertyObj.zillowAnalysis.region
        state = self.propertyObj.zillowAnalysis.state
        city = self.propertyObj.zillowAnalysis.city
        homeType = self.propertyObj.zillowAnalysis.homeType
        try:
            pricePlot = PlotCanvasTimeSeriesForecast(neighborhood, state, city, homeType)
            return pricePlot.getPlot()
        except Exception: # API Didn't Work
            self.api_fail.emit()
            lab = QLabel()
            lab.setText("Plot cannot be rendered")
            return lab



















