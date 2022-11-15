"""
Adapted from https://github.com/Sven-Bo/streamlit-sales-dashboard-with-userauthentication
Thanks to Sven-Bo
"""

import pickle
import os

import streamlit_authenticator as stauth

names = ["Arno", "Carole"]
usernames = ["arno", "carole"]
passwords = ["CaroleArno", "CaroleArno"]

hashed_passwords = stauth.Hasher(passwords).generate()
print(hashed_passwords)


config = f"""
credentials:
  usernames:
    jsmith:
      email: jsmith@gmail.com
      name: John Smith
      password: 123 # To be replaced with hashed password
    rbriggs:
      email: rbriggs@gmail.com
      name: Rebecca Briggs
      password: 456 # To be replaced with hashed password
cookie:
  expiry_days: 30
  key: some_signature_key
  name: some_cookie_name
preauthorized:
  emails:
  - melsby@gmail.com
  """


def create_user_pass_str(username, email, name, hash_pass):
    user_pass_str = (
        f"    {username}:"
        f"      email: {email}"
        f"      name: {name}"
        f"      password: {hash_pass}"
    )
    return user_pass_str

