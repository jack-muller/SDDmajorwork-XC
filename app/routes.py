from app import app
import os
import operator

from flask import render_template, flash, redirect, url_for, request
from flask import jsonify
#from app.forms import LoginForm
import bcrypt

global rne # this was the most logical way I could figure out to pass this important variable from one route to another.
rne = ""
# def load_users():
#     users = []
#     with open("app/users.txt", "r") as file:
#         for line in file:
#             # Split each line by commas
#             username,password,firstname,lastname,admintag = line.strip().split('|')
#             # Append the athlete data to the list as a dictionary
#             users.append({
#                 'uname': username,
#                 'pword': password,
#                 'fname': firstname,
#                 'lname': lastname, 
#                 'atag': admintag,
#             })
#     return users

# users = load_users()

# print(users)

# class User():
#     def __init__(self, username, password, firstname, lastname, admintag):
#         self.id = username
#         self.status = users[admintag]['status']

#     def get_status(self):
#         return self.status

#     def toggle_status(self):
#         users[self.id]['status'] = not users[self.id]['status']
#         self.status = users[self.id]['status']

@app.route('/')
@app.route('/landingpage') # this means that when the user starts up the page with http://whatever/, they will get sent to the landing page
def landingpage():
    return render_template('landingpage.html', title='landingpage') #renders the landing page template in templates


@app.route('/home')
def home():
    user = {"username": "MrLankyBean"}
    posts = [
        {
            'author': {"username": "Wizzythewizard"},
            'body': "you want to fight let's fight"
        },
        {
            'author': {"username": "MrLankyGone"},
            'body': "what a ruckus"
        }
    ]
    return render_template('home.html', title='Home', posts=posts, userCurrent=user) # renders the home page template in templates


@app.route('/login', methods=['POST', 'GET'])  
def login():
    # form = LoginForm()
    # return render_template('login.html', title='Login', form=form)
    print(f'{request.method}')
    if (request.method == "POST"): # the method is POST after they submit the login form, and the submit button posts the data
        print(f'{request.method} I am in')
        usernameEntered = request.form['lusername'] # receives username
        passwordEntered = request.form['lpassword'] # receives password

        passwordBytes = passwordEntered.encode('utf-8')
        salt = b'$2b$12$terrycrewsisabigboy.Iu' # haha funny salt
        hashPassword = bcrypt.hashpw(passwordBytes, salt)
        strHashPass = str(hashPassword) # one way encryption of passwords using bcrypt
        f = open("app/users.txt", "r") # open the file that has all the users created by /register route.
        for i in f:
            v = i.split("|")
            if (v[0] == usernameEntered): #this if checks to find the username of the user
                if (strHashPass == v[1]): #checks to see if their encrypted password is the same as the encrypted version of the password they added upon login.
                    return redirect(url_for('home')) #if its sweet then you get sent to the homepage
        f.close()
        return redirect(url_for('login'))#if its not sweet you get sent back to login rip.
    else:
        return render_template('login.html', title='Login') # this is just for pageloading if you get the page by clicking another button somewhere (e.g. on landing page).
        
