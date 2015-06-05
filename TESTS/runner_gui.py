#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
from PySide.QtGui import QWidget, QCheckBox, QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout, QApplication, QMessageBox
#from PySide.QtCore import *
#import unittest
from unittest import TestSuite, TestLoader, TextTestRunner
from test_container import test_container # or create your own import

class MainWindow(QWidget, TestLoader):
    
    def __init__(self):
        
        QWidget.__init__(self)
        self.cboxList = []
        self.radioLocal = QRadioButton('Run locally', self)
        self.radioLocal.setChecked(True)
        self.radioCloud = QRadioButton('Run in cloud', self)
        hbox = QHBoxLayout()
        hbox.addWidget(self.radioLocal)
        hbox.addWidget(self.radioCloud)
        hbox.addStretch(1)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addSpacing(15)
        
        for item in test_container:
            checkbox = QCheckBox('%s' % item["name"], self)
            checkbox.setToolTip(item["tooltip"])
            vbox.addWidget(checkbox)
            record = {"class":item["class"], "element":checkbox}
            self.cboxList.append(record)
        
        vbox.addSpacing(15)    
        self.runButton = QPushButton('Run Tests', self)
        self.runButton.clicked.connect(lambda: self.generate_list())
        vbox.addWidget(self.runButton)
        
        self.setLayout(vbox)
        self.setWindowTitle("Auto Test GUI")
        self.setGeometry(300, 250, 400, 300)
        
    def generate_list(self):
        self.list = []
        if self.radioLocal.isChecked():
            for el in self.cboxList:
                if el["element"].isChecked() and el["class"] not in self.list:
                    self.list.append(el["class"])
                if not el["element"].isChecked() and el["class"] in self.list: 
                    self.list.remove(el["class"])
        if self.radioCloud.isChecked(): # Update script logic in accordance with your cloud server settings
            for el in self.cboxList:
                if el["element"].isChecked() and el["class"] not in self.list:
                    self.list.append(el["class"])
                if not el["element"].isChecked() and el["class"] in self.list: 
                    self.list.remove(el["class"])
        if self.list == []:
            self.alert_empty_list()
        else: print "The following tests will run: " , self.list
        """self.suite = TestSuite() 
        for test_class in self.list:
            tests = self.loadTestsFromTestCase(test_class)
            self.suite.addTests(tests)
        test_item = TextTestRunner()
        test_item.run(self.suite)"""
        
    def alert_empty_list(self):
        QMessageBox.warning(self, 'Warning', "Please select at least one test", QMessageBox.Ok)
        
            
if __name__ =='__main__':
    try:
        runner_gui = QApplication(sys.argv)
        testWindow = MainWindow()
        testWindow.show()
        runner_gui.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error:", sys.exc_info()[1])
    except SystemExit:
        print("GUI closed")
    except Exception:
        print(sys.exc_info()[1])