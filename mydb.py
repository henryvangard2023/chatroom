import mysql.connector
import os

# user modules
import main

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '2597',
    database = 'hlubradiochatroom'
)

cur = db.cursor()

################################
# Select ALL from the 'users' table
# Status:   Successful!
# Date:     10/9/24
################################
   
def SelectAll():

    cur.execute("SELECT * FROM users")

    AllUsers = cur.fetchall()
    
    for row in AllUsers:
        print (row)


# Create a user

def CreateUser(user):
    
    sql = 'INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    val = (user.ID, user.FirstName, user.LastName, user.Username, user.Password, user.Email, 0,0,0)  # 0 for Disabled, Suspended, and Admin
    
    # testing
    # print(val)
    
    # INSERT INTO users VALUES (user.ID, user.FirstName, user.LastName, user.Username, user.Password, user.Email);
    cur.execute(sql, val)
    
    # Make sure to commit to the database not the cursor
    db.commit()
    
    
# Delete a user

def DeleteUser(user):
    ...


# Modify a user

def ModifyUser(user):
    ...


# How about disabling a user from chatting???

def DisableUser(user):
    '''
    Disable a user by the admin, must add a disable field to the database.
    '''
    
    ...


# Close the database connection

def CloseDB():
    db.close()

    
################################
# Main 
################################

if __name__ == '__main__':
    os.system('cls')
    SelectAll()
    
    # Make sure to you double quotes if there are single quotes inside like in a SQL statement
    
    '''
    cur.execute("INSERT INTO users \
                VALUES (9000, \
                'Tom', \
                'Yang', \
                'tomcat', \
                '1234', \
                'ty@abc.com')" \
                )  
   
   '''
   
    # Make sure to commit to the database not the cursor
    db.commit()
    
    # At the end, close the database connection
    CloseDB()
    