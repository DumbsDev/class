import json
import csv

def getClassList():
    with open('classdat.json') as json_file:
        data = json.load(json_file)
        # print('type content of data[\'classes\']:', type((data['classes'])))
        # print('contents of data[\'classes\']:', (data['classes']))
        return (data['classes'])

def getStudent():
    with open('classdat.json') as json_file:
        data = json.load(json_file)
        student_topics = []
        for class_name in data['classes'].keys():
            topics = list(data["classes"][class_name]["Topics"].values())  # Extract values
            student_topics.append(topics)  # Append list of values
        return student_topics  # Now returns a list of topic values per class


def class_weighting(cl, st):
    score = []

    topic_count = len(list(getDataByIndex(0)))

    for i in range(topic_count):
        topic_value = getTopicByIndex(cl, i)  # This is an integer
        student_value = int(st[i])  # Convert st[i] to an integer

        score.append(abs(topic_value - student_value))  # This provides the difference between the topic value and student value
    

    print('b: ', score[0])

    return score


order = []

def getTopicByIndex(class_index, topic_index):
    class_list = getClassList()  # Get dictionary of all classes
    class_keys = list(class_list.keys())  # Extract class names as a list

    if 0 <= class_index < len(class_keys):  # Ensure class index is valid
        class_name = class_keys[class_index]  # Get the class name by index
        topics = list(class_list[class_name]["Topics"].items())  # Get topics of that class
        
        if 0 <= topic_index < len(topics):  # Ensure topic index is valid
            return int(topics[topic_index][1])  # Return the topic value as integer
        else:
            return "Topic index out of range"
    else:
        return "Class index out of range"


def getDataByIndex(index, typerequest = "topics"):
    class_keys = list(getClassList())  # Get all class names as a list
    if 0 <= index < len(class_keys):  # Ensure index is within range
        class_name = class_keys[index]  # Get class name by index
        if typerequest == "name":
            return getClassList()[class_name]["name"]  # Return topics of the class
        if typerequest == "topics":
            return getClassList()[class_name]["Topics"]  # Return topics of the class
        else:
            print("Improper input, please input either \"name\" to get the name of a class or \"topics\" to get the topics in a class")
    else:
        return "Index out of range"

def getDataByIndex(index, typerequest = "topics"):
    class_keys = list(getClassList())  # Get all class names as a list
    if 0 <= index < len(class_keys):  # Ensure index is within range
        class_name = class_keys[index]  # Get class name by index
        if typerequest == "name":
            return getClassList()[class_name]["name"]  # Return topics of the class
        if typerequest == "topics":
            return getClassList()[class_name]["Topics"]  # Return topics of the class
        else:
            print("Improper input, please input either \"name\" to get the name of a class or \"topics\" to get the topics in a class")
    else:
        return "Index out of range"
    
print("\nGET CLASS LIST:", getDataByIndex(0, "topics"))

for i in range(len(getClassList())):
    # print(i, getClassList())
    order.append(class_weighting(i, getStudent()[0]))

print(order)