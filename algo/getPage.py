

def getPage(arr, pageNumber, rows) :
    # count = len(arr)
    end = rows * pageNumber
    start = end - rows
    return arr[start : end]
