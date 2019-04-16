#!/usr/bin/env python
# reference https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256

#
#  This was from the KringleCon 2018 
# (https://www.holidayhackchallenge.com/2018/winners/esnet_hhc18/)
#
from Crypto.Cipher import AES  # need to do an "easy_install pycrypto" after installing VCForPython27.msi
import binascii
import struct

hex_key = "fbcfc121915d99cc20a3d3d5d84f8308"  # This came from rsadecrypt.py
key = binascii.unhexlify(hex_key)  # same as passphrase

with open("alabaster_passwords.elfdb.wannacookie", 'rb') as f:
    # Get IV (initialization-vector) length & IV for the encrypted file      
    # $FileSW.Write([System.BitConverter]::GetBytes($AESP.IV.Length), 0, 4) - this was how it was encrypted (32 bytes)
    iv_length = struct.unpack('i', f.read(4))[0]

    # Next - get the actual IV
    # $FileSW.Write($AESP.IV, 0, $AESP.IV.Length) - this was how it was encrypted
    iv = f.read(iv_length)

    rest = f.read()  # This is the ciphertext

    # create a new AES object
    aes = AES.new(key, AES.MODE_CBC, iv)

    result = open("alabaster_passwords.elfdb", 'wb')
    result.write(aes.decrypt(rest))
    result.close()

print('File should now be decrypted!'
