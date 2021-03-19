import sys, psutil, datetime, os
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QTableView, QMessageBox
from TaskManagerDialog import Ui_MainWindow

class TaskManagerApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.updateButton.clicked.connect(self.updateContent)
        self.ui.closeButton.clicked.connect(self.killProcess)
        self.ui.dirButton.clicked.connect(self.getDirectory)
        self.ui.tableWidget.setSelectionBehavior(QTableView.SelectRows)
        self.ui.tableWidget.cellClicked.connect(self.selectProcess)
        self.today = datetime.date.today()
        self.initData()
        self.addContent()
        self.show()
    
    def initData(self): self.data = self.getAllProcess()

    def showError(self, msg):
        if msg == "AccessDenied": msg = msg + '\nIntenta ejecutar el programa como administrador'
        QMessageBox.critical(self, 'Error', '- Tipo de error: ' + msg)
    
    def selectProcess(self, row, column):
        pid = int(self.ui.tableWidget.item(row, 0).text())
        self.currentlyProcessId = pid
        self.ui.spinBox.setValue(pid)

    def setFormatTime(self, time):
        ctime = datetime.datetime.fromtimestamp(time)

        if ctime.date() == self.today:
            ctime = ctime.strftime("%H:%M hs")
        else:
            ctime = ctime.strftime("%b %d")

        return ctime
    
    def getAllProcess(self):
        temp = list()
        for process in psutil.process_iter():
            if(process.status() == 'running'): 
                processId = str(process.pid)
                processName = process.name()
                createTime = self.setFormatTime(process.create_time()) 
                temp.append((processId, processName, createTime))
        return temp
    
    def getDirectory(self):
        try:
            path = psutil.Process(self.currentlyProcessId).cwd()
            os.startfile(path)
            self.updateContent()
        except psutil.Error as error: self.showError(error.__class__.__name__)
    
    def killProcess(self):
        try:
            process = psutil.Process(self.currentlyProcessId)
            process.terminate()
            self.updateContent()
        except psutil.Error as error: self.showError(error.__class__.__name__)

    def updateContent(self):
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        self.data.clear()
        self.data = self.getAllProcess()
        self.addContent()

    def toggleButtons(self):
        self.ui.updateButton.setEnabled(not self.ui.updateButton.isEnabled())
        self.ui.dirButton.setEnabled(not self.ui.dirButton.isEnabled())
        self.ui.closeButton.setEnabled(not self.ui.closeButton.isEnabled())
    
    def addContent(self):
        row = 0
        self.toggleButtons()
        for process in self.data:
            column = 0
            self.ui.tableWidget.insertRow(row)
            for element in process:
                cell = QTableWidgetItem(element)
                self.ui.tableWidget.setItem(row, column, cell)
                column += 1
            row += 1
        self.toggleButtons()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManagerApp()
    window.show()
    sys.exit(app.exec_())