from algo import getOptions
from PyQt6.QtWidgets import QMessageBox
import re
from algo import checkDitto
from PyQt6.QtCore import Qt
from datetime import datetime

def formValidated(data, myObj, self, obj) :
    msgbox = QMessageBox(self)
    msgbox.setIcon(QMessageBox.Icon.Critical)
    msgbox.setStyleSheet("background-color: #a1413f; color: white")
    if (data == 'students') :
        if obj is None: obj = {'id_no' : '0'}
        idnoRegex = r'^[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]$'
        year = myObj['id_no'][0:4]
        current_year = int(datetime.now().year)

        if not myObj['id_no'] or not myObj['first_name'] or not myObj['last_name'] :
            msgbox.setWindowTitle("empty entry")
            msgbox.setText("no entry should be empty")
            msgbox.exec()
            return False
        elif (re.fullmatch(idnoRegex,myObj['id_no']) is None):
            msgbox.setWindowTitle("invalid format")
            msgbox.setText("id number should follow format, e.g 2019-0001")
            msgbox.exec()
            return False
        elif int(year) < 1968 or int(year) > current_year :
            msgbox.setWindowTitle("invalid year")
            msgbox.setText("id number should be a valid year")
            msgbox.exec()
            return False
        
        elif (checkDitto.checkStudents(myObj['id_no'].lower()) is True and obj['id_no'].lower() != myObj['id_no'].lower()) :
            msgbox.setWindowTitle("ditto id number")
            msgbox.setText("student with id number already exists")
            msgbox.exec()
            return False
        else :
            return True
    elif (data == 'programs') :
        if obj is None: obj = {'code' : '0'}
        codeRegex = r'^[a-zA-Z]+$'
        if not myObj['code'] or not myObj['name'] : 
            msgbox.setWindowTitle("empty entry")
            msgbox.setText("no entry should be empty")
            msgbox.exec()
            return False
        elif (re.fullmatch(codeRegex, myObj['code']) is None) :
            msgbox.setWindowTitle("invalid format")
            msgbox.setText("program code should only contain letters, e.g bscs")
            msgbox.exec()
            return False
        elif (checkDitto.checkPrograms(myObj['code'].lower()) is True and obj['code'].lower() != myObj['code'].lower()) :
            msgbox.setWindowTitle("ditto program code")
            msgbox.setText("program code already exists")
            msgbox.exec()
            return False
        else:
            return True
    elif (data == 'colleges') :
        if obj is None: obj = {'code' : '0'}
        codeRegex = r'^[a-zA-Z]+$'
        if not myObj['code'] or not myObj['name']: 
            msgbox.setWindowTitle("empty entry")
            msgbox.setText("no entry should be empty")
            msgbox.exec()
        elif (re.fullmatch(codeRegex, myObj['code']) is None) :
            msgbox.setWindowTitle("invalid format")
            msgbox.setText("college code should only contain letters, e.g ccs")
            msgbox.exec()
            return False
        elif (checkDitto.checkColleges(myObj['code'].lower()) is True and obj['code'].lower() != myObj['code'].lower()) :
            msgbox.setWindowTitle("ditto college code")
            msgbox.setText("college code already exists")
            msgbox.exec()
        else:
            return True
    
def update_formComboBox(data, comboBox) :
    if data == 'programs' :
        comboBox.blockSignals(True)
        comboBox.clear()
        comboBox.addItem('none')
        comboBox.addItems(getOptions.getPrograms())
        comboBox.blockSignals(False)

    elif data == 'colleges' :
        comboBox.blockSignals(True)
        comboBox.clear()
        comboBox.addItem('none')
        comboBox.addItems(getOptions.getColleges())
        comboBox.blockSignals(False)

def update_filterComboBox(data, comboBox, num = None) : 
    if data == 'programs' or num == 2: # 2 means college_code is edited - update student filter cb
        comboBox.blockSignals(True)
        comboBox.clear()
        comboBox.addItem('no filter')
        comboBox.addItem('assigned')
        comboBox.addItem('unassigned')
        comboBox.addItem("-- by College --")
        college_labelIndex = comboBox.count() -1
        comboBox.setItemData(college_labelIndex, False, Qt.ItemDataRole.UserRole -1)
        comboBox.addItems(getOptions.getColleges())
        comboBox.addItem("-- by Program --") 
        program_labelIndex = comboBox.count() - 1
        comboBox.setItemData(program_labelIndex, False, Qt.ItemDataRole.UserRole -1)
        comboBox.addItems(getOptions.getPrograms())
        comboBox.blockSignals(False)

    else : 
        comboBox.blockSignals(True)
        comboBox.clear()
        comboBox.addItem('no filter')
        comboBox.addItem('assigned')
        comboBox.addItem('unassigned')
        comboBox.addItem("-- by College --")
        college_labelIndex =comboBox.count() -1
        comboBox.setItemData(college_labelIndex, False, Qt.ItemDataRole.UserRole -1)
        comboBox.addItems(getOptions.getColleges())
        comboBox.blockSignals(False)

