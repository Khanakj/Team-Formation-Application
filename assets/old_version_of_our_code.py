#IMPORTED FUNCTIONS
import os
import random

#OPENING FILE TO WRITE DATA
f2 = open("OLD_SD.csv", "w", newline = "")
cwd = os.getcwd()

#FUNCTIONS

#SORTING STUDENTS BASED ON TUT GROUP
def tut_grp_div():
    #OPENING CSV FILE TO READ DATA
    with open(os.path.join(cwd, 'records.csv'), 'r') as file:
        studentrecords = file.read()

    students = studentrecords.split('\n')
    l = [] #TEMPORARY LIST TO STORE STUDENTS OF ONE TUTORIAL GROUP
    current_tg = None #KEEPING TABS ON THE TUT GRP BEING SORTED

    for i in students:
        i = i.split(',')

        if i[0] == '':
            continue
        if i[0] != "Tutorial Group": # TO IGNORE THE HEADER CONTENT
            if i[0] != current_tg:
                if len(l) == 50: # WHEN ALL 50 STUDENTS FROM A TUT GROUP ARE SORTED, ADDING THEN TO THE MAIN TUT_GRP LIST
                    tut_grp.append(sorted(l, key=lambda x: x["GPA"])) #SORT STUDENTS BASED ON CGPA
                    l = [] #EMPTY TEMP LIST
                current_tg = i[0]
                #print(current_tg)

            d = {} #STORING EACH STUDENT RECORD AS A DICTIONARY
            d["TG"] = i[0]
            d["ID"] = i[1]
            d["School"] = i[2]
            d["Name"] = i[3]
            d["Gender"] = i[4]
            d["GPA"] = float(i[5])
            l.append(d)

    if len(l) == 50: # WHEN ALL 50 STUDENTS FROM A TUT GROUP ARE SORTED, ADDING THEN TO THE MAIN TUT_GRP LIST
        tut_grp.append(l)
    

def calc_sd(grp):
    cgpas = [student['GPA'] for student in grp]
    mean_cgpa = sum(cgpas)/len(cgpas)
    sum_squared_diff = sum((x - mean_cgpa) ** 2 for x in cgpas)
    sd = (sum_squared_diff / len(cgpas)) ** 0.5
    return sd

#SORTING EACH TUT GROUP INTO 10 TEAMS OF 5 STUDENTS EACH
def teams_of_5(x):
    team_number = 1 #KEEPING TAB ON THE NUMBER OF TEAMS
    successful_teams = []  #LIST OF TEAMS WHICH MEET DIVERSITY CRITERIA
    max_attempts = 100 #TO AVOID INFINITE LOOP SITUTAION 
    while len(successful_teams) < 10 and len(x) >= 5:
        attempts = 0
        found_team = False
        
        while attempts < max_attempts:
            random.shuffle(x) #SHUFFLE TUT GROUP STUDENTS INTO A RANDOM ORDER
            team = x[:5] #CREATING A TEAM OF 5 INITIAL STUDENTS
                
            if diversity([d["School"] for d in team], 
                        [d["Gender"] for d in team],
                        [d["GPA"] for d in team],
                        sd_grp): #IF THE TEAM OF 5 MEETS THE DIVERSITY CRITERIA...
                
                for d in team:
                    d["Team Number"] = team_number #ASSIGN STUDENTS THEIR TEAM NUMBER
                    d["Anomaly"] = 0
                
                team_number += 1
                successful_teams.append(team) #ADD THE TEAM TO SUCCESSFUL TEAMS
                x = x[5:] #REMOVE THE ASSIGNED STUDENTS FROM THE TUT GRP LIST TO AVOID REPETITION OF ALREADY ASSIGNED STUDENTS
                found_team = True
                break
            attempts += 1
            
        # IF NO TEAM IS FOUND AFTER MAX ATTEMPTS, BREAK OUT OF THE LOOP 
        if not found_team and len(x) >= 5:
            team = x[:5]

            for d in team:
                d["Team Number"] = team_number
                if diversity([d["School"] for d in team], 
                    [d["Gender"] for d in team],
                    [d["GPA"] for d in team],
                    sd_grp):
                    d["Anomaly"] = 0
                else:
                    d["Anomaly"] = 1
    
            successful_teams.append(team)
            x = x[5:]
            team_number += 1
        
    return successful_teams


#CHECKING DIVERSITY BASED ON SCHOOL, GENDER, AND CGPA
def diversity(schools, gender, cgpa, sd_grp):
    for i in schools:
        if schools.count(i) > 3:
            return False
    
    for i in gender:
        if gender.count(i) > 3:
            return False
    
    # Method 1 with average
    sum_cgpa = sum(cgpa)
    avg_cgpa = sum_cgpa/len(cgpa)
    
    if avg_cgpa > 4 and avg_cgpa < 4.15:
        return True
    else:
        return False
    
    #Method 2 with standard deviation
    '''mean_cgpa = sum(cgpa)/len(cgpa)
    sum_squared_diff = sum((x - mean_cgpa) ** 2 for x in cgpa)
    team_sd = (sum_squared_diff / len(cgpa)) ** 0.5
    if team_sd > sd_grp * 1.5 or team_sd < sd_grp * 0.7:
        return False
    
    return True'''

        
#WRITING CONETNT TO ANOTHER FILE WITH ASSIGNED TEAMS
def write_csv(grp):
    for team in grp:
        for student in team:
            row = (f"{student["TG"]},{student["ID"]},{student["School"]},{student["Name"]},{student["Gender"]},{student["GPA"]},{student["Team Number"]},{student["Anomaly"]}\n")
            f2.write(row)

#EXECUTION:
tut_grp = [] #DIVIDING STUDENTS ON THE BASIS OF TUT GROUPS
tut_grp_div()
anomalies = 0

#WRITING CONTENT TO ANOTHER FILE WITH ASSIGNED TEAMS
header = (f"TG,ID,School,Name,Gender,GPA,Team Number\n")
f2.write(header)

for i in tut_grp: #DIVISION OF TEAMS
    sd_grp = calc_sd(i)
    grp = teams_of_5(i)
    write_csv(grp)
    for team in grp:
        for student in team:
            if student["Anomaly"] == 1:
                anomalies += 1

print("The total number of anomalies are: ", anomalies/5)
f2.close() #CLOSING FILE TO SAVE CHANGES