import secrets
import string

def generated_password():
    length = secrets.choice(range(8, 13)) 
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password