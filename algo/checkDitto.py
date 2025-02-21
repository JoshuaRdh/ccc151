import csv

def checkStudents(idno) :
    with open('data/students.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        studentsList = [row['id_no'] for row in reader]
    
    return idno in studentsList

def checkPrograms(code) :
    with open('data/programs.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        programsList = [row['code'] for row in reader]
 
    return code in programsList

def checkColleges(code) :
    with open('data/colleges.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        collegesList = [row['code'] for row in reader]
    
    return code in collegesList