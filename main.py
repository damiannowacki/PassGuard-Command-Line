import string
import math
import hashlib
import requests


lowercase_letters = string.ascii_lowercase
uppercase_letters = string.ascii_uppercase
intergers = string.digits
special_characters = string.punctuation


def calculate_pool_size(password):
    has_lowercase = False
    has_uppercase = False
    has_int = False
    has_spec_char = False

    for letter in password:
        if letter in lowercase_letters:
            has_lowercase = True
        elif letter in uppercase_letters:
            has_uppercase = True
        elif letter in intergers:
            has_int = True
        elif letter in special_characters:
            has_spec_char = True

    pool_size = 0 #total combo of characters, e.g 26 letters of the lowercase alphabet, so the pool size of all lowercase letters is 26

    if has_lowercase:
        pool_size += 26
    if has_uppercase:
        pool_size += 26
    if has_int:
        pool_size += 10
    if has_spec_char:
        pool_size += 32

    return pool_size


def password_strength(password, pool_size):
    if pool_size == 0:
        print("Please Enter A Suitable Password")
        return 0
    
    length = len(password)
    strength = round(length * math.log2(pool_size), 2) #standard formula for calculating the password strength, not my original formula
    return strength


def hash_password(password): #i used external research for this function along with pwned_api
    password_bytes = password.encode('utf-8')
    sha1_hash = hashlib.sha1(password_bytes)
    return sha1_hash.hexdigest().upper()


def pwned_api(password):
    hashed_pass = hash_password(password)
    prefix = hashed_pass[:5] #sends only the first 5 letters of the password, the rest is secure
    suffix = hashed_pass[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    hashes = response.text.splitlines()

    for line in hashes: #all the breached passwords from the first 5 letters, goes through all of those and sees is any match the full password (done locally, so more secure)
        returned_suffix, count = line.split(":")

        if returned_suffix == suffix:
            return int(count) 
    return 0

def crack_time_estimator(strength):
    if strength > 100: #above a strength of 100 the result would be a lot of centuries, so i figured 100 is a good cap to keep the command line clean
        return "z"
    
    crack_time_seconds = (2 ** (strength - 1)) / 100_000_000_000 #standard formula for calculating cracktime, not my original formula

    crack_time_minutes = crack_time_seconds / 60
    crack_time_hours = crack_time_seconds / 3600
    crack_time_days = crack_time_seconds / 86400
    crack_time_weeks = crack_time_seconds / 604_800
    crack_time_months = crack_time_seconds / 2_629_746 #average because different months have different amount of days in them, therefore different amount of seconds
    crack_time_years = crack_time_seconds / 31_557_600
    crack_time_decades = crack_time_seconds / 315_569_520
    crack_time_centuries = crack_time_seconds / 3_153_600_000

    if crack_time_centuries > 1:
        return f"{int(crack_time_centuries)} Centuries"
    elif crack_time_decades > 1:
        return f"{int(crack_time_decades)} Decades"
    elif crack_time_years > 1:
        return f"{int(crack_time_years)} Years"
    elif crack_time_months > 1:
        return f"{int(crack_time_months)} Months"
    elif crack_time_weeks > 1:
        return f"{int(crack_time_weeks)} Weeks"
    elif crack_time_days > 1:
        return f"{int(crack_time_days)} Days"
    elif crack_time_hours > 1:
        return f"{int(crack_time_hours)} Hours"
    elif crack_time_minutes > 1:
        return f"{int(crack_time_minutes)} Minutes"
    elif crack_time_seconds > 1:
        return f"{int(crack_time_seconds)} Seconds"
    else:
        return "0 Seconds"
    

def command_line(): #the command line interface you interact with (no gui)
    while True:
        first_line = input('enter "s" to test the strength of the password, enter "c" to find out the time it would take to crack your password, or enter "l" to check if your password has been leaked ')

        if first_line.lower() == "s":
            input_password1 = input("Please Enter A Password ")
            print(f"Your Password Strength Is {password_strength(input_password1, calculate_pool_size(input_password1))}")

        elif first_line.lower() == "c":
            input_password2 = input("Please Enter A Password ")
            pass_strength = password_strength(input_password2, calculate_pool_size(input_password2))
            crack_time = crack_time_estimator(pass_strength)
        
            if crack_time == "z":
                print("Damn. That Password Is Almost Uncrackable, In Fact It Would Take Over 1 Trillion Centuries To Crack!")
            else:
                print(f"It Would Take {crack_time} To Crack Your Password")

        elif first_line.lower() == "l":
            input_password3 = input("Please Enter A Password ")
            breach_count = pwned_api(input_password3)
            if breach_count == 0:
                print("Good News! This Password Has Not Been Found In Known Data Breaches")
            else:
                print(f"Warning! This Password Has Been Found in {breach_count:,} Data Breaches")

        else:
            print('Please Enter etiher "s", "c" or "l" ')
            continue

        while True:
            again = input('If You Would Like To Run This Program Again, Enter "Y", Otherwise Enter "N" ')
            if again.lower() == "y":
                break
            elif again.lower() == "n":
                return None
            else:
                print("Please Enter A Suitable Answer")

if __name__ == "__main__":
    command_line()


#Coming soon:
#Add a colour-based reply along with the password strength
#Add password recommendations for the user's inputed password
#Check a password for common patterns
#A secure password genrator, customised to the user's requests 