
import secrets
import random
import string

def generate_password(password_length): #autogenerates credentials
    password = []
    character_list_alpha = string.ascii_letters
    character_list_num = string.digits
    character_list_punc = string.punctuation
    
    character_list = character_list_alpha + character_list_num + character_list_punc
    """
    while(len(password) != password_length):
        if random.random() < 1/4 :
            password.append(secrets.choice(character_list_num))
        if random.random() < 1/4:
            password.append(secrets.choice(character_list_punc))
        if random.random() < 1/2 :
            password.append(secrets.choice(character_list_alpha))
    """
    for i in range(password_length):
        password.append(secrets.choice(character_list))
    return ''.join(password)


print(generate_password(20))