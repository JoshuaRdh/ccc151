from PyQt6.QtWidgets import (
    QLineEdit,
    QLabel,
    QComboBox,
    )
import math
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from algo import getOptions

def headerUI_init(self) :
    count = len(self.obj.keys())
    myWidth = math.floor(640/count)

    numberLabel = QLabel()
    numberLabel.setFixedWidth(self.numberWidth)
    self.layout.addWidget(numberLabel)

    for keys in self.obj.keys() :
        label = QLabel(keys)
        if keys == 'name':
            label.setFixedWidth(500)
        elif keys == 'first_name' :
            label.setFixedWidth(200)
        elif keys == 'code' or keys == 'college_code' :
            label.setFixedWidth(math.floor((640-400)/2))
        else:
            label.setFixedWidth(myWidth)

        self.layout.addWidget(label)
    self.layout.addStretch()


def studentUI_init(self) :
    myWidth = math.floor(640 / 6)
    idlabel = QLabel(self.obj['id_no'])
    fnlabel = QLabel(self.obj['first_name'])
    lslabel = QLabel(self.obj['last_name'])
    glabel = QLabel(self.obj['gender'])
    ylabel = QLabel(self.obj['year_level'])
    pclabel = QLabel(self.obj['program_code'])
    arr = [idlabel, fnlabel, lslabel, glabel, ylabel, pclabel]
    for label in arr :
        label.installEventFilter(self)

    idlabel.setFixedWidth(myWidth)
    fnlabel.setFixedWidth(200)
    lslabel.setFixedWidth(myWidth)
    glabel.setFixedWidth(myWidth)
    ylabel.setFixedWidth(myWidth)
    pclabel.setFixedWidth(myWidth)

    numberLabel = QLabel(f"{self.number}")
    numberLabel.setFixedWidth(self.numberWidth)
    self.layout.addWidget(numberLabel)

    self.layout.addWidget(idlabel)
    self.layout.addWidget(fnlabel)
    self.layout.addWidget(lslabel)
    self.layout.addWidget(glabel)
    self.layout.addWidget(ylabel)
    self.layout.addWidget(pclabel)

def programUI_init(self) :
    myWidth = math.floor((640-400) / 2)
    clabel = QLabel(self.obj['code'])
    nlabel = QLabel(self.obj['name'])
    cclabel = QLabel(self.obj['college_code'])
    arr = [clabel, nlabel, cclabel]
    for label in arr:
        label.installEventFilter(self)

    clabel.setFixedWidth(myWidth)
    nlabel.setFixedWidth(500)
    cclabel.setFixedWidth(myWidth)

    numberLabel = QLabel(f"{self.number}")
    numberLabel.setFixedWidth(self.numberWidth)
    self.layout.addWidget(numberLabel)

    self.layout.addWidget(clabel)
    self.layout.addWidget(nlabel)
    self.layout.addWidget(cclabel)

def collegeUI_init(self) :
    myWidth = math.floor((640-400) / 2)
    clabel = QLabel(self.obj['code'])
    nlabel = QLabel(self.obj['name'])
    arr = [clabel, nlabel]
    for label in arr:
        label.installEventFilter(self)

    clabel.setFixedWidth(myWidth)
    nlabel.setFixedWidth(500)

    numberLabel = QLabel(f"{self.number}")
    numberLabel.setFixedWidth(self.numberWidth)
    self.layout.addWidget(numberLabel)

    self.layout.addWidget(clabel)
    self.layout.addWidget(nlabel)
    # self.setLayout(self.layout)


