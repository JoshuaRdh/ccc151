import csv

# example = {'id_no':'2025-2258','first_name': 'John','last_name': 'Doe','year_level': '4','gender': 'M','program_code': 'bscs'}

def writeStudentData(studentList) :
    with open("data/students.csv", 'w', newline='') as csvfile:
        fieldNames = ['id_no', 'first_name', 'last_name', 'gender','year_level', 'program_code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(studentList)


def addStudent(newStudent) : 
    with open('data/students.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        studentList = list(reader)
        studentList.append(newStudent)

    print('adding student', newStudent)
    writeStudentData(studentList)

def editStudent(id, obj) :
    editedList = []
    with open('data/students.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        studentList = list(reader)
        for student in studentList :
            if id == student['id_no'] :
                print('hello')
                editedList.append(obj)
                continue
            editedList.append(student)
    print('updating student with idno',id,'to', obj)
    writeStudentData(editedList)

def delStudent(id) :
    editedList = []
    with open('data/students.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        studentList = list(reader)
        for student in studentList :
            if id != student['id_no'] :
                editedList.append(student)
    print('deleting student', id)
    writeStudentData(editedList)

def editStudentProgCode(code, change) :
    editedList = []
    with open('data/students.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        studentList = list(reader)
        for student in studentList :
            if student['program_code'] == code :
                student['program_code'] = change
                editedList.append(student)
                continue
            editedList.append(student)
    writeStudentData(editedList)

# addStudent(example)
