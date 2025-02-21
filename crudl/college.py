import csv
from crudl.program import editProgramCollege_Code

# example = {'code':'ccs','name': 'college of computer studies'}

def writeCollegeData(collegeList) :
    with open("data/colleges.csv", 'w') as csvfile:
        fieldNames = ['code', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(collegeList)


def addCollege(newCollege) : 
    with open('data/colleges.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        collegeList = list(reader)
        collegeList.append(newCollege)

    print('adding college', newCollege)
    writeCollegeData(collegeList)
    
def editCollege(thisCode, obj) :
    editedList = []
    with open('data/colleges.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        collegeList = list(reader)
        for college in collegeList :
            if thisCode == college['code'] :
                editedList.append(obj)
                if obj['code'] != college['code'] :
                    editProgramCollege_Code(thisCode, obj['code'])
                continue
            editedList.append(college)
    print('updating college code', thisCode, 'to', obj)
    writeCollegeData(editedList)

def delCollege(code) :
    editedList = []
    with open('data/colleges.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        collegeList = list(reader)
        for college in collegeList :
            if code != college['code'] :
                editedList.append(college)
    print("deleting", code)
    editProgramCollege_Code(code, 'none')
    writeCollegeData(editedList)
    
# addCollege(example)