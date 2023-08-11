from cryptography.fernet import Fernet

def generate_key(file_path):
    key = Fernet.generate_key()
    with open(file_path, 'wb') as key_file:
        key_file.write(key)

    return key

generate_key('encryption_key.key')
