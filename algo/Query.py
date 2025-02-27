import math
from algo.getOptions import getProgramsOfColleges

def refactor_Query( queryObj) : # filter -> search -> sort
    arr = queryObj['fetchedList']
    filter_Params = queryObj['filter_Params']
    searchBy = queryObj['searchedBy']
    keyword = queryObj['keyword']
    sort = queryObj['sort']
    return refactor_Filter(arr, filter_Params, searchBy, keyword, sort)

def refactor_Filter(arr, filter_Params, searchBy, keyword, sort) :
    resultsArr = []

    if filter_Params is None or filter_Params['filterBy'] == 'no filter' :
        return refactor_Search(arr, searchBy, keyword, sort)
    
    filterBy = filter_Params['filterBy']
    data = filter_Params['data']
    index = filter_Params['index']
    programLabel_index = filter_Params['programLabel_index']

    if filterBy == 'unassigned' :
        filterBy = 'none'

    if data == 'students' :
        category = 'program' if index > programLabel_index or filterBy == 'none' else 'college'

        if filterBy == 'assigned' :
            for obj in arr :
                    if obj['program_code'] != 'none' :
                        resultsArr.append(obj) 
        elif (category == 'program'):
            for obj in arr :
                if obj['program_code'] == filterBy :
                    resultsArr.append(obj)
        elif (category == 'college') :
            programs = getProgramsOfColleges(filterBy)
            for obj in arr :
                if obj['program_code'] in programs :
                    resultsArr.append(obj)
    elif data == 'programs' :
        if filterBy == 'assigned' :
            for obj in arr :
                    if obj['college_code'] != 'none' :
                        resultsArr.append(obj)
        else :
            for obj in arr :
                if obj['college_code'] == filterBy :
                    resultsArr.append(obj)

    return refactor_Search(resultsArr, searchBy, keyword, sort)

def refactor_Search(arr, searchBy, keyword, sort) :
    resultsArr = []
    for obj in arr :
        if (searchBy != 'everywhere') :
            if keyword.lower() in obj[searchBy].lower() :
                resultsArr.append(obj)
        else:
        #if at least 1 value contains substr, push to resultsArr

            for value in obj.values():
                if keyword.lower() in value.lower() :
                    resultsArr.append(obj)
                    break

    return Sort(resultsArr, sort)

def Sort(arr, sortBy) :
    if (sortBy == 'oldest') :
        return arr
    elif (sortBy == 'recent') :
        rev = list(reversed(arr))
        return rev
    elif (sortBy == 'id no.↑') :
        return mergeSort(arr, '^', 'id_no')
    elif (sortBy == 'id no.↓') :
        return mergeSort(arr, 'v', 'id_no')
    elif (sortBy == 'a-z') :
        return mergeSort(arr, 'v', 'code')
    elif (sortBy == 'z-a') :
        return mergeSort(arr, '^', 'code')
    elif (sortBy == 'last name↑') :
        return mergeSort(arr, '^', 'last_name')
    elif (sortBy == 'last name↓') :
        return mergeSort(arr, 'v', 'last_name')
    elif (sortBy == 'year level↑') :
        return mergeSort(arr, '^', 'year_level')
    elif (sortBy == 'year level↓') :
        return mergeSort(arr, 'v', 'year_level')
    elif (sortBy == 'college') :
        return mergeSort(arr, 'v', 'college_code')
    elif (sortBy == 'program') :
        return mergeSort(arr, 'v', 'program_code')


def mergeSort(arr, order, code) : 
    if len(arr) <= 1 : return arr

    middle = math.floor(len(arr)/2)
    left = arr[0:middle]
    right = arr[middle:len(arr)]
    leftSorted = mergeSort(left, order, code)
    rightSorted = mergeSort(right, order, code)  
    return merge(leftSorted, rightSorted, order, code)

def merge(left, right, order, code) :
    leftLen = len(left)
    rightLen = len(right)
    mergedArr = []
    leftIndex = 0
    rightIndex = 0
    if order == 'v' :
        while (leftIndex < leftLen and rightIndex < rightLen) :
            if (left[leftIndex][code] <= right[rightIndex][code]) :
                mergedArr.append(left[leftIndex])
                leftIndex+=1
            else :
                mergedArr.append(right[rightIndex])
                rightIndex+=1
    else :
        while (leftIndex < leftLen and rightIndex < rightLen) :
            if (left[leftIndex][code] >= right[rightIndex][code]) :
                mergedArr.append(left[leftIndex])
                leftIndex+=1
            else :
                mergedArr.append(right[rightIndex])
                rightIndex+=1

    while (leftIndex < leftLen) :
        mergedArr.append(left[leftIndex])
        leftIndex+=1
    while (rightIndex < rightLen) :
        mergedArr.append(right[rightIndex])
        rightIndex+=1
    
    return mergedArr