def editStudent_init(self, myWidth, height) :
    self.id_number = QLineEdit()
    self.id_number.setInputMask("9999-9999")
    self.id_number.setText(self.obj['id_no'])
    self.id_number.setFixedWidth(myWidth)
    self.id_number.setFixedHeight(height)
    self.first_name = QLineEdit()
    self.first_name.setText(self.obj['first_name'])
    self.first_name.setFixedWidth(200)
    self.first_name.setFixedHeight(height)
    self.last_name = QLineEdit()
    self.last_name.setText(self.obj['last_name'])
    self.last_name.setFixedWidth(myWidth)
    self.last_name.setFixedHeight(height)
    self.year_level = QComboBox()
    self.year_level.addItems(["1","2","3","4","5"])
    self.year_level.setCurrentText(self.obj['year_level'])
    self.year_level.setFixedWidth(myWidth)
    self.year_level.setFixedHeight(height)
    self.gender = QComboBox()
    self.gender.addItems(["m", "f"])
    self.gender.setCurrentText(self.obj['gender'])
    self.gender.setFixedWidth(myWidth)
    self.gender.setFixedHeight(height)
    self.program_code = QComboBox()
    self.program_code.addItem('none')
    self.program_code.addItems(getOptions.getPrograms())
    self.program_code.setCurrentText(self.obj['program_code'])
    self.program_code.setFixedWidth(myWidth)
    self.program_code.setFixedHeight(height)
    IbeamArr = [self.id_number, self.first_name, self.last_name]
    for input in IbeamArr :
        input.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
    arr = [ self.gender, self.year_level, self.program_code]
    for input in arr :
        input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    self.setObjectName("studentDetailsEdit")

    self.id_number.returnPressed.connect(self.handleSave)
    self.first_name.returnPressed.connect(self.handleSave)
    self.last_name.returnPressed.connect(self.handleSave)

    numberLabel = QLabel(f"{self.number}")
    numberLabel.setFixedWidth(self.numberWidth)
    self.layout.addWidget(numberLabel)

    self.layout.addWidget(self.id_number)
    self.layout.addWidget(self.first_name)
    self.layout.addWidget(self.last_name)
    self.layout.addWidget(self.gender)
    self.layout.addWidget(self.year_level)
    self.layout.addWidget(self.program_code)
    self.layout.addStretch()

def editProgram_init(self, height) :
    myWidth = math.floor((640-400) / 2)

    self.code = QLineEdit()
    self.code.setText(self.obj['code'])
    self.code.returnPressed.connect(self.handleSave)
    self.code.setFixedWidth(myWidth)
    self.code.setFixedHeight(height)
    self.name = QLineEdit()
    self.name.returnPressed.connect(self.handleSave)
    self.name.setText(self.obj['name'])
    self.name.setFixedWidth(500)
    self.name.setFixedHeight(height)
    self.college_code = QComboBox()
    self.college_code.addItem('none')
    self.college_code.addItems(getOptions.getColleges())
    self.college_code.setCurrentText(self.obj['college_code'])
    self.college_code.setFixedWidth(myWidth)

    numberLabel = QLabel(f"{self.number}")
    numberLabel.setFixedWidth(self.numberWidth)
    self.layout.addWidget(numberLabel)
    self.setObjectName("programDetailsEdit")

    self.layout.addWidget(self.code)
    self.layout.addWidget(self.name)
    self.layout.addWidget(self.college_code)
    self.layout.addStretch()

def editCollege_init(self, height) :
    myWidth = math.floor((640-400) / 2)

    self.code = QLineEdit()
    self.code.returnPressed.connect(self.handleSave)
    self.code.setText(self.obj['code'])
    self.code.setFixedWidth(myWidth)
    self.code.setFixedHeight(height)
    self.name = QLineEdit()
    self.name.returnPressed.connect(self.handleSave)
    self.name.setText(self.obj['name'])
    self.name.setFixedWidth(500)
    self.name.setFixedHeight(height)


    numberLabel = QLabel(f"{self.number}")
    numberLabel.setFixedWidth(self.numberWidth)
    self.layout.addWidget(numberLabel)
    self.setObjectName("collegeDetailsEdit")

    self.layout.addWidget(self.code)
    self.layout.addWidget(self.name)
    self.layout.addStretch()