import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class DBSample(QMainWindow):
    def __init__(self):
        super(DBSample, self).__init__()
        uic.loadUi('untitled.ui', self)
        self.con = sqlite3.connect("coffee.db")
        self.modified = {}
        self.tableWidget.itemChanged.connect(self.item_changed)
        self.pushButton.clicked.connect(self.select_data)
        self.pushButton_2.clicked.connect(self.show_window_2)
        self.pushButton_4.clicked.connect(self.save_results)
        self.select_data()

    def show_window_2(self):
        self.w2 = SecondWindow()
        self.w2.show()

    def select_data(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()
        self.row = item.row() + 1

    def save_results(self):
        if self.modified:
            cur = self.con.cursor()
            que = "UPDATE coffee SET\n"
            que += ", ".join([f"{key}='{self.modified.get(key)}'"
                              for key in self.modified.keys()])
            que += "WHERE id = ?"
            cur.execute(que, (self.row,))
            self.con.commit()
            self.modified.clear()


class SecondWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        a = ['молотый', 'в зёрнах']
        b = ['светлая', 'средняя', 'средне-тёмная', 'тёмная', 'очень тёмная']
        self.comboBox.addItems(a)
        self.comboBox_2.addItems(b)
        self.pushButton_3.clicked.connect(self.close1)

    def close1(self):
        self.addition()

    def addition(self):
        self.name = self.lineEdit.text()
        self.degree = self.comboBox_2.currentText()
        self.vid = self.comboBox.currentText()
        self.tasty = self.lineEdit_3.text()
        self.prise = self.lineEdit_4.text()
        self.valume = self.lineEdit_5.text()
        self.finish(self.name, self.degree, self.vid, self.tasty, self.prise, self.valume)

    def finish(self, a, b, c, d, e, f):
        if a != '' and d != '' and e != '' and f != '':
            if e.isdigit() and f.isdigit():
                self.con = sqlite3.connect("coffee.db")
                cur = self.con.cursor()
                cur.execute("""INSERT INTO coffee(title_grade, degreeroasting, processing,
                 descriptiontype, price, volume) VALUES(?, ?, ?, ?, ?, ?)""", (a, b, c, d, e, f)).fetchall()
                self.con.commit()
                self.destroy()
            else:
                self.statusBar().showMessage('Проверьте коректность введённых данных')
        else:
            self.statusBar().showMessage('Пожалуйста введите все поля')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DBSample()
    ex.show()
    sys.exit(app.exec())