@app.route('/register', methods=['POST', 'GET']) 
def register():
    # to register - the form must have first name, last name, username, password. 
    # It will write the blokes into the file
    if (request.method == "POST"): # this will trigger after on the register page, someone submits their details
        print("we're in")
        with open("app/users.txt", "r+") as f:
            print("the file has been opened")
            # all of this stuff below is just getting data from the submitted form
            newusername = request.form['rusername']
            newpassword = request.form['rpassword']
            newfirstname = request.form['rfname']
            newlastname = request.form['rlname']
            newadmintag = request.form['atag']
            #all of these are booleans for validation purposes.
            newusernameCheck = True
            newpasswordCheck = True
            newusernametaken = False
            newfirstnameCheck = True
            newlastnameCheck = True
            validadmintag = True

            if validadmintag == True: # checking to make sure the people haven't said they're like 22's or something random.
                print("checking if admin is a number")
                if newadmintag in ['0', '1']:
                    print("yup")
                else:
                    validadmintag = False
                    print("wompwomp not a number")


            if newusernameCheck == True: #makes sure the username doesn't have a character that is used as a delimiter later
                print("im checking whether the username is sweet")
                for i in newusername:
                    if i == '|':
                        newusernameCheck = False
                    else:
                        print("The username is sweet")
                        #pass
                for i in f: #makes sure no-one else has the username, although the print statements I used for testing make that pretty clear
                    print("I'm checking whether someone else has the username")
                    v = i.split('|')
                    print(v)
                    print(f'this is the other guys username: "{v[0]}"')
                    print(f'this is the new username: "{newusername}"')
                    if v[0] == newusername:
                        newusernametaken = True
                        print("someone else has it")
                    else:
                        print("nope not this person")
                        #pass     
                    
            if newpasswordCheck == True: #passwords can be anything, just not already used by someone else.
                print("checking if the password is sweet")
                for i in newpassword:
                    if i == '|':
                        newpasswordCheck = False
                        print("the password was not g")
                    else:
                        print("the password is g")
                        #pass
            
            if newfirstnameCheck == True: #firstname must be alphabetical, thus we check for that
                print("Come over here I'm feeling alphanumerical")
                if newfirstname.isalpha() == False:
                    newfirstnameCheck = False
                    print("your name ain't alphanumerical")
                else:
                    print("your first name is alpha")
                    #pass
                    
            if newlastnameCheck == True: #last names must also be alphabetical. Yes I'm discriminating against Elon Musk's kid.
                    print("lemme check if your last name is alpha")
                    if newlastname.isalpha() == False:
                        newlastnameCheck = False
                        print("non alpha last name")
                    else:
                        print("alpha last name")
                        #pass
            
            print("all g we moving on")

            def passwordencryptor(passwordEntered): #this is where the passwords are encrypted so people with access to the users file can't steal other peoples password!
                passwordBytes = passwordEntered.encode('utf-8')
                salt = b'$2b$12$terrycrewsisabigboy.Iu'
                hashPassword = bcrypt.hashpw(passwordBytes, salt)
                strHashPass = str(hashPassword)
                return strHashPass #lovely :)

            # checks to make sure all of the booleans are ok before writing to the file. If one fails then we shut the joint down.
            if newfirstnameCheck and newlastnameCheck and newpasswordCheck and newusernameCheck and validadmintag and not newusernametaken:
                print("time to write to the file")
                # write all of the things into a file:
                f.write(f'\n{newusername}|{passwordencryptor(newpassword)}|{newfirstname}|{newlastname}|{newadmintag}')
                #flash('Registration successful! Now you can log in!', 'success')
                return redirect(url_for('login'))
            else:
                #rahhh it failed >:( grrrr
                print("the checks failed - the new account details are funky")
                error_message = "Registration failed. Username might be same as someone elses, or other details may be incorrect."
                return render_template('register.html', title='Register', error_message=error_message) 
                # I sent the error message through within the render_template to use the jinja2 stuff and create some changing error messages within the html file.
    else:
        # return redirect(url_for('login'))
        print('wee woo')
        #flash('ERROR. IDK WHAT HAPPENED', 'error')
        return render_template('register.html', title='Register') 


