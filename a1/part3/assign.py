#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import time
import random 

# converts text file to list of dictionaries
def decode(input_file):
    users = []
    with open(input_file, 'r') as f:
        lines = f.readlines()
        for line in range(len(lines)):
            curr = lines[line].split()
            user_id = curr[0]
            q2 = curr[1].split('-')
            team = len(q2)
            members = []
            for i in range(len(q2)):
                if q2[i] != "xxx" and q2[i] != user_id:
                    members.append(q2[i])
            not_members = []
            q3 = curr[2].split(',')
            for i in range(len(q3)):
                if q3[i] != '_':
                    not_members.append(q3[i])
            user = {"ID": user_id,
                    "group #": team,
                    "pair with": members,
                    "do not pair with": not_members}
            users.append(user)
    return users

# teams : list of lists
# responses : list of dictionaries
def cost(teams, responses):
    # 5 minutes to grade each team
    total_time = len(teams) * 5
    for r in range(len(responses)):
        user_id = responses[r]["ID"]
        for t in range(len(teams)):
            if user_id in teams[t]:
                curr_team = teams[t]
        # add 2 if team size not met
        if len(curr_team) != responses[r]["group #"]:
            total_time += 2
        # for each requested not in team, add 60 * .05 = 3
        for m in range(len(responses[r]["pair with"])):
            if responses[r]["pair with"][m] not in curr_team:
                total_time += 3
        # for each requested not to work with in team, add 10
        for m in range(len(responses[r]["do not pair with"])):
            if responses[r]["do not pair with"][m] in curr_team:
                total_time += 10
    return total_time

# creates teams randomly 
def create_random(responses):
    user_ids = []
    teams = []
    for r in range(len(responses)):
        user_ids.append(responses[r]["ID"])
    while len(user_ids) != 0:
        ids_left = len(user_ids)
        max_range = min(3, ids_left)
        team_size = random.randint(1, max_range)
        curr_team = []
        for t in range(team_size):
            if len(user_ids) != 0:
                rand_member = random.choice(user_ids)
                curr_team.append(rand_member)
                user_ids.remove(rand_member)
        teams.append(curr_team)
    return ["-".join(teams[i]) for i in range(len(teams))]
            
# mutates team list
# can split, combine, or both
# split: create two teams from one
# combine: create one team from two
def mutate(loser, prob_split=.5, prob_combine=.5):
    split = True if random.random() < prob_split else False
    combine = True if random.random() < prob_combine else False
    if split:
        splitable = []
        for l in range(len(loser)):
            if '-' in loser[l]:
                splitable.append(loser[l])
        if len(splitable) > 1:
            team_choice = random.choice(splitable)
            loser.remove(team_choice)
            new_team = team_choice.split('-')
            if len(new_team) > 2:
                if random.random() > .5:
                    choice1 = random.choice(new_team)
                    new_team.remove(choice1)
                    choice2 = random.choice(new_team)
                    new_team.remove(choice2)
                    new_team.append(choice1 + '-' + choice2)
            for i in range(len(new_team)):
                loser.append(new_team[i])
            
    if combine:
        combinable = []
        for l in range(len(loser)):
            curr_split = loser[l].split('-')
            if len(curr_split) < 3:
                combinable.append(loser[l])
        if len(combinable) > 1:
            combine_choice1 = random.choice(combinable)
            loser.remove(combine_choice1)
            combinable.remove(combine_choice1)
            combine_choice2 = random.choice(combinable)
            loser.remove(combine_choice2)
            combinable.remove(combine_choice2)
            combination = combine_choice1 + '-' + combine_choice2
            comb_s = combination.split('-')
            if len(comb_s) > 3:
                separate_choice = random.choice(comb_s)
                comb_s.remove(separate_choice)
                loser.append(separate_choice)
                loser.append("-".join(comb_s))
            else:
                loser.append(combination)
          
    return loser

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    responses = decode(input_file)
    # hist keeps track of explored teams and their cost
    hist = {}
    random_teams = []
    # start w 1000 random teams
    for i in range(1000):
        teams = create_random(responses)
        random_teams.append(teams)
        tstring = "|".join(teams)
        t_list = []
        for t in range(len(teams)):
            t_list.append(teams[t].split('-'))
        hist[tstring] = cost(t_list, responses)
    # yield best fit
    best_fit = min(hist, key=hist.get)
    yield({"assigned-groups": best_fit.split("|"),
            "total-cost" : hist[best_fit]})
    prev_best = hist[best_fit]
    while hist[best_fit] != (len(responses) / 3) * 5:
        best_fit = min(hist, key=hist.get)
        # if new best, return
        if hist[best_fit] < prev_best:
            prev_best = hist[best_fit]
            yield({"assigned-groups": best_fit.split("|"),
                   "total-cost" : hist[best_fit]})
        # competition
        for i in range(500):
            competitor1 = random.choice(random_teams)
            random_teams.remove(competitor1)
            competitor2 = random.choice(random_teams)
            random_teams.remove(competitor2)
            
            random_teams.append(competitor1)
            random_teams.append(competitor2)
            
            if hist["|".join(competitor1)] < hist["|".join(competitor2)]:
                loser = competitor2
            if hist["|".join(competitor2)] <= hist["|".join(competitor1)]:
                loser = competitor1
            
            # mutate and replace loser
            random_teams.remove(loser)
            loser = mutate(loser)
            random_teams.append(loser)
            
            # get cost if not already in hist
            if "|".join(loser) not in hist:
                loser_list = []
                for l in range(len(loser)):
                    loser_list.append(loser[l].split('-'))
                hist["|".join(loser)] = cost(loser_list, responses)

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))
    
    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
