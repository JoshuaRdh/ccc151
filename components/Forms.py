from PyQt6.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QPushButton, 
    QVBoxLayout, 
    QComboBox,
    QDialog,
    )
from crudl.student import addStudent
from crudl.program import addProgram
from crudl.college import addCollege
from algo import getOptions
from utils.Utils import formValidated, update_formComboBox, update_filterComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor


class Form(QDialog) :
    def __init__(self, parent, listSection, data, dependencyPanel = None, dependencyPanel2 = None):
        super().__init__(parent)
        self.setObjectName("formDialog")
        self.parent = parent
        self.setWindowTitle(f"add {data[:-1]}")
        self.setFixedWidth(400)
        self.listSection = listSection 
        self.data = data
        self.form_comboBox = dependencyPanel

        if (self.data == 'students') :
            self.studentUI_init()
        elif (self.data == 'programs') :
            self.form_comboBox = dependencyPanel.myForm.program_code
            self.filter_comboBox = dependencyPanel.myQueryBar.filterComboBox
            self.programUI_init()
        elif (self.data == 'colleges') :
            self.form_comboBox = dependencyPanel.myForm.college_code
            self.filter_comboBox = dependencyPanel.myQueryBar.filterComboBox
            self.filter_comboBox2 = dependencyPanel2.myQueryBar.filterComboBox
            self.collegeUI_init()

    def studentUI_init(self) :
        self.id_number = QLineEdit()
        self.id_number.setInputMask("9999-9999")
        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        self.year_level = QComboBox()
        self.year_level.addItems(["1","2","3","4","5"])
        self.gender = QComboBox()
        self.gender.addItems(["m", "f"])
        self.program_code = QComboBox()
        self.program_code.addItem('none')
        self.program_code.setCurrentText('none')
        self.program_code.addItems(getOptions.getPrograms())

        layout = QVBoxLayout()
        form = QFormLayout()

        form.addRow("id number:", self.id_number)
        form.addRow("first name:", self.first_name)
        form.addRow("last name:", self.last_name)
        form.addRow("year level:", self.year_level)
        form.addRow("gender:", self.gender)
        form.addRow("program code:", self.program_code)
        button = QPushButton('Add Student')

        button.clicked.connect(self.handleAdd)

        ibeamArr = [self.id_number, self.first_name, self.year_level]
        for input in ibeamArr :
            input.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        arr = [self.gender, self.program_code, button]
        for input in arr :
            input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        layout.addLayout(form)
        layout.addWidget(button)

        self.setLayout(layout)
    
    def programUI_init(self) :
        self.code = QLineEdit()
        self.name = QLineEdit()
        self.college_code = QComboBox()
        self.college_code.addItem('none')
        self.college_code.setCurrentText('none')
        self.college_code.addItems(getOptions.getColleges())
        layout = QVBoxLayout()
        form = QFormLayout()

        form.addRow("code:", self.code)
        form.addRow("name:", self.name)
        form.addRow("college code:", self.college_code)
        button = QPushButton('Add Program')
        button.clicked.connect(self.handleAdd)
        ibeamArr = [self.code, self.name]
        for input in ibeamArr :
            input.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        arr = [ self.college_code, button]
        for input in arr :
            input.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        layout.addLayout(form)
        layout.addWidget(button)

        self.setLayout(layout)

    def collegeUI_init(self) :
        self.code = QLineEdit()
        self.name = QLineEdit()
        layout = QVBoxLayout()
        form = QFormLayout()

        form.addRow("code:", self.code)
        form.addRow("name:", self.name)
        button = QPushButton('Add College')
        button.clicked.connect(self.handleAdd)
        self.code.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.name.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addLayout(form)
        layout.addWidget(button)

        self.setLayout(layout)
        

    def handleAdd(self) :
        # make input all lowercased maybe
        print(f"handle{self.data}Clicked")
        objToAdd = None
        validated = False
        if (self.data == 'students') : # considers validation
            objToAdd = {
                'id_no':self.id_number.text(),
                'first_name': self.first_name.text().lower().strip(),
                'last_name': self.last_name.text().lower().strip(),
                'year_level': self.year_level.currentText(),
                'gender': self.gender.currentText(),
                'program_code': self.program_code.currentText()
                }
            
            if formValidated(self.data, objToAdd,self, None) :
                addStudent(objToAdd)
                validated = True

        elif (self.data == 'programs') :
            objToAdd = {
                'code' : self.code.text().lower().strip(),
                'name' : self.name.text().lower().strip(),
                'college_code' : self.college_code.currentText(),
            }
            if formValidated(self.data, objToAdd,self, None) :
                addProgram(objToAdd)
                update_formComboBox(self.data, self.form_comboBox)
                update_filterComboBox(self.data, self.filter_comboBox)                
                validated = True
               
        elif (self.data == 'colleges') :
            objToAdd = {
                'code' : self.code.text().lower().strip(),
                'name' : self.name.text().lower().strip(),
            }
            if formValidated(self.data, objToAdd,self, None) :
                addCollege(objToAdd)
                update_formComboBox(self.data, self.form_comboBox)
                update_filterComboBox(self.data, self.filter_comboBox, 1)                
                update_filterComboBox(self.data, self.filter_comboBox2, 2)  
                validated = True

        if validated :
            self.listSection.refactor_rerender()
            self.close()
            self.parent.parent().parent().parent().animationSeq("add")
         #tell passed list to update