@app.route('/athletemaker', methods=['POST', 'GET'])
def athletemaker():
    if (request.method == "POST"):
        with open("app/athletes.txt", "a") as f:
            firstname = request.form['fname'] #gets firstname from form
            lastname = request.form['lname'] #gets lastname from form
            athletenumber = request.form['acode'] #gets athletecode from form
            agegroup = request.form['agegroup'] #gets agegroup from form
            school = request.form['school'] #school from form
            athletenumbervalid = True #the dropdowns don't need validators as I can control their choices. 
            firstnamevalid = True
            lastnamevalid = True

            if athletenumbervalid == True: #validation for athlete code, which I just want to be a number
                    print("checking if athleteno. is a number")
                    if athletenumber.isnumeric() == True: #thus I check whether its numeric
                        print("Athlete number is numeric")
                    else:
                        athletenumbervalid = False
                        print("wompwomp not a number")
            
            print('next')
            
            if firstnamevalid == True: #is firstname alphabetic
                if firstname.isalpha() == True:# yes
                    print("First name is alpha")
                else:
                    firstnamevalid = False #no, change up that bool
                    print("First name isn't alpha")
            print('next')
            if lastnamevalid == True: #is last name valid
                if lastname.isalpha() == True:
                    print("Last name is alpha")
                else:
                    lastnamevalid = False #reassign value
                    print("Last name is not alpha")

            print(f'firstname: {firstname}') # this stuff helped me to check the feedback and find where errors were during the coding process.
            print(f'is firstname valid: {firstnamevalid}')
            print(f'lastname: {lastname}')
            print(f'is last name valid: {lastnamevalid}')
            print(f'athlete number: {athletenumber}')
            print(f'is athlete no. valid: {athletenumbervalid}')
            print(f'agegroup: {agegroup}')
            

            if lastnamevalid and firstnamevalid and athletenumbervalid: #check to make sure
                    print("time to write to the file")
                    # write all of the things into a file:
                    
                    f.write(f'\n{firstname}|{lastname}|{athletenumber}|{agegroup}|{school}') #yep thats good
                    #flash('Registration successful! Now you can log in!', 'success')
                    #don't have to close it as I opened the file in a pythonic way :)
                    return render_template('athletemaker.html', title='Athlete Maker')
            else: 
                print("the checks failed - the new account details are funky")
                error_message = "athlete not valid" # look its a cool personalised error message
                return render_template('athletemaker.html', title='Athlete Maker', error_message=error_message) # error got passed in thru here.
    
    else:
        # return redirect(url_for('login'))
        print('wee woo')
        return render_template('athletemaker.html', title='Athlete Maker') #if they want info passed to them, they GET it, therefore only page renders.
    

@app.route('/previous_results', methods=['POST', 'GET'])
def previousresults():
    if (request.method == "GET"):
        seasondict = {} #season dictionary
        currentseason = read_number() #this is important, so that I don't go out of range and also so I look through all of the files
        for i in range(1, currentseason + 1): #look through all season files
            season_dir = os.path.join('app', 'races', f'season{i}') #path for each season file from 1 to current
            all_entries = os.listdir(season_dir) #all_entries is a list of all txt files in each folder.
            seasondict[season_dir] = all_entries #make a dictionary relating the season folder to all of its races
        print(seasondict)
        return render_template('previous_results.html', title='Previous Results', seasondict=seasondict) # send the dict through to the html page, where each file will be displayed by a jinja2 loop
    else:
        #this is the same thing, I put it here because I didn't really know what to do but it broke nothing touch wood.
        seasondict = {} 
        currentseason = read_number()
        for i in range(1, currentseason + 1):
            season_dir = os.path.join('app', 'races', f'season{i}')
            all_entries = os.listdir(season_dir)
            seasondict[season_dir] = all_entries
        print(seasondict)
        return render_template('previous_results.html', title='Previous Results', seasondict=seasondict)

@app.route('/scorer', methods=['POST', 'GET']) #scorer is a nav page, hasn't got much going for it
def scorer():
    current_season = read_number()
    return render_template('scorer.html', title='Scorer', number=current_season) #pass the current season in as the new season button will increment it.

def read_number(): # a function to return the current season, very helpful
    with open("app/season.txt", "r") as f:
        season_no = int(f.readline().strip())
    return season_no

@app.route('/increment', methods=['POST']) # functionality to increment the current season+1
def increment():
    new_number = read_number() + 1 #increments
    write_number(new_number) #writes it back to the file

    new_dir1 = os.path.join('app', 'races', f'season{new_number}')
    os.makedirs(new_dir1, exist_ok=True) #makes a new file for the new season
    
    transferathletes = [] #this is used to move all of the athletes to the next season folder, initialised with zero score.
    with open('app/athletes.txt', 'r') as f:
        for line in f:
            linelist = line.strip().split('|')
            transferathletes.append(int(linelist[2])) #just gets the old athletes codes

    race_file_path = os.path.join('app', 'individualscores', f'indivboardseason{new_number}.txt')#makes a new leaderboard for individuals
    with open(race_file_path, 'a') as f:
        for i in transferathletes: # move all of the athletes to the new leaderboard, making all scores 0 at the start of the new season
            f.write(f'{i}:0\n')
    
    race_file_path = os.path.join('app', 'schoolscores', f'schoolboardseason{new_number}.txt') # new txt file for school leaderboard at the start of a new season
    with open(race_file_path, 'a') as f: #in the new leaderboard file path, create a new leaderboard of schools with no scores
        f.write("Scots:0\n")
        f.write("Kings:0\n")
        f.write("Shore:0\n")
        f.write("Newington:0\n")
        f.write("Grammar:0\n")
        f.write("Riverview:0\n")
        f.write("High:0\n")
        f.write("Joeys:0\n")
        

    return jsonify({'number': new_number}) #returns the number so that the number underneath the new season button updaates.

