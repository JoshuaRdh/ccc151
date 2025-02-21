import csv

def getPrograms() :
    with open('data/programs.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        programList = [row['code'] for row in reader]

        
    return sorted(programList)

def getColleges() :
    with open('data/colleges.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        programList = [row['code'] for row in reader]

        
    return sorted(programList)  

def getProgramsOfColleges(college) :
    with open('data/programs.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        programSet = set()
        for row in reader :
            if row['college_code'] == college :
                programSet.add(row['code'])

    return list(programSet)

def getStudentsOfProgramsCount(program_code) :
    count = 0
    with open('data/students.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for obj in reader:
            if obj["program_code"] == program_code :
                count +=1

    return count 

def getProgramsOfCollegesCount(college_code) :
    count = 0
    with open('data/programs.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for obj in reader:
            if obj["college_code"] == college_code :
                count +=1

    return count 
