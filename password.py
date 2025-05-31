from random import randint
from random import shuffle,choice
import string

alp=string.ascii_lowercase
alphebert=list(alp)
#alphebert=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
spe=string.punctuation
special_char=list(spe)
#special_char=['!','?','#','@','&','*','$','%','=','+','-','(',')']


def get_content(total_length:int, numaric:bool,special_char:bool): 
    '''enter password length as integer and requirment of numaric and special charactor as boolean. 
    this return number of alphabatic,numaric and special charactors in turple'''
    if numaric:
        actual_number_of_numaric_char=randint(1,round(total_length/4))
    else:
        actual_number_of_numaric_char=0
    if special_char:
        actual_number_of_special_char=randint(1,round(total_length/4))
    else:
        actual_number_of_special_char=0
    actual_number_of_alphabatic_char=total_length-actual_number_of_numaric_char-actual_number_of_special_char
    return (actual_number_of_alphabatic_char,actual_number_of_numaric_char,actual_number_of_special_char)

def generate_password(length:int,numaric:bool,special:bool):
    '''enter password length as integer and requirment of numaric and special charactor as boolean
    this method return a string which content the password'''
    content=get_content(length,numaric,special)
    password=[]
    for i in range (0,content[0],1):
        alp=choice(alphebert)
        option= choice([True,False])
        if option:
            alp=alp.upper()
        else:
            alp=alp
          
        password.append(alp)
    for i in range (0,content[1],1):
        num=randint(0,9)
        password.append(num)
    for i in range (0,content[2],1):
        special=choice(special_char)
        password.append(special)
        shuffle(password)
    # adding from password list to a single string
    password_string=''
    for i in password:
        password_string+=str(i)
    return password_string