def read_number(): #function to return the current season number, which has been used before
    with open("app/season.txt", "r") as f:
        season_no = int(f.readline().strip())
    return season_no

def write_number(new_number): # this function writes the new season number to the season.txt file
    f = open("app/season.txt", "w")
    f.write(f'{new_number}')
    pass

import re
@app.route('/newrace', methods=['POST', 'GET'])
def newrace():
    racename_pattern = r'^[a-zA-Z0-9 ]+$'  # Allows letters, numbers, and spaces
    coordname_pattern = r'^[a-zA-Z ]+$' # Allows letters and spaces
    global rne #global racenameentered variable. 
    print(f'{request.method}')
    if (request.method == "POST"):
        print(f'{request.method} I am in this')
        racenameentered = request.form['nameofraceinput'] 
        rne = racenameentered #this gets used later as well for some calculations and such
        agegroupentered = request.form['agegroupinput'] #age group
        coordnameentered = request.form['coordinatorinput'] #name of coordinator
        coursenameentered = request.form['coursenameinput'] #name of course, this is a drop down

        if re.fullmatch(racename_pattern, racenameentered) and re.fullmatch(coordname_pattern, coordnameentered): #make sure there aren't rogue characters
            currentseason = read_number() #get current season again
            season_dir = os.path.join('app', 'races', f'season{currentseason}') #get the directory to the current season folder

            os.makedirs(season_dir, exist_ok=True) #make sure the directory exists and if not create it
            race_file_path = os.path.join(season_dir, f'{racenameentered}.txt') #make a new file with racenameentered
            
            with open(race_file_path, 'w') as f: #write to the fie the identifying header
                f.write(f"{racenameentered}|{agegroupentered}|{coordnameentered}|{coursenameentered}") # this is the identifying header
        else:
            return redirect(url_for('newrace')) #reject if it doesn't work

        
        return redirect(url_for('beginscanning'))

    else:
        return render_template('newrace.html', title='New Race') # for the GET times
    
def read_number(): #wow never seen this before
    with open("app/season.txt", "r") as f:
        season_no = int(f.readline().strip())
    return season_no

@app.route('/beginscanning', methods=['GET', 'POST'])
def beginscanning():
    print(f'{request.method} HIHIHIHI')
    if (request.method == "POST"):
        athleteCode = request.form['athlete_code']
        racenameentered = rne

        currentseason = read_number()
        season_dir = os.path.join('app', 'races', f'season{currentseason}')

        os.makedirs(season_dir, exist_ok=True)
        race_file_path = os.path.join(season_dir, f'{racenameentered}.txt')
        
        athInFile = False
        if check_athlete_code(athleteCode):
            with open(race_file_path, 'r') as f:
                linesOfFile = f.readlines()
                for i in linesOfFile:
                    if ":" in i:
                        d = i.split(":")
                        print(d[1])
                        if d[1].strip() == athleteCode:
                            athInFile = True
                if athInFile == False:
                    with open(race_file_path, 'a') as f:
                        f.write(f"\n{get_next_place(race_file_path)}:{athleteCode}")
                noAthlete = False
        else:
            noAthlete = True
        
        with open(race_file_path, 'r') as f:
            lines = f.readlines()
            athletes = []
            for i in lines:
                if ":" in i:
                    d = i.split(":")
                    print(d[1])
                    d.append(get_athlete_name(d[1].strip()))
                    print(d[2])
                    athletes.append(d)


        return render_template('beginscanning.html', title='Scanning', athInFile=athInFile, noAthlete=noAthlete, ath = athletes)


    else:
        # return render_template('beginscanning.html')
        return render_template('beginscanning.html', title='Scanning')

