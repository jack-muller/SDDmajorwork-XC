from app import app

from flask import render_template, flash, redirect, url_for, request
from flask import jsonify
#from app.forms import LoginForm
import bcrypt

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
        f = open("app/users.txt", "r+")
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
            f.close()
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
        f = open("app/athletes.txt", "a")
        firstname = request.form['fname']
        lastname = request.form['lname']
        athletenumber = request.form['acode']
        agegroup = request.form['agegroup']
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
                
                f.write(f'\n{firstname}|{lastname}|{athletenumber}|{agegroup}')
                f.close()
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
    return render_template('previous_results.html', title='Previous_results')   

@app.route('/scorer', methods=['POST', 'GET'])
def scorer():
    return render_template('scorer.html', title='Scorer') 

@app.route('/increment', methods=['POST'])
def increment():
    new_number = read_number() + 1
    write_number(new_number)
    return jsonify({'number': new_number})

def read_number():
    f = open("app/season.txt", "r")
    print(f'{f}')
    season_no = int(f.readline().strip())
    f.close()
    return season_no

def write_number(new_number):
    f = open("app/season.txt", "w")
    f.write(f'{new_number}')
    pass