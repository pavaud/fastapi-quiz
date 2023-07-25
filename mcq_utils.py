from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import pandas as pd


users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
}

admins = {
    "admin": "4dm1N"
}


security = HTTPBasic()


def get_user(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Check credentials for user routes
    """
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")

    for user, password in users.items():
        correct_username_bytes = user.encode("utf8")
        correct_password_bytes = password.encode("utf8")
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )

        if (is_correct_username and is_correct_password):  
                return credentials.username

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
    )


def get_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Check credentials for admin routes
    """
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")

    for user, password in admins.items():

        correct_username_bytes = user.encode("utf8")
        correct_password_bytes = password.encode("utf8")
        is_correct_username = secrets.compare_digest(
            current_username_bytes, correct_username_bytes
        )
        is_correct_password = secrets.compare_digest(
            current_password_bytes, correct_password_bytes
        )

        if (is_correct_username and is_correct_password):  
                return credentials.username

    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
    )

def get_uses():
    """
    Returns the list of distinct question uses in the database 
    """
    df = pd.read_csv('questions.csv')
    uses = list(df.use.unique())

    return uses

def get_subjects():
    """
    Returns the list of distinct question subjects in the database 
    """
    df = pd.read_csv('questions.csv')
    subjects = list(df.subject.unique())
    
    return subjects


def get_random_mcq(subjects, use, nb):
    """
    Returns a list of questions given a subject, use and number of questions in unordered fashion
    """
    df = pd.read_csv('questions.csv')
    df_mcq = df[(df.subject.isin(subjects)) & (df.use == use)]
    nb_mcq = (len(df_mcq),nb)[len(df_mcq)>nb]

    return df_mcq.sample(nb_mcq)