def check_athlete_code(athlete_code): # the logic for the function explained above
    with open("app/athletes.txt", "r") as f:
        listofathletes = f.readlines()
        for i in listofathletes:
            i = i.split("|")
            if i[2] == athlete_code:
                return True
    return False

def get_athlete_name(athlete_code): #this returns the name of the athlete based on the athlete code that is passed in
    with open("app/athletes.txt", "r") as f:
        listofathletes = f.readlines()
        for i in listofathletes:
            i = i.split("|")
            if i[2] == athlete_code:
                name = i[0] + i[1]
                return name

# @app.route('/confirm_athlete', methods=['POST'])
# def confirm_athlete():
#     data = request.json
#     racename = data['racename']
#     athlete_code = data['athlete_code']
    
#     # Add athlete to race file
#     race_file_path = f"app/races/season{get_current_season()}/{racename}.txt"
#     with open(race_file_path, 'a') as f:
#         place = get_next_place(race_file_path)  # Implement this function
#         f.write(f"{place} {athlete_code}\n")
    
#     return jsonify({'success': True, 'place': place})

# def get_current_season():
#     with open("app/season.txt", "r") as f:
#         season_no = int(f.readline().strip())
#     return season_no

def get_next_place(path): # :)
    with open(path, 'r') as f:
        Lines = f.readlines()
        return len(Lines)
    
#this doesn't have any functionality, so I made it pass the entire thing

# @app.route('/removerunner', methods=['POST']) 
# def removerunner():
#     #needs to find the runner that its associated with
#     racenameentered = rne

#     currentseason = read_number()
#     season_dir = os.path.join('app', 'races', f'season{currentseason}')

#     os.makedirs(season_dir, exist_ok=True)
#     race_file_path = os.path.join(season_dir, f'{racenameentered}.txt')
#     pass

@app.route('/view_race_results', methods=['POST']) # a way to view previous races
def view_race_results():
    file_path = request.form.get('file_path') # this gets send through
    # Logic to read the file and display its contents
    race = file_path.split('/')[-1]
    with open(file_path, 'r') as f:
        next(f)
        race_dict = {}
        for line in f:
            a = line.strip().split(':')
            name = get_athlete_name(a[1]) #a[1] is the athlete's code
            race_dict[a[0]] = f'{a[1]} ({name})' #assigning name and code to the placing
            
    
    return render_template('viewresults.html', race_dict=race_dict, title="View Race Results", race=race)

def get_athlete_name(athlete_code): #once again.
    with open("app/athletes.txt", "r") as f:
        listofathletes = f.readlines()
        for i in listofathletes:
            i = i.split("|")
            if i[2] == athlete_code:
                name = i[0] + i[1]
                return name
            
