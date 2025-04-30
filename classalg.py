import json
import csv
from colorama import Fore, Back, Style  # For colored terminal output

order = []  # Stores computed class weightings per student

# Function to load and return either class or student data
def getLenList(lengthType="class"):
    if lengthType == "class":
        with open('classdat.json') as json_file:
            data = json.load(json_file)
            return data['classes']  # Returns dictionary of classes
    if lengthType == "student":
        with open("studentdat.json") as json_file:
            data = json.load(json_file)
            return data['students']  # Returns dictionary of students
    else:
        print(Fore.RED + "Improper input, please input either \"class\" or \"student\" to get the length of the list!")

# Function to print and return a list of topic values for each student
def getStudent():
    with open('studentdat.json') as json_file:
        data = json.load(json_file)
        student_topics = []  # Will contain list of topic lists
        for student_name in data['students'].keys():
            topics = list(data["students"][student_name]["Topics"].values())  # Get topic values
            student_topics.append(topics)  # Add to student topics list
            print(student_name, ":", topics)  # Display student's topic values
        return student_topics  # Returns list of lists (one list per student)

# Calculates the absolute difference between a class's topic values and a student's topic values
def class_weighting(cl, st):
    score = []
    topic_count = len(list(getDataByIndex(0)))  # Number of topics per class (assumes uniformity)

    for i in range(topic_count):
        topic_value = getTopicByIndex(cl, i)  # Get topic value for class
        student_value = int(st[i])  # Get corresponding student topic value
        score.append(abs(topic_value - student_value))  # Calculate and store absolute difference

    return score  # Returns list of differences

# Gets a specific topic value for a given class and topic index
def getTopicByIndex(class_index, topic_index):
    class_list = getLenList("class")  # Dictionary of all classes
    class_keys = list(class_list.keys())  # List of class keys

    if 0 <= class_index < len(class_keys):  # Check for valid class index
        class_name = class_keys[class_index]  # Get class name from index
        topics = list(class_list[class_name]["Topics"].items())  # Get topic items for the class
        
        if 0 <= topic_index < len(topics):  # Check for valid topic index
            return int(topics[topic_index][1])  # Return topic value as int
        else:
            return "Topic index out of range"
    else:
        return "Class index out of range"

# Retrieves specific data (topics or name) for a class by index
def getDataByIndex(index, typerequest="topics"):
    class_keys = list(getLenList("class"))  # List of class names
    if 0 <= index < len(class_keys):  # Validate index
        class_name = class_keys[index]  # Get class name
        if typerequest == "name":
            return getLenList("class")[class_name]["name"]  # Return class name
        if typerequest == "topics":
            return getLenList("class")[class_name]["Topics"]  # Return topic dictionary
        else:
            print("Improper input, please input either \"name\" to get the name of a class or \"topics\" to get the topics in a class")
    else:
        return "Index out of range"
    
# Gets name of a student by index
def getStudentNameByIndex(index):
    student_list = getLenList("student")
    if 0 <= index < len(student_list):
        return list(student_list.keys())[index]  # Return student name
    else:
        return "Index out of range"

# MAIN EXECUTION

# Print first class's topic dictionary
print("\nGET CLASS LIST:", getDataByIndex(0, "topics"))

student_order = []  # Will store the ordering or matching results

# Loop through each student
for i in range(len(getLenList("student"))):
    # add students name
    order.append(getStudentNameByIndex(i))
    # Loop through each class
    for j in range(len(getLenList("class"))):
        # Calculate weighting score for this student-class pair
        order.append(class_weighting(j, getStudent()[i]))
    print("o:", order)  # Print current state of order list
# combine it, so each indice is a tuple of (student name, class weightings)
order = [(order[i], order[i+1:i+len(getLenList("class"))+1]) for i in range(0, len(order), len(getLenList("class")) + 1)]
print
print("printed order:", order[1][1][1])
for i in range(len(order[i])):
    # fill in later
    pass