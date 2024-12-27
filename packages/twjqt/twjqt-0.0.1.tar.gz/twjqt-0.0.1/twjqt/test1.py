import sys
from PyQt5.QtWidgets import QApplication,QWidget

if __name__ == '__main__':
    app=QApplication(sys.argv)

    mywindows=QWidget()

    mywindows.setWindowTitle('战地5')
    mywindows.resize(600,500)
    mywindows.move(300,300)

    mywindows.show()

    app.exec_()