#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 19:19:27 2018

@author: Rathi
"""

# Explaining the entire approach here:
#
# Taking test file - Students: A,B,C,D,E,F
#
# We first implemented Brute Force method, by taking all combinations of A to F
# Like - ABC, ABD, ABF, BCF, DEF and so on. Then formed mutually exclusive sets,
# such that A, if once taken, never repeats in the set. Eg. ABC, DEF or ABD, CEF
# but not ABC, BDE (B repeating). Taking all these plausible sets, we found the one with the least cost.

# However, this method doesn't work in required time for larger number of inputs.
# 
# So we have considered the following: the time taken for grading an entire assignment
# with multiple questions would be greater than the time required for setting up a meeting
# which will in turn be greater than the time required for reading an e-mail.

# In short, we have considered - k >> m > n > 1

# So, we make groups of 3 at first since it reduces time by k for every team less made but
# this is a trade-off against the 1 minute which gets added for not giving size preference

# Followed by this, all these groups are shuffled for varying number of times and their
# time required is stored in a list. The one set/combination with lowest time is then
# given as output


import heapq
from itertools import combinations
import random
import sys


file = []
username = []
size_pref = []
person_pref = []
person_not_pref = []
list_of_ppl = []


count1 = 0
cutoff = len(username)

# Input Parameters
text_file = open(str(sys.argv[1]),"r")

k = int(sys.argv[2])

m = int(sys.argv[3])

n = int(sys.argv[4])


# Read the text file and store the data in suitable structures
for line in text_file:
    file = line.split()
    username.append(file[0])  # List of all usernames
    size_pref.append(file[1])  
    int_file = list(map(int, size_pref)) # Integer list of all preferred sizes wrt username
    person_pref.append(file[2]) # List of person preferences with respect to username
    person_not_pref.append(file[3]) # List of person non-preferences with respect to username  
    count1 = count1 + 1 # Counting number of people giving inputs


# Make samples of the population where you want to implement your search algorithm.
def generateSamples(list_of_ppl,size=3,count=0):
        
    if len(list_of_ppl) > size:
        for team in combinations(list_of_ppl, size):
            if count<10:
                for comb in generateSamples(list(set(list_of_ppl) - set(team))):
                    count=count+1
                    yield [list(team), *comb]

    else:
        yield [list_of_ppl]
        
# Calculate time required for given combination of groups, given k,m,n parameters
def total_time(groups):
    time = 0
    group_times = []
    
    dict_size_pref = {username[i]:int_file[i] for i in range(0,count1)}

    dict_person_pref = {}
    for i in range(0,count1):
        if person_pref[i] == "_":
            dict_person_pref[username[i]] = []
        else:
            dict_person_pref[username[i]] =person_pref[i].split(",")

    dict_person_not_pref = {}
    for i in range(0,count1):
        if person_pref[i] == "_":
            dict_person_not_pref[username[i]] = []
        else:
            dict_person_not_pref[username[i]] =person_not_pref[i].split(",")

    # Calculate cost associated with every group
    for group in groups:
        group_time = 0
        # Calculate cost associated with one person of the group
        for person in group:
            # Group size issue
            if dict_size_pref[person] != 3 and dict_size_pref[person] != 0:
                group_time += 1

            other_persons = [i for i in group if i != person]

            # Preferred person not in group. n minutes of time of grader
            for preferred in dict_person_pref[person]:
                if preferred not in other_persons:
                    group_time += n

            # Not preferred person in group. m minutes of grader
            for other_person in other_persons:
                if other_person in dict_person_not_pref[person]:
                    group_time += m

        group_times.append(group_time)

    time = sum(group_times)
    time += len(group_times)*k
    return time

# Gives minimum time out of all possible combinations of groups passed to it
def get_min_time(all_poss_combinations):
    fringe = []

    for groups in all_poss_combinations:
        heapq.heappush(fringe, (total_time(groups), groups))

    time, goal_team = heapq.heappop(fringe)
    return goal_team, time


# shuffling_times = len(username)

goal_time = []
time1=[]
goal1=[]
u=list(username)

for x in range(0,100):
    random.shuffle(u) # Shuffling list of usernames
    t = list(generateSamples(u,size=3,count=0)) # Generating samples of teams of 3 of shuffled list
    temp_goal  = list(get_min_time(t))
    goal1.append(temp_goal[0])
    time1.append(temp_goal[1])

for y in range(0,len(time1)):
    if time1[y] == min(time1):
        for z in goal1[y]:
            print(" ".join(z))
        print(time1[y])
        break