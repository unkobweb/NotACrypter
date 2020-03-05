import hashlib
import sys

def hashMsg(message, algo):
    if algo == 'sha1':
        m = hashlib.sha1()
    elif algo == 'sha256':
        m = hashlib.sha256()
    elif algo == 'sha512':
        m = hashlib.sha512()
    elif algo == 'md5':
        m = hashlib.md5()
    elif algo == 'blake2b':
        m = hashlib.blake2b()
    else:
        return 'L\'algorithme n\'est pas connu par LLSA'
    m.update(message.encode())
    return m.hexdigest()

print(hashMsg(sys.argv[1], sys.argv[2]))