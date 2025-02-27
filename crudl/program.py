import csv
from crudl.student import editStudentProgCode

example = {'code':'bscs','name': 'bachelors of science in computer science', 'college_code': 'ccs'}

def writeProgramData(programList = {}) :
    with open("data/programs.csv", 'w', newline='') as csvfile:
        fieldNames = ['code', 'name', 'college_code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(programList)


def addProgram(newProgram) : 
    with open('data/programs.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        programList = list(reader)
        programList.append(newProgram)

    print('adding program', newProgram)
    writeProgramData(programList)

def editProgram(thisCode, obj) :
    editedList = []
    with open('data/programs.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        ProgramList = list(reader)
        for program in ProgramList :
            if thisCode == program['code'] :
                editedList.append(obj)
                if obj['code'] != program['code'] :
                    editStudentProgCode(thisCode, obj['code'])
                continue
            editedList.append(program)
    print('updating program code', thisCode, 'to ', obj)
    writeProgramData(editedList)
    #account for when code is changed, should sync with student.csv

def delProgram(code) :
    editedList = []
    with open('data/programs.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        ProgramList = list(reader)
        for program in ProgramList :
            if code != program['code'] :
                editedList.append(program)
    print("deleting",code)
    editStudentProgCode(code, 'none')
    writeProgramData(editedList)

def editProgramCollege_Code(code, change) :
    editedList = []
    with open('data/programs.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        programList = list(reader)
        for program in programList :
            if program['college_code'] == code :
                program['college_code'] = change
                editedList.append(program)
                continue
            editedList.append(program)
    writeProgramData(editedList)

# addProgram(example)