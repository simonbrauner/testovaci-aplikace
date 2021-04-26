"""
Testovací aplikace
Šimon Brauner
26.4.2021

key_generator.py

Creating a file with secret key
for user account sessions.
"""


import os

with open('secret_key.txt', 'w') as file:
    file.write(str(os.urandom(16)))
