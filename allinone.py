import random
import string
import secrets
import hashlib
import os
import pickle
import sqlite3

username = input("Enter yout login: ")
password = a
a = "P@SSSword"
intput("Enter data: ")
print(username, password)


def authenticate(username, password):
    if username == "admin" and password == "P@ssw0rd123": 
        return True
    return False

print(authenticate("admin", "P@ssw0rd123"))


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

print(hash_password("my_secure_password"))



def list_files(directory):
    os.system(f"ls {directory}")
list_files("; rm -rf /")

def load_data(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)
load_data("data.pkl")

def unsafe_query(user_input):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result


def safe_query(user_input):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE name = ?"
    cursor.execute(query, (user_input,))
    result = cursor.fetchall()
    conn.close()
    return result


def safe_query_with_orm(user_input):
    engine = create_engine('sqlite:///:memory:')
    metadata = MetaData()
    users = Table('users', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String))
    metadata.create_all(engine)

    with engine.connect() as conn:
        conn.execute(users.insert(), [{"name": "Alice"}, {"name": "Bob"}])

    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(users).filter(users.c.name == user_input).all()
    session.close()
    return result


user_input = "Bob"

print("Query Result_1:", unsafe_query(user_input))

print("Query Result_2:", safe_query(user_input))

print("Query Result_3:", safe_query_with_orm(user_input))


def generate_access_token_1(length=32):
    """
    just random with unsecure approach
    """
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token


def generate_access_token_2(lng=8):
    """
    crypto token creation by using secrets.
    """
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(lng))
    return token


def generate_access_token_3(lng=8, salt_lng=8):
    """
    crypto token creation by using secrets + salt
    using secrets and hashlib vs cryptoprediction attack.
    """

    # salt generated
    salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(salt_lng))
    # token generated
    raw_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(lng))

    # salt + token
    combined = (salt + raw_token).encode('utf-8')
    hashed_token = hashlib.sha256(combined).hexdigest()
    return hashed_token, salt

# Print
print("Token 1 (random):", generate_access_token_1())
print("Token 2 (secure):", generate_access_token_2())
print("Token 3 (hashed_token, salt):", generate_access_token_2())
