# library imports
from argparse import ArgumentParser
import json
import bcrypt
import hashlib
import binascii
import os

# NOTE: DOES NOT WORK... :(

def encode_method(encode_method):
    if encode_method is 'md5':
        return '1'
    elif encode_method is 'Blowfish':
        return '2a'
    elif encode_method is 'SHA-256':
        return '5'
    elif encode_method is 'SHA-512':
        return '6'


def hash_password(password):
    """Hash a password for storing."""
    encrypt_method = '1'  # passwd format for signifying md5 method
    encrypt_salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')[:8]
    pwdhash = hashlib.pbkdf2_hmac('md5', password.encode('utf-8'),
                                  encrypt_salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return encrypt_method, encrypt_salt.decode('ascii'), pwdhash.decode('ascii')


if __name__ == '__main__':
    # Set up argument parser and options
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    parser.add_argument('filename',  help="supply a filename where the user names and passwords are stored")

    # parse supplied arguments
    args = parser.parse_args()
    filename = args.filename

    # read supplied users file into users dict
    users = {}
    with open(filename) as json_file:
        data = json.load(json_file)
        for user in data['users']:
            users[user['username']] = user['password']

    # generate password and shadow files
    pass_file_name = 'etc_passwd.txt'
    shadow_file_name = 'etc_shadow.txt'
    pass_file = open(pass_file_name, 'w')
    shadow_file = open(shadow_file_name, 'w')
    for user in users:
        method, salt, encrypted_password = hash_password(users[user])
        encrypted_entry = method + salt + encrypted_password
        passwd_entry = "{}:{}:{}:{}:{}:{}:{}\n".format(user, 'x', '45', '1045', 'GECOS', 'directory', 'shell45')
        shadow_entry = "{}:{}:{}:{}:{}:{}:::\n".format(user, encrypted_entry, '14538', '0', '99999', '7')
        pass_file.write(passwd_entry)
        shadow_file.write(shadow_entry)

    pass_file.close()
    shadow_file.close()

    print('DONE')






