#IMPORTED FUNCTIONS
import random
import os

#GET CURRENT DIRECTORY
cwd = os.getcwd()

#OPENING NEW CSV FILE TO WRITE DATA
f2 = open("FCS5_team4_JindalKhanak.csv", "w", newline = "")

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

            d = {} #STORING EACH STUDENT RECORD AS A DICTIONARY
            d["TG"] = i[0]
            d["ID"] = i[1]
            d["School"] = i[2]
            d["Name"] = i[3]
            d["Gender"] = i[4]
            d["GPA"] = float(i[5])
            l.append(d)

    if len(l) == 50: # WHEN ALL 50 STUDENTS FROM A TUT GROUP ARE SORTED, ADDING THEN TO THE MAIN TUT_GRP LIST
        tut_grp.append(sorted(l, key=lambda x: x["GPA"])) #SORT STUDENTS BASED ON CGPA

#CALCULATING THE MEAN CGPA OF THE ENTIRE TUT GROUP
def calc_mean(grp): 
    cgpas = [student['GPA'] for student in grp]
    mean_cgpa = sum(cgpas)/len(cgpas)
    return mean_cgpa

#CALCULATING THE TOTAL NUMBER OF FEMALES AND MALES IN EACH TUT GROUP
def total_f_m(grp):
    females = 0
    males = 0
    for student in grp:
        if student["Gender"] == "Female":
            females += 1
        else:
            males += 1
    return females, males

#CHECK TEAM DIVERSITY IN TERMS OF SCHOOL, CGPA, GENDER
def diversity(schools, gender, cgpa, mean_cgpa, f, m):
    
    #SCHOOL DIVERSITY CHECKING
    for i in schools:
        if schools.count(i) > 3: #A TEAM SHOULD NOT HAVE MORE THAN 3 STUDENTS BELONGING TO THE SAME SCHOOL
            return False

    #GENDER DIVERSITY CHECKING
    female_ratio = f / (f + m) #CALCULATING THE RATIO OF FEMALES IN THE TUT GROUP
    male_ratio = m / (f + m) #CALCULATING THE RATIO OF MALES IN THE TUT GROUP

    max_females = max(4, int(female_ratio * 5) + 1) #ESTIMATING THE MAX NUMBER OF FEMALES PER TEAM
    max_males = max(4, int(male_ratio * 5) + 1) #ESTIMATING THE MAX NUMBER OF MALES PER TEAM

    if gender.count("Female") > max_females or gender.count("Male") > max_males:
        return False

    #CGPA DIVERSITY CHECKING
    mean_cgpa_team = sum(cgpa)/len(cgpa) #CALCULATING THE MEAN CGPA OF THE FORMED TEAM
    bottom_limit = mean_cgpa * 0.5 #ALLOWING CGPA VARIANCE
    top_limit = mean_cgpa * 1.5 #ALLOWING CGPA VARIANCE
    if not (bottom_limit <= mean_cgpa_team <= top_limit):
        return False

    return True

#CREATING TEAMS OF 5 
def teams_of_5(x, mean_cgpa, f, m): 
    successful_teams = [] #TEAMS MEETING DIVERSITY CRITERIA LIST
    left_students = [] #STUDENTS WHOSE TEAMS DID NOT MEET DIVERSITY CRITERIA YET
    team_number = 1 #KEEPING TRACK OF ASIGNED TEAM AND TEAM NUMBER

    #ALLOTMENT OF TEAMS BY THE ZIG-ZAG METHOD (OR RIGHT TO LEFT METHOD)
    left, right = 0, len(x) - 1
    team_found = False
    iterations = 0

    while iterations < 10 and len(x) >= 5:
        team = []
        while len(team) < 5 and left <= right:
            team.append(x[left])
            left += 1
            if len(team) < 5 and left <= right:
                team.append(x[right])
                right -= 1

        if len(team) == 5:
            team_found = diversity([d["School"] for d in team], [d["Gender"] for d in team], [d["GPA"] for d in team], mean_cgpa, f, m) #RUNNING DIVERSITY CHECK

            #ON MEETING DIVERSITY CRITERIA
            if team_found:
                for student in team:
                    student["Team Assigned"] = team_number #ASSIGN TEAM NUMBER
                    student["Anomaly"] = 0 #MARK THEM AS NOT AN ANOMALY
                team_number += 1 
                successful_teams.append(team)
                team = []

            #IF IT FAILS TO MEET THE DIVERSITY CRITERIA
            else: 
                for student in team:
                    left_students.append(student)

            iterations += 1

    #SINCE THERE ARE 50 STUDENTS PER TUT GROUP, 10 TEAMS OF 5 NEED TO BE FORMED.
    if len(successful_teams) < 10:
        more_teams = distribute(left_students, mean_grp, team_number) #RUN DISTRIBUTE FUNCTION TO FORM TEAMS
        for team in more_teams:
            successful_teams.append(team)

    return successful_teams

def distribute(left, mean_grp, team_number):
    created_teams = [] #SUCCESSFULLY FORMED TEAMS
    max_attempts = 100 # TO AVOID INFINITE LOOP SITUTAION
    attempts = 0

    while len(left) >= 5:
        team_found = False

        while attempts < max_attempts:
            random.shuffle(left) #SHUFFLE TUT GROUP STUDENTS INTO A RANDOM ORDER

            team = left[:5] #CREATING A TEAM OF 5 INITIAL STUDENTS

            team_found = diversity([d["School"] for d in team], [d["Gender"] for d in team], [d["GPA"] for d in team], mean_grp, f, m) #RUNNING DIVERSITY CHECK

            #IF TEAM METS DIVERSITY CRITERIA:
            if team_found:
                for student in team:
                    student["Team Assigned"] = team_number#ASSIGN TEAM NUMBER
                    student["Anomaly"] = 0 #MARK THEM AS NOT AN ANOMALY
                team_number += 1
                created_teams.append(team)

                team = []
                left = left[5:] #REMOVE INITIAL 5 STUDENTS FRON THE LEFT STUDENTS LIST
                break
            attempts += 1

        #NOT MEETING DIVERSITY CRITERIA
        else:
            team = left[:5] #CREATE A TEAM FO 5 INITIAL STUDENTS
            for student in team:
                    student["Team Assigned"] = team_number
                    student["Anomaly"] = 1 #MARK THEM AS ANOMALY
            team_number += 1
            created_teams.append(team)
            left = left[5:]

    return created_teams

#WRITING CONETNT TO ANOTHER FILE WITH ASSIGNED TEAMS
def write_csv(grp):
    for team in grp:
        for student in team:
            row = (f"{student['TG']},{student['ID']},{student['School']},{student['Name']},{student['Gender']},{student['GPA']},{student['Team Assigned']},{student['Anomaly']}\n")
            f2.write(row)

tut_grp = [] #DIVIDING STUDENTS ON THE BASIS OF TUT GROUPS
tut_grp_div()
anomalies = 0

header = (f"TG,ID,School,Name,Gender,GPA,Team Assigned\n")
f2.write(header)

#MAIN EXECUTION
for i in tut_grp: #DIVISION OF TEAMS
    mean_grp = calc_mean(i)
    f, m = total_f_m(i)
    grp = teams_of_5(i, mean_grp, f, m)
    for team in grp:
        for student in team:
            if student["Anomaly"] == 1:
                anomalies += 1
    write_csv(grp)

print("The total number of anomalies are: ", anomalies/5)
f2.close()