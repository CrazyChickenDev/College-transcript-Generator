import datetime

#================== FUNCTION DECLARATIONS ==========================

# A function to read data from a text files
def filereader(filename):
    if filename.endswith('.txt'):
        with open(filename, 'r') as f:
            return f.readlines()
    else: raise ValueError("File name must end with .txt")

# A function to write data to a text file
def filewriter(filename, lines):
    with open(filename, 'a+') as f:
        return f.writelines(lines)

# A function to print Student's Name
def getName(fn, ln):
    return fn+" "+ln

#??????
def getCount(score, excel, passd, faild):
    if score > 55 and score <= 100:
        excel +=1
    elif score > 45 and score < 55:
        passd +=1
    elif score > 0 and score < 45:
        faild +=1

# A function to determine score grade and remarks
def getScoreInfo(score):
    if score > 74 and score <= 100:
        return str(score)+"\t\t  \tA\t \tExcellent"
    
    elif score > 69 and score < 75:
        return str(score)+"\t\t  \tA\t \tVery Good"

    elif score > 64 and score < 70:
        return str(score)+"\t\t  \tB\t \tGood"
        
    elif score > 59 and score < 65:
        return str(score)+"\t\t  \tB\t \tCredit"
        
    elif score > 54 and score < 60:
        return str(score)+"\t\t  \tC\t \tCredit"
        
    elif score > 49 and score < 55:
        return str(score)+"\t\t  \tC\t \tPass"
        
    elif score > 44 and score < 50:
        return str(score)+"\t\t  \tD\t \tPass"
        
    elif score > 39 and score < 45:
        return str(score)+"\t\t  \tF\t \tFail"
        
    elif score > 0 and score < 45:
        return str(score)+"\t\t  \tF\t \tFail"


#=================== MAIN PROGRAM BLOCK ============================

#Variable decalarations
rawFileContents, datafeedArray, studentsScores = [], [], []
runcount, innercount = 0, 0
yr = datetime.datetime.now()
generalRemarks = "\nRemarks: You did Good in {} Course(s), Passed {} Course(s) and Failed {} Course(s)\n"
advice = "\n\tNote: Failed Courses are Advised to be retaken\n\t*******************************************************\n\n"
fileHeader = "\t\t\tFINAL EXAMINATION RESULTS\n\t\t\t************************\n\t\t\t************************\n"

#Opening the input file
try:
    infile = filereader('rawResult.txt')
except IOError as e:
    print("File could not be opened; ", e)
except ValueError as e:
    print("Unrecognized file name; ", e)

# Reading and storing the file contents to a list (and getting rid of all form of white spaces)
for lines in infile:
    rawFileContents.append(lines.split())

# Creating another list to contain Student's details
for data in rawFileContents:
    if data == rawFileContents[0]:
        pass
    else:
        studentsScores.append(data)

# Reading from all the lists and formating the output 
while runcount < len(rawFileContents):
    for row in rawFileContents:
        scoreCounter = 2
        great, passed, failed = 0, 0, 0
        for column in row:
            datafeedArray = studentsScores[runcount]
            if rawFileContents.index(row) == 0 and row.index(column) == 0:
                filewriter(getName(datafeedArray[0], datafeedArray[1])+" Transcript.doc", "\n"+fileHeader+"\n")
                #print(fileHeader)
                filewriter(getName(datafeedArray[0], datafeedArray[1])+" Transcript.doc", (column+":\t"+getName(datafeedArray[0], datafeedArray[1])+"\n"))
                #print(column, ":\t", getName(datafeedArray[0], datafeedArray[1]))
                filewriter(getName(datafeedArray[0], datafeedArray[1])+" Transcript.doc", ("Session: Final\nYear: {}\n\n".format(yr.year))+"\n")
                #print("Session: Final\nYear: {}\n\n".format(yr.year))
                filewriter(getName(datafeedArray[0], datafeedArray[1])+" Transcript.doc", "Courses\t    Score\t  Grade\t   Remarks\n=======\t    =====\t  =====\t   =======\n")
                #print("Courses\t    Score\t  Grade\t   Remarks\n=======\t    =====\t  =====\t   =======\n")
                
            else:
                filewriter(getName(datafeedArray[0], datafeedArray[1])+" Transcript.doc", (column+"\t  "+getScoreInfo(int(datafeedArray[scoreCounter])))+"\n")
                #print(column, "\t  ", getScoreInfo(int(datafeedArray[scoreCounter])))
                #counting excellent, pass and failed courses
                if int(datafeedArray[scoreCounter]) > 55 and int(datafeedArray[scoreCounter]) <= 100: great +=1
                elif int(datafeedArray[scoreCounter]) > 45 and int(datafeedArray[scoreCounter]) < 55: passed +=1
                elif int(datafeedArray[scoreCounter]) > 0 and int(datafeedArray[scoreCounter]) < 45: failed +=1
                else: pass
                scoreCounter +=1
                        
        filewriter(getName(datafeedArray[0], datafeedArray[1])+" Transcript.doc", generalRemarks.format(great, passed, failed))
        #print(generalRemarks.format(great, passed, failed))
        filewriter(getName(datafeedArray[0], datafeedArray[1])+" Transcript.doc", advice)        
        #print(advice)
        runcount += 1
        break
    if runcount == (len(rawFileContents)-1):
        break

print("Done...All transcipts have been generated in the resulting folder with respect to the Students")
                
    

