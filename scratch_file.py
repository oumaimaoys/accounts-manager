import bcrypt
import datetime as dt


# create the password class and make all of these methods in it 

def generatePassword(name, last_name):
    password = name[0] + last_name + "_" + str(dt.date.today().year)
    return password

password = generatePassword("ouamaima", "ouyassine")
print(password)

def hashPasword(password): #it is supposed to give the same output
    password = password.encode('utf-8')
    hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashedPassword

hashedpassword = hashPasword(password)
print(hashedpassword)

def authenticatePassword(password, hashedpassword):
    # we hash the input password and compare it to the one stored 
    # instead of unhsahsing the stored one and comparing it ot the input
    password = password.encode('utf-8')
    if bcrypt.checkpw(password, hashedpassword):
        return True
    else :
        raise ValueError("You entered the wrong password")
    
print(authenticatePassword(password, hashedpassword))