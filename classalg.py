import json
import csv
from colorama import Fore, Back, Style  # For colored terminal output
import copy

def output_return():
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
                # print(student_name, ":", topics)  # Display student's topic values
            return student_topics  # Returns list of lists (one list per student)

    # Calculates the absolute difference between a class's topic values and a student's topic values
    def class_weighting(cl, st):
        score = []
        topic_count = len(list(getDataByIndex(0)))  # Number of topics per class (assumes uniformity)

        for i in range(topic_count):
            topic_value = getTopicByIndex(cl, i)  # Get topic value for class
            student_value = int(st[i])  # Get corresponding student topic value
            score.append(abs(topic_value - student_value))  # Calculate and store absolute difference

        # print("score:", score)  # Print the score for debugging
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
    class Student:
        def __init__(self, name, class_scores):
            self.name = name
            self.class_scores = sorted(class_scores, key=lambda x: x[1])  # Sort on init

        def get_top_classes(self, count=5):
            return self.class_scores[:count]

        def __str__(self):
            top_classes = self.get_top_classes()
            result = f"{self.name}'s Top {len(top_classes)} Classes:\n"
            for class_name, score in top_classes:
                result += f"  {class_name}: {score}\n"
            return result


    # print("\nGET CLASS LIST:", getDataByIndex(0, "topics"))

    class_names = list(getLenList("class").keys())
    student_data = getLenList("student")
    student_topics_list = getStudent()  # Load once

    order = []  # (student name, list of (class, score))

    for i, student_name in enumerate(student_data.keys()):
        student_topics = student_topics_list[i]
        class_scores = []

        for j, class_name in enumerate(class_names):
            score = sum(class_weighting(j, student_topics))  # total weighting score
            class_scores.append((class_name, score))

        # Sort class_scores from lowest (best match) to highest
        class_scores.sort(key=lambda x: x[1])

        order.append((student_name, class_scores))

    # Print results nicely
    print("\nORDERED CLASS MATCHES PER STUDENT (Best to Worst):\n")
    for student_name, class_scores in order:
        print(f"{student_name}:")
        for class_name, score in class_scores:
            print(f"  {class_name}: {score}")
        print()

    # create a student object, which assigns the student their top 5 classes.
    student_objects = []  # List to hold student objects

    # FINAL STUDENT OBJECT CREATION & TOP 5 CLASSES DISPLAY
    print("\nTOP 5 CLASS MATCHES PER STUDENT:\n")
    for student_name, class_scores in order:
        student = Student(student_name, class_scores)
        print(student)
    
    return order  # Return the ordered list of students and their class scores