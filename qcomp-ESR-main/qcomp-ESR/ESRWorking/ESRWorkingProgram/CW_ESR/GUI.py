# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Workspace\ESRWorkingProgram\CW_ESR\GUI\GUI.ui'
#
# Created: Tue Jul 07 17:08:48 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 10, 781, 231))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 260, 271, 281))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayoutWidget = QtGui.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 20, 251, 261))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.startFreqGHzLabel = QtGui.QLabel(self.formLayoutWidget)
        self.startFreqGHzLabel.setObjectName(_fromUtf8("startFreqGHzLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.startFreqGHzLabel)
        self.startFreqLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.startFreqLineEdit.setObjectName(_fromUtf8("startFreqLineEdit"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.startFreqLineEdit)
        self.stopFreqGHzLabel = QtGui.QLabel(self.formLayoutWidget)
        self.stopFreqGHzLabel.setObjectName(_fromUtf8("stopFreqGHzLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.stopFreqGHzLabel)
        self.stopFreqLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.stopFreqLineEdit.setObjectName(_fromUtf8("stopFreqLineEdit"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.stopFreqLineEdit)
        self.stepFreqGHzLabel = QtGui.QLabel(self.formLayoutWidget)
        self.stepFreqGHzLabel.setObjectName(_fromUtf8("stepFreqGHzLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.stepFreqGHzLabel)
        self.stepsLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.stepsLineEdit.setObjectName(_fromUtf8("stepsLineEdit"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.stepsLineEdit)
        self.numOfAvgsLabel = QtGui.QLabel(self.formLayoutWidget)
        self.numOfAvgsLabel.setObjectName(_fromUtf8("numOfAvgsLabel"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.numOfAvgsLabel)
        self.numOfAvgsLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.numOfAvgsLineEdit.setObjectName(_fromUtf8("numOfAvgsLineEdit"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.numOfAvgsLineEdit)
        self.powerSynLabel = QtGui.QLabel(self.formLayoutWidget)
        self.powerSynLabel.setObjectName(_fromUtf8("powerSynLabel"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.powerSynLabel)
        self.powerSynSpinBox = QtGui.QSpinBox(self.formLayoutWidget)
        self.powerSynSpinBox.setMaximum(3)
        self.powerSynSpinBox.setObjectName(_fromUtf8("powerSynSpinBox"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.powerSynSpinBox)
        self.powerAmpLabel = QtGui.QLabel(self.formLayoutWidget)
        self.powerAmpLabel.setObjectName(_fromUtf8("powerAmpLabel"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.powerAmpLabel)
        self.powerAmpSpinBox = QtGui.QSpinBox(self.formLayoutWidget)
        self.powerAmpSpinBox.setMaximum(63)
        self.powerAmpSpinBox.setSingleStep(0)
        self.powerAmpSpinBox.setObjectName(_fromUtf8("powerAmpSpinBox"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.powerAmpSpinBox)
        self.dwellTimeMsLabel = QtGui.QLabel(self.formLayoutWidget)
        self.dwellTimeMsLabel.setObjectName(_fromUtf8("dwellTimeMsLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.dwellTimeMsLabel)
        self.dwellTimeLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.dwellTimeLineEdit.setObjectName(_fromUtf8("dwellTimeLineEdit"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.dwellTimeLineEdit)
        self.powerEstiDBLabel = QtGui.QLabel(self.formLayoutWidget)
        self.powerEstiDBLabel.setObjectName(_fromUtf8("powerEstiDBLabel"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.powerEstiDBLabel)
        self.powerEstiLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.powerEstiLineEdit.setEnabled(False)
        self.powerEstiLineEdit.setObjectName(_fromUtf8("powerEstiLineEdit"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.powerEstiLineEdit)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(290, 260, 221, 281))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.pushButtonStart = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonStart.setGeometry(QtCore.QRect(20, 20, 93, 28))
        self.pushButtonStart.setObjectName(_fromUtf8("pushButtonStart"))
        self.pushButtonStop = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonStop.setEnabled(False)
        self.pushButtonStop.setGeometry(QtCore.QRect(120, 20, 93, 28))
        self.pushButtonStop.setObjectName(_fromUtf8("pushButtonStop"))
        self.textEdit = QtGui.QTextEdit(self.groupBox_2)
        self.textEdit.setGeometry(QtCore.QRect(10, 80, 201, 191))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(10, 60, 53, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(520, 260, 271, 281))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.pushButtonSave = QtGui.QPushButton(self.groupBox_3)
        self.pushButtonSave.setEnabled(False)
        self.pushButtonSave.setGeometry(QtCore.QRect(20, 20, 93, 28))
        self.pushButtonSave.setObjectName(_fromUtf8("pushButtonSave"))
        self.pushButtonDiscard = QtGui.QPushButton(self.groupBox_3)
        self.pushButtonDiscard.setEnabled(False)
        self.pushButtonDiscard.setGeometry(QtCore.QRect(160, 20, 93, 28))
        self.pushButtonDiscard.setObjectName(_fromUtf8("pushButtonDiscard"))
        self.comboBox = QtGui.QComboBox(self.groupBox_3)
        self.comboBox.setGeometry(QtCore.QRect(20, 70, 231, 22))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.pushButtonPrev = QtGui.QPushButton(self.groupBox_3)
        self.pushButtonPrev.setEnabled(False)
        self.pushButtonPrev.setGeometry(QtCore.QRect(20, 120, 93, 28))
        self.pushButtonPrev.setObjectName(_fromUtf8("pushButtonPrev"))
        self.pushButtonNext = QtGui.QPushButton(self.groupBox_3)
        self.pushButtonNext.setEnabled(False)
        self.pushButtonNext.setGeometry(QtCore.QRect(160, 120, 93, 28))
        self.pushButtonNext.setObjectName(_fromUtf8("pushButtonNext"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "CW ESRC", None))
        self.groupBox.setTitle(_translate("MainWindow", "Parameters", None))
        self.startFreqGHzLabel.setText(_translate("MainWindow", "Start Freq (GHz)", None))
        self.stopFreqGHzLabel.setText(_translate("MainWindow", "Stop Freq (GHz)", None))
        self.stepFreqGHzLabel.setText(_translate("MainWindow", "Num of Steps", None))
        self.numOfAvgsLabel.setText(_translate("MainWindow", "Num of Avgs", None))
        self.powerSynLabel.setText(_translate("MainWindow", "Power Syn", None))
        self.powerAmpLabel.setText(_translate("MainWindow", "Power Amp", None))
        self.dwellTimeMsLabel.setText(_translate("MainWindow", "Dwell Time (ms)", None))
        self.powerEstiDBLabel.setText(_translate("MainWindow", "Power Esti (dB)", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Control", None))
        self.pushButtonStart.setText(_translate("MainWindow", "Start", None))
        self.pushButtonStop.setText(_translate("MainWindow", "Stop", None))
        self.label.setText(_translate("MainWindow", "Log", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Data", None))
        self.pushButtonSave.setText(_translate("MainWindow", "Save", None))
        self.pushButtonDiscard.setText(_translate("MainWindow", "Discard", None))
        self.pushButtonPrev.setText(_translate("MainWindow", "Previous", None))
        self.pushButtonNext.setText(_translate("MainWindow", "Next", None))

