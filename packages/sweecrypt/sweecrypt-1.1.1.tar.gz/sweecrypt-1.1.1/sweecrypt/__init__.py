__version__ = "1.1.1"
db = {
    'a': '`',
    'b': '-',
    'c': ')',
    'd': '/',
    'e': '?',
    'f': '^',
    'g': '#',
    'h': '!',
    'i': ';', 
    'j': '.',
    'k': '\\',
    'l': '~', 
    'm': '&', 
    'n': '*',
    'o': '(',
    'p': '@', 
    'q': '"',
    'r': '>', 
    's': '<', 
    't': '[', 
    'u': ']', 
    'v': '{',
    'w': '}', 
    'x': '|',
    'y': '+', 
    'z': '_', 
    ' ': ',', 
    ',': ':', 
    '.': '=', 
    '!': 'a', 
    '?': 'b',
    '\n': 'c', 
    "'": 'd', 
    '(': 'e', 
    ')': 'f', 
    '1': 'g', 
    '2': 'h', 
    '3': 'i', 
    '4': 'j',
    '5': 'k',
    '6': 'l', 
    '7': 'm', 
    '8': 'n', 
    '9': 'o', 
    '0': 'p', 
    '-': 'q', 
    '&': 'r', 
    ':': 's', 
    ';': 't', 
    '"': 'u', 
    '\\': 'v',
    '/': 'w'
}

db2 = {v: k for k, v in db.items()}

def encrypt(what, shift=0):
    tempdb = dict(zip(list(db.keys()), list(db.values())[shift:] + list(db.values())[:shift]))
    encoded = ""
    what = what.lower()
    for i in range(len(what)):
        encoded += tempdb.get(what[i], "￼")
    return encoded


def decrypt(what, shift=0):
    if shift !=0:
        shift = shift * -1
    tempdb = dict(zip(list(db2.keys()), list(db2.values())[shift:] + list(db2.values())[:shift]))
    decoded = ""
    for i in range(len(what)):
        decoded += tempdb.get(what[i], "￼")
    return decoded
