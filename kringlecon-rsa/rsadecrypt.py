from Crypto.Hash import SHA
from base64 import b64decode
import binascii
import hashlib

# Get the possible key from the memory dump using power_dump.py
# Use the process from Video: Analyzing PowerShell Malware/Chris Davis
#  https://www.youtube.com/watch?v=wd12XRq2DNk&t=677s
# Place the results into file possible_key.txt (should be a single line of 512 characters)
fd = open("possible_key.txt", "r")
pub_key_encrypted_key = fd.read()
fd.close()
print ('Public Key Encrypted Key: {0}' .format(pub_key_encrypted_key) )

raw_encrypted_key = binascii.unhexlify(pub_key_encrypted_key)

# Get the Private RSA key
rsa_key = RSA.importKey(open('server.key', "rb").read())
cipher = PKCS1_OAEP.new(rsa_key)

decrypted_key = cipher.decrypt(raw_encrypted_key)
hex_key = binascii.hexlify(decrypted_key)

# Check the SHA1 hash
sha1_target = "b0e59a5e0f00968856f22cff2d6226697535da5b"
sha1_result = hashlib.sha1(hex_key).hexdigest()

if (sha1_result == sha1_target):
   print ('Found the key! - {0}' .format(hex_key) )
else:
   print ("Key SHA1 hash doesn't match...")
   print ('Target:{0} - Ours:{1}' .format(sha1_target,sha1_result) )
