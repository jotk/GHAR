
from PyQt5.QtWidgets import QMenu, QAction, QWidget, QHBoxLayout, QTabWidget, QVBoxLayout, QPushButton, QFormLayout, QMessageBox, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal
from property import Property
from propertyWidget import propertyBox
from functools import partial

class CustomPropWidget(QWidget):
    """
    Widget to insert custom user address through a form, renders the analysis of the property when form is submitted.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prop = None
        self.form = QWidget()  # the form to submit the plot info
        self.plot = QWidget()  # the result of the address being processed, widget with all the info
        self.streetAdEdit = None
        self.zipcodeEdit = None
        self.stateEdit = None
        self.cityEdit = None
        self.aliasEdit = None
        self.submitButton = None
        self.formLayout = None
        self.createForm()  # create the form, init the form components
        self.mainLayout = QVBoxLayout(self)  # vertical layout
        self.mainLayout.addWidget(self.form)  # add form to main layout


    def createForm(self):
        """
        Creates a form layout and adds lineEdits for address, city, state, zipcode, and alias and submit button. Sets the self.form to hold
        the layout
        :return: Nothing
        """
        self.formLayout = QFormLayout()  # create form layout

        self.streetAdEdit = QLineEdit()
        self.streetAdEdit.setPlaceholderText("1234 Innovation Dr.")
        self.zipcodeEdit = QLineEdit()
        self.zipcodeEdit.setPlaceholderText("80302")
        self.stateEdit = QLineEdit()
        self.stateEdit.setPlaceholderText("CO")
        self.cityEdit = QLineEdit()
        self.cityEdit.setPlaceholderText("Boulder")
        self.aliasEdit = QLineEdit()
        self.aliasEdit.setPlaceholderText("**optional**")
        self.submitButton = QPushButton("Analyze")

        self.formLayout.addWidget(QLabel("Enter property information below to see analysis"))
        self.formLayout.addRow(QLabel("Property Alias: "), self.aliasEdit)
        self.formLayout.addRow(QLabel("Street Address: "), self.streetAdEdit)
        self.formLayout.addRow(QLabel("City: "), self.cityEdit)
        self.formLayout.addRow(QLabel("State: "), self.stateEdit)
        self.formLayout.addRow(QLabel("Zipcode: "), self.zipcodeEdit)
        self.formLayout.addRow(self.submitButton)

        self.form.setLayout(self.formLayout)  # add the layout to the form widget

    def changeProperty(self):
        """
        Will hide the property and show the form again.
        :return:
        """
        self.form.show()
        self.propObj = None
        self.clearForm() # will clean out all of the entries already exisitng in the form
        self.prop.hide()

    def clearForm(self):
        self.streetAdEdit.clear()
        self.zipcodeEdit.clear()
        self.stateEdit.clear()
        self.cityEdit.clear()
        self.aliasEdit.clear()

    def createPlot(self, streetAddress, city, state, zipcode, alias):
        """
        Creates the analysis plot based on given address, city, state, zipcode, and alias.
        :param streetAddress: street address as string
        :param city: city as string
        :param state: state as two letter string ex. "CO"
        :param zipcode: zipcode as an int
        :param alias: prop alias as  string
        :return: Nothing
        """
        self.propObj = Property()  # property object
        self.propObj.setInfo(streetAddress.text(), city.text(), state.text(), zipcode.text(), alias.text())  # manually set info instead of getting from db
        try:
            self.propObj.initZillowInfo("X1-ZWz17njsl1wx6z_3mmvk")  # replace with key in env
            self.prop = propertyBox(self.propObj)
            self.prop.createBox()
            self.mainLayout.addWidget(self.prop)
            self.resubmitform = QPushButton("Change Property")
            self.resubmitform.clicked.connect(self.changeProperty)
            self.prop.vbox.addWidget(self.resubmitform)
            self.form.hide()
        except Exception as e:
            print(e)
            # create a popup window with the error and keep form as is
            QMessageBox.about(self, "Error", "Sorry! API cannot get full analytics. Check if address is valid.")



