import json
import csv

def getClassList():
    with open('classdat.json') as json_file:
        data = json.load(json_file)
        return list(data['classes'].keys())

def getClassData(classID, ask):
    with open('classdat.json') as json_file:
        data = json.load(json_file)
        className = getClassList()[classID]
        if ask == "":
                return data['classes'][className]
        else:
            try:
                return data['classes'][className][ask]
            except:
                return "Invalid data request."


def run():
    print(getClassList())
    print("Class data options: " + str(list(getClassData(0, "").keys())))
    print("Class count (ID's): " + "0 - " + str(len(getClassList())-1))
    print(getClassData(int(input("Enter class ID: ")), (input("Enter data request: "))))

def assign():
    # This is the code used to cross reference student "interests" and their weights
    # with the class "topics" and their weights. 
    pass
    # print the amount of classes
    print(len(getClassList()))

assign()