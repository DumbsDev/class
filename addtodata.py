import json # allow for json file manipulation

def selectBlocks(): # this sets the blocks (1-5) that the class is offered in
    z = []
    x = input("Enter the blocks that this class is offered in (1-5) (NO COMMAS, JUST 12345): ")
    for i in range(len(x)):
        print(x[i])
        z.append(int(x[i]))
    return z #returns a list with the blocks that the class is offered in

def selectStandards(): # this sets the standards that the class covers
    z = []
    w = []
    dic = dict()
    sc = input("Enter the number of standards that this class covers (ex. 3, 9, 1): ")
    for i in range(int(sc)):
        z.append(input("Enter the standard name (refer to the standardized document for proper syntaxing): "))
        w.append(input("Enter the standard weight (1-10): "))
        # weight the standards by the user's input as above
    
    dic = dict(zip(z, w))
    print(dic)
    print(type(dic))
    return dic # returns a dictionary with the standards and their weights

def ClassSize(): # This sets the the minimum and maximum class size
    z = ["min", "max"]
    w = []
    dic = dict()
    w.append(input("Enter the minimum class size: "))
    w.append(input("Enter the maximum class size: "))
    # weight the standards by the user's input as above
    
    dic = dict(zip(z, w))
    print(dic)
    return dic # return the minimum and maximum students per class as a dictionary.

def selectTopics(): # this sets the interest topics in the class, to be cross-referenced with the student's interests
    z = []
    w = []
    dic = dict()
    sc = input("Enter the number of interests/topics you want to add to this class: ")
    for i in range(int(sc)):
        z.append(input("Enter the interest/topic name (refer to the standardized document for proper syntaxing): "))
        for j in range(len(z)):
            w.append(input("Enter the topic/interest weight (1-10): "))
        # weight the standards by the user's input as above
    
    dic = dict(zip(z, w))
    print(dic)
    return dic # this returns a dictionary with a list of topics and their associated weights.

def edit_class(): # this creates/edits a class and writes it to the classdat.json file
    with open('classdat.json', 'r+') as file:
        data = json.load(file)
        new_class = {
            "name": input("Enter the name of the new class: "),
            "prereqs": input("Enter the prerequisites for the new class: "),
            "MinGrade": input("Enter the minimum grade for the new class(0-3, freshman-senior): "),
            
            "Blocks": selectBlocks(),
            "Standards": selectStandards(),
            "ClassSize": ClassSize(),
            "Topics": selectTopics()
        }
        data['classes'].update({new_class['name']: new_class})
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

c = input("Would you like to add a new class or a student? (c/s): ")

if c == 'c':
    edit_class()