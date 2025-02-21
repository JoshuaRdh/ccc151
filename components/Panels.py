from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, 
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFrame,
    )
from components.Lists import Lists
from components.Forms import Form
from components.QueryBar import QueryBar
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtCore import Qt, QSize

class dataPanel(QWidget) :
    def __init__(self, data, dependencyPanel = None, dependencyPanel2 = None):
        super().__init__()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        self.data = data
        self.myLabel = QLabel(f"{data[0:1].upper()}{data[1:]}")
        self.myLabel.setObjectName("headerLabel")

        self.myList = Lists(data, dependencyPanel, dependencyPanel2)
        self.myQueryBar = QueryBar(self.myList, data)
        self.myForm = Form(self, self.myList, data, dependencyPanel, dependencyPanel2)

        self.addBtn = QPushButton()
        self.addBtn.setIcon(QIcon("addCircle.svg"))
        self.addBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addBtn.setIconSize(QSize(32,32))
        self.addBtn.setFixedHeight(32)
        self.addBtn.setObjectName("headerAddBtn")
        self.addBtn.clicked.connect(lambda: self.myForm.exec())

        # self.feedback.hide()

        header_frame = QFrame()
        header_frame.setFixedHeight(80)
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.myLabel)
        header_layout.addWidget(self.addBtn)
        header_layout.addStretch()
        header_frame.setLayout(header_layout)

        if (self.data == "students") :
            header_frame.setObjectName("studentsHeader")
        elif (self.data == "programs") :
            header_frame.setObjectName("programsHeader")
        elif (self.data == "colleges") :
            header_frame.setObjectName("collegesHeader")

        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(header_frame)
        main_layout.addWidget(self.myQueryBar)
        main_layout.addWidget(self.myList)
        
        self.setLayout(main_layout)
    

    def printSelf(self) : # for debugging
        print('dependencyPanel is', self.data)
    
    
