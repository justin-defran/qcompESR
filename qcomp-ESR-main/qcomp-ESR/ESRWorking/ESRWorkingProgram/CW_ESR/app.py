'''
Created on Jul 2, 2015

@author: Kai Zhang
'''
# Modified on Oct. 14, 2019 by Gurudev Dutt
# major issues fixed are converting to python 3 and upgrading to PyQt5

# from GUI.GUI import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from Hardware.Threads import ScanThread
import sys, numpy
from collections import deque
import csv, datetime
import os
import SQL_ESR


Ui_MainWindow,junk = uic.loadUiType('GUI_v3.ui')


class MyGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

       # Image matplotlib widget
        fig=Figure()
        self.ui.mplMap=FigureCanvas(fig)
        self.ui.mplMap.setParent(self.ui.widget)
        self.ui.mplMap.axes=fig.add_subplot(111)
        self.ui.mplMap.setGeometry(QtCore.QRect(QtCore.QPoint(0,0),self.ui.widget.size()))

        #creating defaults for variables before the load_defaults() is called to then reassign them in load_defualts()
        self.startFreq = None
        self.stopFreq = None
        self.NumOfSteps = None
        self.DwellTime = None
        self.NumOfAvgs = None
        self.PowerSyn = None
        self.PowerAmp = None

        self.load_defaults()
       

        self.sThread = ScanThread()

        #creating defaults for new variables added not included in load_defaults()
        #in start() function these variables are reassigned to what is typed their corresponding lineEdit
        self.PowerOutput = None  #previously PowerEsti
        self.AttPower = None
        self.LaserWavelength = 532 #nm
        self.LaserPower = None
        self.FreqAtDip = None  #this value is currently disabled on GUI, will take some more work to impliment

        self.setup_conn()


        self.history = deque(maxlen=5)

        self.myPlot = None
        self.myErrorPlot = None



    def load_defaults(self, fName='defaults.txt'):
        f = open(fName, 'r')
        d = {}
        for line in f.readlines():
            if line[-1] == '\n':
                line = line[:-1]
            [key, value] = line.split('=')
            d[key] = value
        f.close()
        dic = {'StartFreq': self.ui.startFreqLineEdit.setText,
               'StopFreq': self.ui.stopFreqLineEdit.setText,
               'NumOfSteps': self.ui.stepsLineEdit.setText,
               'DwellTime': self.ui.dwellTimeLineEdit.setText,
               'NumOfAvgs': self.ui.numOfAvgsLineEdit.setText,
               'PowerSyn': lambda x: self.ui.powerSynSpinBox.setValue(int(x)),
               'PowerAmp': lambda x: self.ui.powerAmpSpinBox.setValue(int(x))
               }
        for key, value in d.items():
            dic.get(key)(value)

        #reassigning variables to there new default values
        self.startFreq = dic['StartFreq']
        self.stopFreq = dic['StopFreq']
        self.NumOfSteps = dic['NumOfSteps']
        self.DwellTime = dic['DwellTime']
        self.NumOfAvgs = dic['NumOfAvgs']
        self.PowerSyn = dic['PowerSyn']
        self.PowerAmp = dic['PowerAmp']

    def save_defaults(self, fName='defaults.txt'):
        pairList = []
        pairList.append(('StartFreq', self.ui.startFreqLineEdit.text()))
        pairList.append(('StopFreq', self.ui.stopFreqLineEdit.text()))
        pairList.append(('NumOfSteps', self.ui.stepsLineEdit.text()))
        pairList.append(('DwellTime', self.ui.dwellTimeLineEdit.text()))
        pairList.append(('NumOfAvgs', self.ui.numOfAvgsLineEdit.text()))
        pairList.append(('PowerSyn', self.ui.powerSynSpinBox.text()))
        pairList.append(('PowerAmp', self.ui.powerAmpSpinBox.text()))

        ofile = open(fName, 'w')
        for pair in pairList:
            ofile.write(pair[0] + "=" + pair[1] + "\n")
        ofile.close()
