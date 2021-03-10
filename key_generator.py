import os

with open('secret_key.txt', 'w') as file:
    file.write(str(os.urandom(16)))
