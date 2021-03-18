import sys, psutil, datetime
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from Qtable import Ui_MainWindow

class QTableWidgeApp(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
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
            
    def addContent(self):
        row = 0
        for process in self.data:
            column = 0
            self.ui.tableWidget.insertRow(row)
            for element in process:
                cell = QTableWidgetItem(element)
                self.ui.tableWidget.setItem(row, column, cell)
                column += 1
            row += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QTableWidgeApp()
    window.show()
    sys.exit(app.exec_())