#------------------------------------------------------------------------------------------------------

    def setup_conn(self):
        self.ui.pushButtonStart.clicked.connect(self.start)
        self.ui.pushButtonStop.clicked.connect(self.stop)

        self.ui.pushButtonSave.clicked.connect(self.saveData2)
        self.ui.pushButtonDiscard.clicked.connect(self.discard)
        self.ui.pushButtonPrev.clicked.connect(self.prev)
        self.ui.pushButtonNext.clicked.connect(self.__next__)
        self.ui.comboBox.currentIndexChanged.connect(self.plot_history)

        self.sThread.status.connect(self.update_status)
        self.sThread.data.connect(self.update_data)
        self.sThread.stopped.connect(self.stopped)


    def start(self):
        self.ui.pushButtonStart.setEnabled(False)
        self.ui.startFreqLineEdit.setEnabled(False)
        self.ui.stopFreqLineEdit.setEnabled(False)
        self.ui.stepsLineEdit.setEnabled(False)
        self.ui.powerAmpSpinBox.setEnabled(False)
        self.ui.powerSynSpinBox.setEnabled(False)
        self.ui.numOfAvgsLineEdit.setEnabled(False)
        self.ui.dwellTimeLineEdit.setEnabled(False)
        self.ui.pushButtonStop.setEnabled(True)
        #new variables
        self.ui.powerOutputLineEdit.setEnabled(False)
        self.ui.alternatorPowerLineEdit.setEnabled(False)
        self.ui.laserWavelengthLineEdit.setEnabled(False)
        self.ui.laserPowerLineEdit.setEnabled(False)
        self.ui.freqValueAtDipLineEdit.setEnabled(False)


        self.startFreq = float(self.ui.startFreqLineEdit.text())
        self.stopFreq = float(self.ui.stopFreqLineEdit.text())
        self.NumOfSteps = int(self.ui.stepsLineEdit.text())
        self.DwellTime = float(self.ui.dwellTimeLineEdit.text())
        self.NumOfAvgs = int(self.ui.numOfAvgsLineEdit.text())
        self.PowerSyn = int(self.ui.powerSynSpinBox.text())
        self.PowerAmp = int(self.ui.powerAmpSpinBox.text())
        #new variables
        self.PowerOutput = int(self.ui.powerOutputLineEdit.text())
        self.AttPower = int(self.ui.attPowerLineEdit.text())
        self.LaserWavelength = int(self.ui.laserWavelengthLineEdit.text())
        self.LaserPower = int(self.ui.laserPowerLineEdit.text())
        self.FreqAtDip = int(self.ui.freqValueAtDipLineEdit.text())

        #new variables do not need to be passed into sThread
        self.sThread.para = (float(self.ui.startFreqLineEdit.text()),
                             float(self.ui.stopFreqLineEdit.text()),
                             int(self.ui.stepsLineEdit.text()),
                             float(self.ui.dwellTimeLineEdit.text()),
                             int(self.ui.numOfAvgsLineEdit.text()),
                             int(self.ui.powerSynSpinBox.text()),
                             int(self.ui.powerAmpSpinBox.text()))
        self.sThread.start()

        self.data = []
        self.x_arr = numpy.linspace(self.startFreq, self.stopFreq, self.NumOfSteps, endpoint=False)

    def stop(self):
        self.sThread.stop()
        self.ui.pushButtonStop.setEnabled(False)

    def stopped(self, reply):
        self.ui.pushButtonStart.setEnabled(True)
        self.ui.startFreqLineEdit.setEnabled(True)
        self.ui.stopFreqLineEdit.setEnabled(True)
        self.ui.stepsLineEdit.setEnabled(True)
        self.ui.powerAmpSpinBox.setEnabled(True)
        self.ui.powerSynSpinBox.setEnabled(True)
        self.ui.numOfAvgsLineEdit.setEnabled(True)
        self.ui.dwellTimeLineEdit.setEnabled(True)
        #new variables
        self.ui.powerOutputLineEdit.setEnabled(True)
        self.ui.attPowerLineEdit.setEnabled(True)
        self.ui.laserWavelengthLineEdit.setEnabled(True)
        self.ui.laserPowerLineEdit.setEnabled(True)
        self.ui.freqValueAtDipLineEdit.setEnabled(True)
        self.ui.textEdit.append(reply)

        if len(self.data) > 0:
            name = QtCore.QDateTime.currentDateTime().toString()
            if len(self.history) == 5:
                self.ui.comboBox.removeItem(0)
            self.history.append([self.x_arr, self.data])
            self.ui.comboBox.addItem(name)
            self.plot_data_err([self.x_arr, self.data])
        if len(self.history) == 1:
            self.ui.pushButtonSave.setEnabled(True)
            self.ui.pushButtonDiscard.setEnabled(True)

    def update_status(self, reply):
        if reply == 'init':
            self.ui.textEdit.append('Initializing...')
        elif reply == 'success':
            self.ui.textEdit.insertPlainText('Done. Start synchronizing...')
        elif reply == 'cal':
            self.ui.textEdit.insertPlainText('Done.')

    def update_data(self, reply):
        self.data.append(reply)
        avg_data = numpy.mean(self.data, axis=0)
        self.plot_data(self.x_arr, avg_data)

    def plot_data(self, x, y):

        if self.myErrorPlot is not None:
            self.ui.mplMap.figure.clear()
            self.ui.mplMap.axes = self.ui.mplMap.figure.add_subplot(111)
            self.myErrorPlot = None

        if self.myPlot is not None:
            self.myPlot.set_xdata(x)
            self.myPlot.set_ydata(y)
        else:
            self.myPlot, = self.ui.mplMap.axes.plot(x, y)

        self.ui.mplMap.draw()

    def plot_data_err(self, l):
        x_arr = l[0]
        data = l[1]
        y_arr = numpy.mean(data, axis=0)
        y_std = numpy.std(data, axis=0)
        y_err = y_std / numpy.sqrt(float(len(data)))
        self.myPlot = None
        self.ui.mplMap.figure.clear()
        self.ui.mplMap.axes = self.ui.mplMap.figure.add_subplot(111)
        self.myErrorPlot = self.ui.mplMap.axes.errorbar(x_arr, y_arr, y_err)
        self.ui.mplMap.draw()

    def plot_history(self, i):
        if i != -1:
            self.plot_data_err(self.history[i])


    def saveData2(self):
        sql = SQL_ESR.SQL_object()
        sql.insert(self.startFreq, self.stopFreq, self.NumOfSteps, self.DwellTime, self.NumOfAvgs,
                   self.PowerSyn, self.PowerAmp, self.PowerOutput, self.AttPower, self.LaserWavelength,
                   self.LaserPower, self.FreqAtDip, self.x_arr, self.data)
        #x_arr = Frequency, data = scans


    def discard(self):
        i = self.ui.comboBox.currentIndex()
        del self.history[i]
        self.ui.comboBox.removeItem(i)
        i = self.ui.comboBox.currentIndex()
        if i == 0:
            self.ui.pushButtonPrev.setEnabled(False)
        if i == self.ui.comboBox.count() - 1:
            self.ui.pushButtonNext.setEnabled(False)
        self.plot_data_err(self.history[i])

    def prev(self):
        i = self.ui.comboBox.currentIndex() - 1
        self.ui.comboBox.setCurrentIndex(i)
        self.ui.pushButtonNext.setEnabled(True)
        if i == 0:
            self.ui.pushButtonPrev.setEnabled(False)

    def __next__(self):
        i = self.ui.comboBox.currentIndex() + 1
        self.ui.comboBox.setCurrentIndex(i)
        self.ui.pushButtonPrev.setEnabled(True)
        if i == self.ui.comboBox.count() - 1:
            self.ui.pushButtonNext.setEnabled(False)

    def closeEvent(self, event):
        exit(0)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = MyGUI()
    UIWindow.show()
    app.exec_()

