import uuid 
import hashlib



def shift_string(s):
    return ''.join(chr(ord(c) + 4) for c in s)


def generate_key():
    return uuid.uuid4()


def hashed(st : str):
    return hashlib.sha256(st.encode()).hexdigest()

