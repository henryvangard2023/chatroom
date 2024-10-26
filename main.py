import os
from dataclasses import dataclass
import uuid
import getpass  # for hiding the characters of a password
import hashlib  # for  

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

################################
# User class
################################

@dataclass
class User:
    
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

################################
# Hash the user password before storing it in the database, don't use salt
################################


def HashPassword(pw):
    pwBytes = pw.encode('utf-8')
    hashObj = hashlib.sha256(pwBytes)
    
    pwHash = hashObj.hexdigest()
    return pwHash   # this is the hashed password to be stored in the database
                    # when comparing the password entered by the user against the hashed password from the database
    

################################
# Verify uniqueness of ID 
################################

def VerifyUniqueID(id: int) -> bool: 
    '''
    Verify the uniqueness of ID as provided by the parameters 
    Returns True if the ID is unique
    '''
    
    sql = 'SELECT id from users WHERE id = %s'
    val = (id,)
    mydb.cur.execute(sql, val)
    
    result = mydb.cur.fetchall()
    if len(result) == 0:    # result returned an empty list, id is unique (it has not been used)
        return True 
    else:
        return False        # id has already been used, ask the user to enter a different id


################################
# Verify uniqueness of ID 
################################    

def VerifyUniqueUsername(username: str) -> bool:
    '''
    Verify the uniqueness of Username as provided by the parameters 
    Returns True if the Username is unique
    '''
    
    sql = 'SELECT username from users WHERE username = %s'
    val = (username,)
    mydb.cur.execute(sql, val)
    
    result = mydb.cur.fetchall()
    if len(result) == 0:    # result returned an empty list, username is unique (it has not been used)
        return True 
    else:
        return False        # username has already been used, ask the user to enter a different username
    
    
################################
# Enter the unique ID of the user 
################################

def EnterID() -> int:   # returns the unique ID of the user in number only
        
    while True:         # repeat until an integer is entered for ID
        try:
            id = int(input('ID (must be unique): '))    
            
            if VerifyUniqueID(id):  # the id entered is unique, return it to exit the loop
                return id
            else: # the id has been used, prompt for a new ID
                print(f'\t{id} already exists!')
                next
        except:
            print('Wrong type:  Enter numbers only for the ID!')
      
        
################################
# Enter the username and check for uniqueness
################################

def EnterUsername() -> str:
    
    while True:
        username = input('Enter username: ')
        
        if VerifyUniqueUsername(username) == True:
            return username
        else:
            _ = input('Please enter a unique username!')
    


################################
# Enter the password and check for uniqueness
################################

def EnterPassword() -> str:
    
    while True:
        ...
   
    return pw


################################
# Create a new user
################################

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
    
    pwHash = HashPassword(pw)   # MySQL data type of VARCHAR(64) is being used for sha256 hashes, successful INSERTed in MySQL 
          
    user = User(id, fname, lname, username, pwHash, email)  # here we are storing the user's hash password and not the original password

    # testing
    # print(user)         
    
    # Create the user in the database
    mydb.CreateUser(user)

    _ = input('\nDone!  Press Enter to continue...')
    
    return user


################################
# Log in
################################

def Login():
    print ('Please log in ...\n')
    
    username = input('Username: ')
    pw = getpass.getpass('Password: ')
    
    # 1.  Check to see if the user exists in the database:  SELECT Username from hlubradiochatroom.users where Password='pw'
    #     If cursor.fetchall() returns an empty list then it's not found.
      
    # 2.  If it exists, verify the password.  If it's correct, log the user in.
    
    # 3.  What does it mean to log the user in?  Show the users who are logged in???
    
    # _ is a dummy variable
    _ = input('\nWaiting!  Press Enter to continue...')


################################
# Exiting the application
################################

def Exit():
    print ('\nGood-bye!  Please come again.')
    exit()


################################
# Welcome menu 
################################

def Welcome():
    
    # the lists of characters for create, login and exit options
    
    CreateL = ['c','C']
    LoginL = ['l','L']
    ExitL = ['e','E']
    
    while True:
        # clear the screen
        os.system('cls')
        
        print ('Welcome to Hlub Radio\'s chatroom!\n')
        print ('Menu:')
        print ('---------------------------------')
        print ('(C\\c) ... Create a new account')
        print ('(L\\l) ... Log in')
        print ('(E\\e) ... Exit')     
        print ('---------------------------------')
          
        choice = input('Enter your choice --> ')
            
        if choice in CreateL:
            Create()
        elif choice in LoginL:
            Login()
        elif choice in ExitL:
            Exit()
        else:
            _ = input('\nInvalid choice!  Press Enter to try again.')
            next


################################
# Main 
################################

if __name__ == '__main__':
    Welcome()
    

    
    
           
           