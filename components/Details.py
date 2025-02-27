from PyQt6.QtWidgets import (
    QPushButton, 
    QHBoxLayout,
    QFrame,
    QMenu,
    QMessageBox,
    QLabel,
    QLineEdit,
    )
import math
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QCursor, QIcon
from algo import getOptions
from crudl.student import editStudent, delStudent
from crudl.program import editProgram, delProgram
from crudl.college import editCollege, delCollege
from utils.Utils import (update_formComboBox, update_filterComboBox, formValidated)
from utils import initDetails

class Details(QFrame):
    def __init__(self, obj, data = 'header', dependencyPanel = None, rerender = None, dependencyPanel2= None, number = None, setFocusedIndex = None, index = None):
        super().__init__()

        self.number = number
        self.numberWidth = 40 # what's this - used in initDetails, its row number

        self.setFocusedIndex = setFocusedIndex
        self.index = index

        self.obj = obj
        self.data = data
        self.dependencyPanel = dependencyPanel
        self.rerender = rerender #rerender changes (rerender from list)
        self.form_comboBox = None # this comboBox is comboBox in forms
        self.filter_comboBox = None # this comboBox is comboBox in queryBar
        self.filter_comboBox2 = None # same thing, but in students querybar when college
        if (self.data == 'programs') :
            self.form_comboBox = dependencyPanel.myForm.program_code
            self.filter_comboBox = dependencyPanel.myQueryBar.filterComboBox
        elif (self.data == 'colleges') :
            self.form_comboBox = dependencyPanel.myForm.college_code
            self.filter_comboBox = dependencyPanel.myQueryBar.filterComboBox
            self.filter_comboBox2 = dependencyPanel2.myQueryBar.filterComboBox

        if (self.data == "students") :
            self.highlightColor = "#2a5ea1"
            self.textColor = "#144272"
        elif (self.data == "programs") :
            self.highlightColor = "#c44e4c"
            self.textColor = "#a1413f"
        elif (self.data == "colleges") :
            self.highlightColor = "#5ea398"
            self.textColor = "#477a72"

        self.frameStyles = """
            QFrame{
                padding-top: 4.5px;
                padding-bottom: 4.5px;
                border-bottom: 0.5px solid #1c172b;

            }
            QFrame > QLabel {
                border: none;
            }
            QFrame > QLineEdit {
                border: none;
                border-bottom: 0.5px solid #144272;
            }"""

        self.setStyleSheet(self.frameStyles)
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(30)
        self.setLayout(self.layout)


        self.setLayout(self.layout)
        self.self_init()

        if data != 'header' :
            self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

            self.labelHighlight = QLabel(self)
            self.labelHighlight.setObjectName("labelHighlight")
            self.labelHighlight.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            self.labelHighlight.installEventFilter(self)
            self.labelHighlight.setStyleSheet(f"color:{self.textColor};background-color:white; border:1px solid {self.highlightColor}")
            self.labelHighlight.hide()
            self.labelHighlight.raise_()


    def focusInEvent(self, event):
        focused_frameStyles = f"""
            QFrame{{
                padding-top: 4.5px;
                padding-bottom: 4.5px;
                border-bottom: 0.5px solid #1c172b;
                background-color: {self.highlightColor};
                color: white;
            }}
            QFrame > QLabel {{
                border: none;
                background-color:  {self.highlightColor};
                color: white;
            }}
            QFrame > QLineEdit {{
                border: none;
                background-color: {self.highlightColor};
                border-bottom: 0.5px solid white;
                color: white;
            }}"""
        self.setStyleSheet(focused_frameStyles)
        super().focusInEvent(event)  # Call the parent method

    def focusOutEvent(self, event):
        self.setStyleSheet(self.frameStyles)
        super().focusOutEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.FocusIn :
            self.focusInEvent(event)
        elif event.type() == QEvent.Type.FocusOut :
            self.focusOutEvent(event)
            if  obj.objectName() == "labelHighlight" :
                self.labelHighlight.hide()
        elif event.type() == QEvent.Type.MouseButtonDblClick :
            if obj is not self.labelHighlight : # to avoid call when it itself is dblclicked
                
                global_pos = obj.mapToGlobal(obj.rect().topLeft())
                selfpos = self.mapToGlobal(obj.rect().topLeft())
                self.labelHighlight.setText(obj.text())
                self.labelHighlight.adjustSize()
                self.labelHighlight.show()
                self.labelHighlight.setFocus()
 
                self.labelHighlight.move(global_pos.x() - selfpos.x(),5)

        return super().eventFilter(obj, event)


    def keyPressEvent(self, event):
        if self.data == "header" : return
        if event.key() == Qt.Key.Key_Up:
            index = self.index
            # index = 1 if self.index == 0 else self.index
            self.setFocusedIndex(index)
            super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_Down:
            index = self.index + 2
            self.setFocusedIndex(index)
            super().keyPressEvent(event)

    def self_init(self) :

        if (self.data == 'students') :
            initDetails.studentUI_init(self)
            self.optionBtn = QPushButton()
            self.optionBtn.setIcon(QIcon("assets/optionDots_student.svg"))
        elif (self.data == 'programs') :
            initDetails.programUI_init(self)
            self.optionBtn = QPushButton()
            self.optionBtn.setIcon(QIcon("assets/optionDots_program.svg"))
        elif (self.data == 'colleges') :
            initDetails.collegeUI_init(self)
            self.optionBtn = QPushButton()
            self.optionBtn.setIcon(QIcon("assets/optionDots_college.svg"))
        else :
            initDetails.headerUI_init(self)

        if self.data != 'header' :
            self.myOptionMenu = QMenu(self)
            self.myOptionMenu.setStyleSheet(f"background-color:{self.highlightColor}; color: white")

            self.optionBtn.setStyleSheet("max-width: 50px; max-height: 20px; border:none;margin-right: 8px;border-radius:10px;")
            self.optionBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

            self.optionBtn.adjustSize()
            self.optionBtn.clicked.connect(self.showMenu)

            edit = self.myOptionMenu.addAction('Edit')
            delete = self.myOptionMenu.addAction('Delete')

            edit.triggered.connect(self.handleEdit)
            delete.triggered.connect(self.hanDel)
            self.layout.addStretch()
            self.layout.addWidget(self.optionBtn)

    def showMenu(self) :
        # pos = QCursor.pos()
        pos = self.optionBtn.mapToGlobal(self.optionBtn.rect().topRight())
        self.myOptionMenu.exec(pos)
    
    def handleEdit(self) :
        myWidth = math.floor(640 / 6)
        height = 17
        clear_layout(self.layout)
        if (self.data == 'students') :
            initDetails.editStudent_init(self, myWidth, height)
        
        elif (self.data == 'programs') :
            initDetails.editProgram_init(self, height)

        elif (self.data == 'colleges') :
           initDetails.editCollege_init(self, height)

        self.saveBtn = QPushButton('save')
        self.saveBtn.clicked.connect(self.handleSave)
        self.saveBtn.setMaximumHeight(height)
        self.layout.addWidget(self.saveBtn)
        self.cancelBtn = QPushButton('cancel')
        self.cancelBtn.clicked.connect(self.handleCancel)
        self.cancelBtn.setMaximumHeight(height)
        self.layout.addWidget(self.cancelBtn)
        self.saveBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.cancelBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        buttonStyles = f"""
        QPushButton {{
            background-color: white;
            color: {self.textColor};
            border: 1px solid {self.textColor};
            padding-left: 3px;
            padding-right: 3px;
            border-radius: 5px;
        }}
        QPushButton:hover {{
            background-color: {self.textColor};
            color: white;
            border: 1px solid {self.textColor};
            padding-left: 3px;
            padding-right: 3px;
            border-radius: 5px;
        
        }}
        """
        self.saveBtn.setStyleSheet(buttonStyles)
        self.cancelBtn.setStyleSheet(buttonStyles)
    
    def handleSave(self) : #reused from Forms handleAdd
        print(f"handle{self.data}Clicked")
        objToEdit = None
        validated = False
        if (self.data == 'students') : #students
            objToEdit = {
                'id_no':self.id_number.text(),
                'first_name': self.first_name.text().lower(),
                'last_name': self.last_name.text().lower(),
                'year_level': self.year_level.currentText(),
                'gender': self.gender.currentText(),
                'program_code': self.program_code.currentText()
                }

            if formValidated(self.data, objToEdit, self,self.obj ) :
                editStudent(self.obj['id_no'],objToEdit) #updates student with idno in csv
                self.obj = objToEdit #updates self obj
                validated = True
                self.handleCancel()
                self.rerender()
            
        elif (self.data == 'programs') : #programs
            objToEdit = {
                'code' : self.code.text().lower(),
                'name' : self.name.text().lower(),
                'college_code' : self.college_code.currentText(),
            }
            if formValidated(self.data, objToEdit, self, self.obj) :
                editProgram(self.obj['code'], objToEdit)
                self.obj = objToEdit
                self.handleCancel()
                update_formComboBox(self.data, self.form_comboBox)
                update_filterComboBox(self.data, self.filter_comboBox)                
                validated=True
                self.dependencyPanel.myList.refactor_rerender()
                self.rerender()
                # every edit should sync with comboBoxes
        elif (self.data == 'colleges') : #colleges
            objToEdit = {
                'code' : self.code.text().lower(),
                'name' : self.name.text().lower(),
            }
            if formValidated(self.data, objToEdit, self, self.obj) :
                editCollege(self.obj['code'], objToEdit)
                self.obj = objToEdit
                self.handleCancel()
                update_formComboBox(self.data, self.form_comboBox)
                update_filterComboBox(self.data, self.filter_comboBox, 1)                
                update_filterComboBox(self.data, self.filter_comboBox2, 2)      
                validated= True          
                self.dependencyPanel.myList.refactor_rerender()
                self.rerender()
        if validated :
            self.parent().parent().parent().parent().parent().parent().animationSeq("edit")
                # every edit should sync with comboBoxes

    def handleCancel(self) :
        clear_layout(self.layout)
        self.self_init()
        self.labelHighlight.raise_()

    def hanDel(self) :
        msgbox = QMessageBox(self)
        msgbox.setStyleSheet("""
                            QMessageBox {
                                background-color: #a1413f;
                             }
                             QMessageBox * {
                                background-color: white;
                                color:  #a1413f;
                                border: none;
                                padding: 3px;
                                border-radius: 5px;
                             }
                            """)
        msgbox.setWindowTitle("confirm deletion")
        msgbox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        deleteYes = False
        for button in msgbox.findChildren(QPushButton):
            button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        if (self.data == 'students') :
            msgbox.setText(f"Are you sure you want to delete student {self.obj['id_no']}?")
            response = msgbox.exec()
            if response == QMessageBox.StandardButton.Yes :
                delStudent(self.obj['id_no'])
                self.rerender()
                deleteYes = True
        elif (self.data == 'programs') :
            programWithCollegeCnt = getOptions.getStudentsOfProgramsCount(self.obj['code'])
            msgbox.setText(f"Are you sure you want to delete program {self.obj['code']}? it currently has {programWithCollegeCnt} students, deleting the program will leave them with no program.")
            response = msgbox.exec()
            if response == QMessageBox.StandardButton.Yes :
                delProgram(self.obj['code'])
                self.rerender()
                update_formComboBox(self.data, self.form_comboBox)
                update_filterComboBox(self.data, self.filter_comboBox)                
                self.dependencyPanel.myList.refactor_rerender()
                deleteYes = True
            # sync with student data
        elif (self.data == 'colleges') :
            programWithCollegeCnt = getOptions.getProgramsOfCollegesCount(self.obj['code'])
            msgbox.setText(f"Are you sure you want to delete college {self.obj['code']}? it currently has {programWithCollegeCnt} programs, deleting the college will leave them with no college.")
            response = msgbox.exec()
            if response == QMessageBox.StandardButton.Yes :
                delCollege(self.obj['code'])
                self.rerender()
                update_formComboBox(self.data, self.form_comboBox)
                update_filterComboBox(self.data, self.filter_comboBox, 1)                
                update_filterComboBox(self.data, self.filter_comboBox2, 2)   
                self.dependencyPanel.myList.refactor_rerender()
                deleteYes = True
        if deleteYes :
            self.parent().parent().parent().parent().parent().parent().animationSeq("delete")

            # sync with program data

def clear_layout(layout): 
    if layout is not None:
        for i in reversed(range(layout.count())):
            item = layout.takeAt(i) 

            if item.widget(): 
                item.widget().deleteLater()
            elif item.spacerItem():  
                layout.removeItem(item) 

            