#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QLabel, QMenuBar
import time


class propertyMenu(QMenuBar):
    def __init__(self, myMainMenu, *args, **kwargs):
        super().__init__( *args, **kwargs)

        self.parentMenu = myMainMenu
        self.bar = self.menuBar()
        self.layout = QHBoxLayout()
        self.profile = self.bar.addMenu("Profile")
        self.profile.addAction("Change Password")
