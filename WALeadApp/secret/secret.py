"""
https://stackoverflow.com/questions/7014953/i-need-to-securely-store-a-username-and-password-in-python-what-are-my-options
"""

from getpass import getpass
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
import os
import base64
import pickle
# try:
#     from config import DB_PATH
# except ModuleNotFoundError:
#     pass


### Settings ###
db= None
passphrase = None
saltSeed = 'jehzts572wef4gwtkd' # MAKE THIS YOUR OWN RANDOM STRING
PASSPHRASE_FILE = './WALeadApp/secret/secret.p'
SECRETSDB_FILE = './WALeadApp/secret/secrets'
PASSPHRASE_SIZE = 64 # 512-bit passphrase
KEY_SIZE = 32 # 256-bit key
BLOCK_SIZE = 16  # 16-bit blocks
IV_SIZE = 16 # 128-bits to initialise
SALT_SIZE = 8 # 64-bits of salt


### System Functions ###

def getSaltForKey(key):
    return PBKDF2(key, saltSeed).read(SALT_SIZE) # Salt is generated as the hash of the key with it's own salt acting like a seed value

def encrypt(plaintext, salt):
    ''' Pad plaintext, then encrypt it with a new, randomly initialised cipher. Will not preserve trailing whitespace in plaintext!'''
    global passphrase
    # Initialise Cipher Randomly
    initVector = os.urandom(IV_SIZE)

    # Prepare cipher key:
    key = PBKDF2(passphrase, salt).read(KEY_SIZE)

    cipher = AES.new(key, AES.MODE_CBC, initVector) # Create cipher
    text = plaintext + ' '*(BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE))
    return initVector + cipher.encrypt(text.encode('utf-8')) # Pad and encrypt

def decrypt(ciphertext, salt):
    ''' Reconstruct the cipher object and decrypt. Will not preserve trailing whitespace in the retrieved value!'''
    global passphrase
    # Prepare cipher key:
    key = PBKDF2(passphrase, salt).read(KEY_SIZE)

    # Extract IV:
    initVector = ciphertext[:IV_SIZE]
    ciphertext = ciphertext[IV_SIZE:]

    cipher = AES.new(key, AES.MODE_CBC, initVector) # Reconstruct cipher (IV isn't needed for edecryption so is set to zeros)

    # return cipher.decrypt(ciphertext).rstrip(' ') # Decrypt and depad
    return cipher.decrypt(ciphertext).decode('utf-8').rstrip(' ') # Decrypt and depad


### User Functions ###

def store(key, value):
    ''' Sore key-value pair safely and save to disk.'''
    global db
    # value = value.encode('utf-8')
    if key in db:
        del db[key]
    db[key] = encrypt(value, getSaltForKey(key))
    with open(SECRETSDB_FILE, 'wb') as f:
        pickle.dump(db, f)

def retrieve(key):
    ''' Fetch key-value pair.'''
    return decrypt(db[key], getSaltForKey(key))

def require(key, passw):
    '''ini di comment/dihapus saat production'''
    ''' Test if key is stored, if not, prompt the user for it while hiding their input from shoulder-surfers.'''
    if not key in db: 
        # store(key, getpass('Please enter a value for "%s":' % key))
        store(key,passw)
def update(key,new_passw):
    if key in db:
        passw = retrieve(key)
        # old_passw = getpass('Please enter previous password for "%s":' % key)
        # new_passw = getpass('Please enter new password for "%s":' % key)
        # confirm = getpass('Confirm new password for "%s":' % key)
        store(key,new_passw)
def check(key):
    if not key in db: 
        return False
    return True
    

### Setup ###

def secret():
    global passphrase
    """
    mode :
        - get : get password 
        - update : update password
    """
    # Aquire passphrase:
    try:
        with open(PASSPHRASE_FILE,'rb') as f:
            passphrase = f.read()
        if len(passphrase) == 0: raise IOError
    except IOError:
        with open(PASSPHRASE_FILE, 'wb') as f:
            passphrase = os.urandom(PASSPHRASE_SIZE) # Random passphrase
            f.write(base64.b64encode(passphrase))

            try: os.remove(SECRETSDB_FILE) # If the passphrase has to be regenerated, then the old secrets file is irretrievable and should be removed
            except: pass
    else:
        passphrase = base64.b64decode(passphrase) # Decode if loaded from already extant file
def query(key,mode='select',*args):
    """
    args : passwd_saved, new_passwd, confirm_passwd
    """
    global db
    # Load or create secrets database:
    try:
        with open(SECRETSDB_FILE,'rb') as f:
            db = pickle.load(f)
        if db == {}: raise IOError
    except (IOError, EOFError):
        db = {}
        with open(SECRETSDB_FILE, 'wb') as f:
            pickle.dump(db, f)

    if mode == 'update':
        update(key,*args)
    elif mode== 'set':
        require(key, *args)
    
    return retrieve(key)

    ### Test (put your code here) ###
    # require('admin')
    # # update('admin')
    # for key in db:
    #     print(key, retrieve(key)) # decode values on demand to avoid exposing the whole database in memory
    # retrieve('coba')
    #     # DO STUFF
# secret()
# query('admin',mode='set')
# for key in db:
#     print(key, retrieve(key)) # decode values on demand to avoid exposing the whole database in memory



