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
    strength = round(length * math.log2(pool_size), 2) #standard formula for calculating the password strength
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


def command_line():
    while True:
        first_line = input('input "s" to test the strength of the password or enter "l" to check if your password has been leaked ')

        if first_line.lower() == "s":
            input_password1 = input("Please Enter A Password ")
            print(f"Your Password Strength Is {password_strength(input_password1, calculate_pool_size(input_password1))}")
        elif first_line.lower() == "l":
            input_password2 = input("Please Enter A Password ")
            breach_count = pwned_api(input_password2)
            if breach_count == 0:
                print("Good News! This Password Has Not Been Found In Known Data Breaches")
            else:
                print(f"Warning! This Password Has Been Found in {breach_count:,} Data Breaches")
        else:
            print('Please Enter etiher a "s" or a "l" ')
            continue

        while True:
            again = input('If You Would Like To Run This Program Again, Enter "Y", Otherwise Enter "N" ')
            if again.lower() == "y":
                break
            elif again.lower() == "n":
                return None
            else:
                print("Please Enter A Suitable Answer")

command_line()