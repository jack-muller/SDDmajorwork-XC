from app import app
import os

from flask import render_template, flash, redirect, url_for, request
from flask import jsonify
#from app.forms import LoginForm
import bcrypt

global rne
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
@app.route('/landingpage')
def landingpage():
    return render_template('landingpage.html', title='landingpage')


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
    return render_template('home.html', title='Home', posts=posts, userCurrent=user)


@app.route('/login', methods=['POST', 'GET'])
def login():
    # form = LoginForm()
    # return render_template('login.html', title='Login', form=form)
    print(f'{request.method}')
    if (request.method == "POST"):
        print(f'{request.method} I am in')
        usernameEntered = request.form['lusername']
        passwordEntered = request.form['lpassword']

        passwordBytes = passwordEntered.encode('utf-8')
        salt = b'$2b$12$terrycrewsisabigboy.Iu'
        hashPassword = bcrypt.hashpw(passwordBytes, salt)
        strHashPass = str(hashPassword)
        f = open("app/users.txt", "r")
        for i in f:
            v = i.split("|")
            if (v[0] == usernameEntered):
                if (strHashPass == v[1]):
                    return redirect(url_for('home'))
        f.close()
        return redirect(url_for('login'))
    else:
        return render_template('login.html', title='Login')
        
@app.route('/register', methods=['POST', 'GET'])
def register():
    # to register - the form must have first name, last name, username, password. 
    # It will write the blokes into the file
    if (request.method == "POST"):
        print("we're in")
        with open("app/users.txt", "r+") as f:
            print("the file has been opened")
            newusername = request.form['rusername']
            newpassword = request.form['rpassword']
            newfirstname = request.form['rfname']
            newlastname = request.form['rlname']
            newadmintag = request.form['atag']
            newusernameCheck = True
            newpasswordCheck = True
            newusernametaken = False
            newfirstnameCheck = True
            newlastnameCheck = True
            validadmintag = True

            if validadmintag == True:
                print("checking if admin is a number")
                if newadmintag.isnumeric() == True:
                    print("yup")
                else:
                    validadmintag = False
                    print("wompwomp not a number")


            if newusernameCheck == True:
                print("im checking whether the username is sweet")
                for i in newusername:
                    if i == '|':
                        newusernameCheck = False
                    else:
                        print("The username is sweet")
                        #pass
                for i in f:
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
                    
            if newpasswordCheck == True:
                print("checking if the password is sweet")
                for i in newpassword:
                    if i == '|':
                        newpasswordCheck = False
                        print("the password was not g")
                    else:
                        print("the password is g")
                        #pass
            
            if newfirstnameCheck == True:
                print("Come over here I'm feeling alphanumerical")
                if newfirstname.isalpha() == False:
                    newfirstnameCheck == False
                    print("your name ain't alphanumerical")
                else:
                    print("your first name is alpha")
                    #pass
                    
            if newlastnameCheck == True:
                    print("lemme check if your last name is alpha")
                    if newlastname.isalpha() == False:
                        newlastnameCheck == False
                        print("non alpha last name")
                    else:
                        print("alpha last name")
                        #pass
            
            print("all g we moving on")

            def passwordencryptor(passwordEntered):
                passwordBytes = passwordEntered.encode('utf-8')
                salt = b'$2b$12$terrycrewsisabigboy.Iu'
                hashPassword = bcrypt.hashpw(passwordBytes, salt)
                strHashPass = str(hashPassword)
                return strHashPass


            if newfirstnameCheck and newlastnameCheck and newpasswordCheck and newusernameCheck and validadmintag and not newusernametaken:
                print("time to write to the file")
                # write all of the things into a file:
                f.write(f'\n{newusername}|{passwordencryptor(newpassword)}|{newfirstname}|{newlastname}|{newadmintag}')
                #flash('Registration successful! Now you can log in!', 'success')
                return redirect(url_for('login'))
            else:
                print("the checks failed - the new account details are funky")
                error_message = "Registration failed. Username might be same as someone else's, or other details may be incorrect."
                return render_template('register.html', title='Register', error_message=error_message)
    else:
        # return redirect(url_for('login'))
        print('wee woo')
        #flash('ERROR. IDK WHAT HAPPENED', 'error')
        return render_template('register.html', title='Register')


