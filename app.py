import sys, psutil, datetime
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from TaskManagerDialog import Ui_MainWindow

class TaskManagerApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.updateButton.clicked.connect(self.updateContent)
        self.ui.closeButton.clicked.connect(self.killProcess)
        self.today = datetime.date.today()
        self.initData()
        self.addContent()
        self.show()
    
    def initData(self): self.data = self.getAllProcess()

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
    
    def getValueSpinBox(self):
        number = self.ui.spinBox.text()
        return int(number)
    
    def killProcess(self):
        pid = self.getValueSpinBox()
        try:
            process = psutil.Process(pid)
            process.terminate()
            self.updateContent()
        except psutil.Error as error: print(str(error))

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