@app.route('/statspage', methods=['GET', 'POST'])
def statspage():
    #individual standing for the season:
    seasondict = {}
    currentseason = read_number()
    for i in range(1, currentseason + 1):
        season_dir = os.path.join('app', 'races', f'season{i}')
        all_races = os.listdir(season_dir)
        seasondict[season_dir] = all_races #relates the season file to the name of lists of all of the race names entered
    
    indiv_board_path = f'app/individualscores/indivboardseason{currentseason}.txt' #path to each individual race

    # step 1: Read and reset scores
    reset_scores = [] 

    with open(indiv_board_path, 'r') as f:
        for line in f:
            athlete_id, _ = line.strip().split(':')  # Split line into athlete ID and score
            reset_scores.append(f'{athlete_id}:0')  # Reset score to 0

    # Step 2: Write the reset scores back to the file
    with open(indiv_board_path, 'w') as f:
        for entry in reset_scores:
            f.write(entry + '\n') #I had to reset scores each time page is loaded, else each time someone POSTs the scores add onto themselves

    x = os.path.join('app', 'races', f'season{currentseason}')
    indivscoredict = {}
    with open(f'app/individualscores/indivboardseason{currentseason}.txt', 'r') as p:
                for line in p:
                    athlete_id, score = line.strip().split(":")
                    indivscoredict[athlete_id] = int(score) # assign the scores 0 to a dictionary so they can be changed
    for race in all_races:
        file_path = f'{x}/{race}' #getting the placings from the current races that exist
        with open(file_path, 'r') as f:
            next(f)
            for line in f:
                placing, athlete_id = line.strip().split(':') #split the delimited file
                placing = int(placing)
                if athlete_id in indivscoredict:
                    indivscoredict[athlete_id] += placing  # Add the placing to the current score
                else:
                    indivscoredict[athlete_id] = placing #if the athlete didn't race, nothing happesn

    with open(f'app/individualscores/indivboardseason{currentseason}.txt', 'w') as p:
        for athlete_id, score in indivscoredict.items():
            p.write(f'{athlete_id}:{score}\n') #write the freshly assigned scores back

    scores = [] #made for sorting reasons

    with open(f'app/individualscores/indivboardseason{currentseason}.txt', 'r') as f:
        for line in f:
            athlete_id, score = line.strip().split(':')
            scores.append((athlete_id, int(score)))

    def bubble_sort(arr): #this is a devious bubble sort that I copied almost word for word from the textbook
        # the bubble sort sorts the athletes by their schors
        n = len(arr)
        swapped = True
        pass_num = 0
        while swapped:
            swapped = False
            comparison = 0
            while comparison < n - 1 - pass_num:
                if arr[comparison][1] > arr[comparison + 1][1]:
                    # Swap the elements
                    arr[comparison], arr[comparison + 1] = arr[comparison + 1], arr[comparison]
                    swapped = True
                comparison += 1
            pass_num += 1
        return arr

    bubble_sort(scores) #yay sorted

    with open(indiv_board_path, 'w') as f:#write everything back
        for athlete_id, score in scores:
            f.write(f'{athlete_id}:{score}\n') #with the new updated, sorted scores
    
    #school standing for the season:

    
    school_board_path = f'app/schoolscores/schoolboardseason{currentseason}.txt' #this is a route to the school standings leaderboard file
    athletes_path = "app/athletes.txt"
    fss = update_school_scores(currentseason, indiv_board_path, school_board_path, athletes_path)
    print(fss) 

    return render_template('statspage.html', title="Statistics Page", indivscoredict=indivscoredict, currentseason=currentseason, fss=fss)

def read_number():
    with open("app/season.txt", "r") as f:
        season_no = int(f.readline().strip())
    return season_no

def get_athlete_name(athlete_code):
    with open("app/athletes.txt", "r") as f:
        listofathletes = f.readlines()
        for i in listofathletes:
            i = i.split("|")
            if i[2] == athlete_code:
                name = i[0] + ' ' + i[1]
                return name
            
from collections import defaultdict

def update_school_scores(currentseason, indiv_board_path, school_board_path, athletes_path):
    # Step 1: Read all athlete data once
    athlete_schools = {}
    with open(athletes_path, 'r') as f: #athletes path is just athletes.txt
        for line in f:
            data = line.strip().split("|")
            athlete_schools[data[2]] = data[4] #athlete code as key and then school as value

    # Step 2: Read individual scores and group by school
    school_scores = defaultdict(list) #turns the school scores into a dictionary with a list of scores as their value
    with open(indiv_board_path, 'r') as f:
        for line in f:
            athlete_id, score = line.strip().split(':')
            school = athlete_schools.get(athlete_id)
            if school:
                school_scores[school].append(int(score)) #get some school scores appended to the school key
                print(school_scores)

    # Step 3: Calculate the top 4 scores for each school
    final_school_scores = {}
    for school, scores in school_scores.items():
        top_scores = sorted(scores)[:4] #learnt a cool new way to sort stuff, this takes the top 4 scores so they can be summed
        print(top_scores) #checking to make sure my changes were doing what I wanted them to do.
        final_school_scores[school] = sum(top_scores)

    # Step 4: Update the school scores file
    with open(school_board_path, 'w') as f:
        for school, total_score in final_school_scores.items(): # final assignment of stuff
            f.write(f'{school}: {total_score}\n')
    
    sorted_final_school_scores = dict(sorted(final_school_scores.items(), key=operator.itemgetter(1))) # this sorts them from lowest to highest in a much easier way than my freaky bubble sort.

    return sorted_final_school_scores