@app.route('/athletemaker', methods=['POST', 'GET'])
def athletemaker():
    if (request.method == "POST"):
        with open("app/athletes.txt", "a") as f:
            firstname = request.form['fname']
            lastname = request.form['lname']
            athletenumber = request.form['acode']
            agegroup = request.form['agegroup']
            school = request.form['school']
            athletenumbervalid = True
            firstnamevalid = True
            lastnamevalid = True

            if athletenumbervalid == True:
                    print("checking if athleteno. is a number")
                    if athletenumber.isnumeric() == True:
                        print("Athlete number is numeric")
                    else:
                        athletenumbervalid = False
                        print("wompwomp not a number")
            
            print('next')
            
            if firstnamevalid == True:
                if firstname.isalpha() == True:
                    print("First name is alpha")
                else:
                    firstnamevalid = False
                    print("First name isn't alpha")
            print('next')
            if lastnamevalid == True:
                if lastname.isalpha() == True:
                    print("Last name is alpha")
                else:
                    lastnamevalid = False
                    print("Last name is not alpha")

            print(f'firstname: {firstname}')
            print(f'is firstname valid: {firstnamevalid}')
            print(f'lastname: {lastname}')
            print(f'is last name valid: {lastnamevalid}')
            print(f'athlete number: {athletenumber}')
            print(f'is athlete no. valid: {athletenumbervalid}')
            print(f'agegroup: {agegroup}')
            

            if lastnamevalid and firstnamevalid and athletenumbervalid:
                    print("time to write to the file")
                    # write all of the things into a file:
                    
                    f.write(f'\n{firstname}|{lastname}|{athletenumber}|{agegroup}|{school}')
                    #flash('Registration successful! Now you can log in!', 'success')
                    return render_template('athletemaker.html', title='Athlete Maker')
            else: 
                print("the checks failed - the new account details are funky")
                error_message = "athlete not valid"
                return render_template('athletemaker.html', title='Athlete Maker', error_message=error_message)
    
    else:
        # return redirect(url_for('login'))
        print('wee woo')
        return render_template('athletemaker.html', title='Athlete Maker')
    

@app.route('/previous_results', methods=['POST', 'GET'])
def previousresults():
    if (request.method == "GET"):
        seasondict = {}
        currentseason = read_number()
        for i in range(1, currentseason + 1):
            season_dir = os.path.join('app', 'races', f'season{i}')
            all_entries = os.listdir(season_dir)
            seasondict[season_dir] = all_entries
        print(seasondict)
        return render_template('previous_results.html', title='Previous Results', seasondict=seasondict)   
    else:
        seasondict = {}
        currentseason = read_number()
        for i in range(1, currentseason + 1):
            season_dir = os.path.join('app', 'races', f'season{i}')
            all_entries = os.listdir(season_dir)
            seasondict[season_dir] = all_entries
        print(seasondict)
        return render_template('previous_results.html', title='Previous Results', seasondict=seasondict)

@app.route('/scorer', methods=['POST', 'GET'])
def scorer():
    return render_template('scorer.html', title='Scorer') 

@app.route('/increment', methods=['POST'])
def increment():
    new_number = read_number() + 1
    write_number(new_number)

    new_dir1 = os.path.join('app', 'races', f'season{new_number}')
    os.makedirs(new_dir1, exist_ok=True)
    
    transferathletes = []
    with open('app/athletes.txt', 'r') as f:
        for line in f:
            linelist = line.strip().split('|')
            transferathletes.append(int(linelist[2]))

    race_file_path = os.path.join('app', 'individualscores', f'indivboardseason{new_number}.txt')
    with open(race_file_path, 'a') as f:
        for i in transferathletes:
            f.write(f'{i}:0\n')
    
    race_file_path = os.path.join('app', 'schoolscores', f'schoolboardseason{new_number}.txt')
    with open(race_file_path, 'a') as f:
        f.write("Scots:0\n")
        f.write("Kings:0\n")
        f.write("Shore:0\n")
        f.write("Newington:0\n")
        f.write("Grammar:0\n")
        f.write("Riverview:0\n")
        f.write("High:0\n")
        f.write("Joeys:0\n")
        

    return jsonify({'number': new_number})

def read_number():
    with open("app/season.txt", "r") as f:
        season_no = int(f.readline().strip())
    return season_no

def write_number(new_number):
    f = open("app/season.txt", "w")
    f.write(f'{new_number}')
    pass

