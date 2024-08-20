def load_users():
    users = []
    with open("app/users.txt", "r") as file:
        for line in file:
            # Split each line by commas
            username,password,firstname,lastname,admintag = line.strip().split('|')
            # Append the athlete data to the list as a dictionary
            users.append({
                'uname': username,
                'pword': password,
                'fname': firstname,
                'lname': lastname, 
                'atag': admintag,
            })
    return users

users = load_users()

print(users)