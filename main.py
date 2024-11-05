import os
from dataclasses import dataclass
import uuid
import getpass  # for hiding the characters of a password
import hashlib  # for hasing the password
import time

# The other modules in this application

import mydb, client, server

################################
# Modules:
#
# 1.  DB for connecting to the MySQL database, DONE!
# 2.  ClientServer for creating the client server connection, DONE but needs to be verified.
#
# Status:   
#           MySQL created and SELECT, pending update, delete
#           generate unique IDs for the users
#
#           MySQL data type varchar(64) is used for the hash password, pending testing
#
# Date:     10/24/24
#
################################


# User class

@dataclass
class User:
    
    # by default, the Disabled and Suspended fields in MySQL are 0 or false
    
    def __init__(self, id:int, fname:str, lname:str, username:str, pw:str, email:str):
        self.ID = id
        self.FirstName = fname
        self.LastName = lname
        self.Username = username
        self.Password = pw
        self.Email = email
    
    # don't need this if using dataclass as it's provided
    def __str__(self):
        return f'{self.ID} {self.FirstName} {self.LastName} {self.Username} {self.Password} {self.Email}'


# Hash the user password before storing it in the database, don't use salt


def HashThePassword(pw):
    pwBytes = pw.encode('utf-8')
    hashObj = hashlib.sha256(pwBytes)
    
    pwHash = hashObj.hexdigest()
    return pwHash   # this is the hashed password to be stored in the database
                    # when comparing the password entered by the user against the hashed password from the database
    

# Find the ID in the database 


def FindID(id: int) -> bool: 
    '''
    Find the ID of the user
    '''
    
    sql = 'SELECT id from users WHERE id = %s'
    val = (id,)
    mydb.cur.execute(sql, val)
    
    result = mydb.cur.fetchall()
    if len(result) == 0:    # result returned an empty list, id is unique (it has not been used)
        return True 
    else:
        return False        # id has already been used, ask the user to enter a different id


# Find the username in the database and return a tuple containing (username, True or None, False) 


def FindUsername(username: str) -> tuple[User, bool]:  # return a tuple of the User and truth value whether the username is found or not
    '''
    Find the Username of the user 
    '''
    
    sql = 'SELECT * from users WHERE username = %s'  # selecting the user where the 3rd value is the username
    val = (username,)
    mydb.cur.execute(sql, val)
    
    user = mydb.cur.fetchone()  # returns a tuple that looks like:  ('joelee2524',)
    
    if user is None:
        return None, False
    elif user[3] == username:     # 3rd index value is the username
        return user, True 
    
 
# Find the password for the given username

    
def FindPassword(username:str, pw:str) -> bool:
    sql = "select password from users where username = %s"  # selecting only the hash password, must compare this to the hashed password the user typed in during the login process
    val = (username,)
    
    mydb.cur.execute(sql, val)
    
    result = mydb.cur.fetchone()  # fetch only one which should be the only hashed password in the database
    
    if result[0] == HashThePassword(pw):  # compare with the first index value
        return True
    else:
        return False
    

# Enter the unique ID of the user 


def EnterID() -> int:   # returns the unique ID of the user in number only
        
    while True:         # repeat until an integer is entered for ID
        try:
            id = int(input('ID (must be unique): '))    
            
            if FindID(id):  # the id entered is unique, return it to exit the loop
                return id
            else: # the id has been used, prompt for a new ID
                print(f'\t{id} already exists!')
                next
        except:
            print('Wrong type:  Enter numbers only for the ID!')
      
        
# Enter the username and check for uniqueness


def EnterUsername() -> str:
    
    while True:
        username = input('Enter username: ')
        
        if FindUsername(username) == True:
            return username
        else:
            _ = input('Please enter a unique username!')
    

# Create a new user


def Create() -> User:
    '''
    Create a new user.  A User object will be returned.
    '''

    id = EnterID()  # make sure the ID is a number and also unique
        
    fname = input('First Name: ') 
    lname = input('Last Name: ')
    
    # EnterUsername()
    
    username = input('Username: ')                  # check username for uniqueness, reprompt if it's not
    
    # EnterPassword()
    
    pw = getpass.getpass(prompt = 'Password: ')     # the characters of the password won't be displayed using getpass.getpass()
    email = input('Email: ')   
    
    pwHash = HashThePassword(pw)   # MySQL data type of VARCHAR(64) is being used for sha256 hashes, successful INSERTed in MySQL 
          
    user = User(id, fname, lname, username, pwHash, email)  # here we are storing the user's hash password and not the original password
    
    # Create the user in the database
    mydb.CreateUser(user)

    _ = input('\nDone!  Press Enter to continue...')
    
    return user


