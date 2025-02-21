from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout,
    QStackedWidget,
    QFrame,
    QLabel,
    )
from PyQt6.QtCore import Qt, QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtGui import QKeySequence, QShortcut, QCursor
import threading
import sys
from components.Panels import dataPanel

class QWindow(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.setGeometry(0,100, 1200, 1000)
        self.setWindowTitle('Main')
        self.state = 0
        frame_width = self.width()
        frame_height = self.height()
        print(f"Frame Size: {frame_width}x{frame_height}")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)
    

        switchPanel = QFrame()
        changePanelLayout = QHBoxLayout()
        self.studentsBtn = QPushButton("Students")
        self.programsBtn = QPushButton("Programs")
        self.collegesBtn = QPushButton("Colleges")
        self.studentsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.programsBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.collegesBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        panelHeight = 40
        self.studentsBtn.setFixedHeight(panelHeight)
        self.programsBtn.setFixedHeight(panelHeight)
        self.collegesBtn.setFixedHeight(panelHeight)

        with open("styles.qss", "r") as f:
            self.qss = f.read()
            self.setStyleSheet(self.qss)
        self.studentsBtn.setObjectName("studentPressed")
        self.programsBtn.setObjectName("programsBtn")
        self.collegesBtn.setObjectName("collegesBtn")

        self.studentsBtn.clicked.connect(lambda: self.changePanel(0))
        self.programsBtn.clicked.connect(lambda: self.changePanel(1))
        self.collegesBtn.clicked.connect(lambda: self.changePanel(2))

        changePanelLayout.addWidget(self.studentsBtn)
        changePanelLayout.addWidget(self.programsBtn)
        changePanelLayout.addWidget(self.collegesBtn)
        changePanelLayout.setSpacing(0)
        changePanelLayout.setContentsMargins(0,0,0,0)
        switchPanel.setLayout(changePanelLayout)

        self.studentPanel = dataPanel("students")
        self.programPanel = dataPanel("programs", self.studentPanel)
        self.collegePanel = dataPanel("colleges", self.programPanel, self.studentPanel)

        self.myPanels = QStackedWidget()
        self.myPanels.addWidget(self.studentPanel)
        self.myPanels.addWidget(self.programPanel)
        self.myPanels.addWidget(self.collegePanel)

        # myTestBtn = QPushButton('test')
        # myTestBtn.clicked.connect(lambda: self.animationSeq('edit'))

        main_layout.addWidget(switchPanel)
        main_layout.addWidget(self.myPanels)
        # main_layout.addStretch()        

        centralWidget = QWidget(self)

        centralWidget.setLayout(main_layout)

        self.setCentralWidget(centralWidget)

        self.feedback = QLabel(self)
        self.feedback.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.feedback.raise_()
        self.feedback.hide()


        exit_shortcut = QShortcut(QKeySequence('esc'), self)
        exit_shortcut.activated.connect(self.close)

    
    def changePanel(self, index) :
        arr = [self.studentsBtn, self.programsBtn, self.collegesBtn]
        for i in range(len(arr)) : # prolly can be better lol
            if i == index :
                if i == 0 :
                    arr[i].setObjectName("studentPressed")
                elif i == 1 :
                    arr[i].setObjectName("programPressed")
                elif i == 2:
                    arr[i].setObjectName("collegePressed")

            else :
                if i == 0 : 
                    arr[i].setObjectName("studentsBtn")
                elif i == 1 :
                    arr[i].setObjectName("programsBtn")
                else :
                    arr[i].setObjectName("collegesBtn")
        self.setStyleSheet(self.qss)

        self.myPanels.setCurrentIndex(index)

    def animationSeq(self, what) :
        if what == "add" :
            self.feedback.setText('added')
            self.feedback.setStyleSheet("max-width: 100px; max-height: 80px; background-color: green;border-radius:12px; font-weight: bold")
        elif what == "edit" :
            self.feedback.setText('edited')
            self.feedback.setStyleSheet("max-width: 100px; max-height: 80px; background-color: orange;border-radius:12px; font-weight: bold")
        elif what == "delete" :
            self.feedback.setText('deleted')
            self.feedback.setStyleSheet("max-width: 100px; max-height: 80px; background-color: red;border-radius:12px; font-weight: bold")

        self.feedback.show()
        self.anim = QPropertyAnimation(self.feedback, b"pos")
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.anim.setStartValue(QPoint(555,1000))

        self.anim.setEndValue(QPoint(555, 950))
        self.anim.setDuration(400)
        threading.Timer(1, lambda: self.feedback.hide()).start()
        self.anim.start()


if __name__ == "__main__":
    app = QApplication([])
    main_window = QWindow()
    main_window.show()
    sys.exit(app.exec())


#todo: option btn
#todo: styling
#todo: take header away from details