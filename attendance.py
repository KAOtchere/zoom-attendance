#Author: Kwabena Aboagye-Otchere
#records attendance count for students in class
"""@params 
argv1: a folder with csv files where each file represents attendance in a zoom session
argv2: a target csv file as output
argv3: minimum acceptable time for attendance (mins). eg: 20"""
import sys
import os, os.path
import glob
import pandas as pd
from collections import Counter
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

#Folder which contains the participant lists from zoom
dir = sys.argv[1]

#target attendance csv file
output = sys.argv[2]

minTimePresent = sys.argv[3]

#Number of lectures held
lectureCounts = len(os.listdir(dir))

#List of names to ignore (Lecturer, FI etc)
nonStudent = ['person1', 'person2']

lecturesCSV = glob.glob("{}/*.csv".format(dir))


lectures = []
lecturecount = 0

for l in lecturesCSV:
    lecturecount += 1
    participants = pd.read_csv(l, skiprows=3, usecols=["Name (Original Name)","Total Duration (Minutes)"], on_bad_lines='skip')
    participants['Name (Original Name)'] = participants['Name (Original Name)'].str.lower()
    participants = participants[participants['Total Duration (Minutes)'] >= minTimePresent] 
    participants = participants.drop_duplicates(subset=['Name (Original Name)']) #gets rid of duplicates which aren't caught by zoom
    participants = participants[~participants.isin(nonStudent)]
    lectures.append(participants)
    
attendance = pd.DataFrame(lectures[0])
for i in range(1, len(lectures)):
    attendance = attendance.append(lectures[i])

attendance.value_counts(subset=['Name (Original Name)']).rename_axis('Names').reset_index(name='Classes attended').to_csv(output)
print('total lectures {}'.format(lecturecount))