@app.route('/newrace', methods=['POST', 'GET'])
def newrace():
    global rne
    print(f'{request.method}')
    if (request.method == "POST"):
        print(f'{request.method} I am in this')
        racenameentered = request.form['nameofraceinput'] 
        rne = racenameentered
        agegroupentered = request.form['agegroupinput']
        coordnameentered = request.form['coordinatorinput']
        coursenameentered = request.form['coursenameinput']

        if racenameentered.isalpha() and coordnameentered.isalpha():
            currentseason = read_number()
            season_dir = os.path.join('app', 'races', f'season{currentseason}')

            os.makedirs(season_dir, exist_ok=True)
            race_file_path = os.path.join(season_dir, f'{racenameentered}.txt')
            
            with open(race_file_path, 'w') as f:
                f.write(f"{racenameentered}|{agegroupentered}|{coordnameentered}|{coursenameentered}")

        
        return redirect(url_for('beginscanning'))

    else:
        return render_template('newrace.html', title='New Race')
    
def read_number():
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

def check_athlete_code(athlete_code):
    with open("app/athletes.txt", "r") as f:
        listofathletes = f.readlines()
        for i in listofathletes:
            i = i.split("|")
            if i[2] == athlete_code:
                return True
        return False

def get_athlete_name(athlete_code):
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

def get_next_place(path):
    with open(path, 'r') as f:
        Lines = f.readlines()
        return len(Lines)
    

@app.route('/removerunner', methods=['POST'])
def removerunner():
    #needs to find the runner that its associated with
    racenameentered = rne

    currentseason = read_number()
    season_dir = os.path.join('app', 'races', f'season{currentseason}')

    os.makedirs(season_dir, exist_ok=True)
    race_file_path = os.path.join(season_dir, f'{racenameentered}.txt')
    pass

@app.route('/view_race_results', methods=['POST'])
def view_race_results():
    file_path = request.form.get('file_path')
    # Logic to read the file and display its contents
    race = file_path.split('/')[-1]
    with open(file_path, 'r') as f:
        next(f)
        race_dict = {}
        for line in f:
            a = line.strip().split(':')
            name = get_athlete_name(a[1])
            race_dict[a[0]] = f'{a[1]} ({name})'
            
    
    return render_template('viewresults.html', race_dict=race_dict, title="View Race Results", race=race)

def get_athlete_name(athlete_code):
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
        seasondict[season_dir] = all_races
    
    print(seasondict)

    indiv_board_path = f'app/individualscores/indivboardseason{currentseason}.txt'

    # step 1: Read and reset scores
    reset_scores = []

    with open(indiv_board_path, 'r') as f:
        for line in f:
            athlete_id, _ = line.strip().split(':')  # Split line into athlete ID and score
            reset_scores.append(f'{athlete_id}:0')  # Reset score to 0

# Step 2: Write the reset scores back to the file
    with open(indiv_board_path, 'w') as f:
        for entry in reset_scores:
            f.write(entry + '\n')

    x = os.path.join('app', 'races', f'season{currentseason}')
    indivscoredict = {}
    with open(f'app/individualscores/indivboardseason{currentseason}.txt', 'r') as p:
                for line in p:
                    athlete_id, score = line.strip().split(":")
                    indivscoredict[athlete_id] = int(score)
    for race in all_races:
        file_path = f'{x}/{race}'
        with open(file_path, 'r') as f:
            next(f)
            for line in f:
                placing, athlete_id = line.strip().split(':')
                placing = int(placing)
                if athlete_id in indivscoredict:
                    indivscoredict[athlete_id] += placing  # Add the placing to the current score
                else:
                    indivscoredict[athlete_id] = placing

    with open(f'app/individualscores/indivboardseason{currentseason}.txt', 'w') as p:
        for athlete_id, score in indivscoredict.items():
            p.write(f'{athlete_id}:{score}\n')

    scores = []

    with open(f'app/individualscores/indivboardseason{currentseason}.txt', 'r') as f:
        for line in f:
            athlete_id, score = line.strip().split(':')
            scores.append((athlete_id, int(score)))

    def bubble_sort(arr):
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

    bubble_sort(scores)

    with open(indiv_board_path, 'w') as f:
        for athlete_id, score in scores:
            f.write(f'{athlete_id}:{score}\n')
    
    #school standing for the season:

    #previous Individual winners

    #previous school winners

    return render_template('statspage.html', title="Statistics Page", indivscoredict=indivscoredict, currentseason=currentseason)

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