# Log in


def Login():
    os.system('cls')
    print ('Please log in ...\n\n')
    
    userAttempts = 0
    while userAttempts < 3:
        username = input('Username: ')
        userAttempts += 1
        
        userFound = False
        user, userFound = FindUsername(username)
        if userFound:      # the username is found in the database, next prompt for the password to try to login
            pwAttempts = 0    
            while pwAttempts < 3: 
                pw = getpass.getpass('Password: ')
                pwAttempts += 1
                
                if FindPassword(username, pw):
                    # if Admin, enter the Admin Console
                    # one Admin is setup in MySQL manually by changing the default value of 0 (false) to 1 (true)
                    if user[8] == 1:  # if the user is admin (the 8th value in the user field), go to the admin console
                        AdminConsole()
                        
                    # if a just a user, enter the chatroom
                    else:
                        os.system('cls')
                        print("Hlub Chatroom welcomes you!\n\n")
                        # show the list of users currently in the chatroom
                        _ = input('Press Enter to continue ...')
                    
                    # go back to the Welcome menu for now
                    Welcome()
                else:  # wrong password
                    print('  Wrong password!  Press try again ...')
            else:                       
                print('Good-bye!  Too many password attempts.')
                _ = input('Press Enter to continue ...')
                Welcome()     
        else:  # username is not found
            print('  Wrong username!  Please try again ...')
    else:
        print('Good-bye!  Too many username attempts.')
        _ = input('Press Enter to continue ...')
        Welcome()            


# Exiting the application


def Exit():
    print('\nGood-bye!  Please come again.')
    exit()


# Welcome menu 

def Welcome():
    
    # the lists of characters for create, login and exit options
    
    CreateL = ['1', 'create']
    LoginL = ['2', 'login']
    ExitL = ['3', 'exit', 'Exit']
    
    while True:
        # clear the screen
        os.system('cls')
        
        print('Welcome to Hlub Radio\'s chatroom!')
        print('---------------------------------')
        print('1. Create a new account')
        print('2. Login')
        print('3. Exit')     
        print('---------------------------------')
          
        choice = input('Enter your choice --> ')
            
        if choice in CreateL:
            Create()
        elif choice in LoginL:
            Login()
        elif choice in ExitL:
            Exit()
        else:
            _ = input('\nInvalid choice!  Press Enter to try again ...')
            next


# Admin Console, will be called from the Login function


def AdminConsole():
    
    while True:
        os.system('cls')
        print ('Admin Console')
        print('------------------------')
        print('1. Disable\enable a user')
        print('2. Suspend a user')
        print('3. Modify a user details')
        print('4. Delete a user')   
        print('5. Add an admin')
        print('6. Exit')
        print('------------------------')
        choice = input('\nEnter your choice --> ')    

        if choice in ['1', 'disable', 'enable:']:
            DisableEnable()
        elif choice in ['2', 'suspend']:
            Suspend()
        elif choice in ['3', 'modify']:
            ModifyDetails()
        elif choice in ['4', 'delete']:
            Delete()
        elif choice in ['5', 'add', 'admin']:
            AddAdmin()
        elif choice in ['6', 'exit']:  # exit to the Welcome screen
            Welcome()
        else:
            _ = input('Wrong choice!  Please Enter to try again ...')
            

# Disable or enable a user

def DisableEnable():
    print('Disable\\Enable a User\n')


# Suspend a user

def Suspend():
    print('Suspend a User\n')
    
    
# Modify user details    
    
def ModifyDetails():
    print('Modify a User Details\n')


# Delete a user

def Delete():
    print('Delete a User\n')
    
  
# Add an admin by changing a user to admin (not creating a new user as admin which by default is NOT)    
    
def AddAdmin():
    print('Add an Admin\n')

    username = input('Username: ')
    user, _ = FindUsername(username)  # ignore the truth value returned
    
    
################################
# Main 
################################

if __name__ == '__main__':
    Welcome()
    

    
    
           
           