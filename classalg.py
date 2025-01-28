import json
import csv

def getClassList():
    with open('classdat.json') as json_file:
        data = json.load(json_file)
        print((data['classes'].keys()))
        return list(data['classes'].keys())

def getStudent():
    with open('studentdat.json') as json_file:
        data = json.load(json_file)
        return data['students']

def class_weighting(cl, st):
    score = []

    topic_count = int(getClassList()[0]['Topics'])

    score = []
    for i in topic_count:
        score.append(
            abs(cl[i] - st[i]).sum()
        )
    return score

order = []

for i in range(len(getClassList())):
    print(i, getClassList()[i])
    order.append(class_weighting(getClassList()[i], getStudent()[0]))
print("test")