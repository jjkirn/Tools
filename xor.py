#
# XOR Encrypt/Decrypy
#
#
# J.Kirn 4/25/19

from itertools import izip, cycle
import base64
import sys, getopt

def xor_crypt_string(data, key):

    if key == '':
	    return ('error')
    xored = ''.join(chr(ord(c)^ord(k)) for c,k in izip(data, cycle(key)))
    return xored

def main(argv):

    epath = 'encode.txt'   # 
    dpath = 'decode.txt'   # 
    kpath = 'key.txt'      #
    encode = True
    decode = True
    encode_data = 'XOR procedure'
    decode_data = 'OTg3Ux8fChMEFwYFCg=='
    key_data ='awesomepassword'

    try:
        opts, args = getopt.getopt(argv,"he:d:k:",["efile=","dfile=","keyfile="])
    except getopt.GetoptError:
        print ('xor.py -e <data file to encode> -d <data file to decode > -k <key file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('xor.py -e <data file to encode> -d <data file to decode > -k <key file>')
            sys.exit()

        elif opt in ("-e", "--efile"):  #get data to encode
            try:
                epath = arg
                print('option -e selected {0}' .format(epath) )
                with open(epath) as file:
		    encode_data = file.read()
                    print('encode_data = {0}'.format(encode_data) )
                    file.close
                    pass
            except IOError as e:
                print('Encode file [{0}] does not exist or can not be read!' .format(arg) )
                sys.exit()

        elif opt in ("-d", "--dfile"):   #get data to decode       
	    try:
                dpath = arg
                print('option -d selected {0}' .format(dpath) )
                with open(dpath) as file:
		    decode_data = file.read()
                    print('decode_data = {0}'.format(decode_data) )
                    file.close
                    pass
            except IOError as e:
                print('Decode file [{0}] does not exist or can not be read!' .format(arg) )
                sys.exit()
		 
        elif opt in ("-k", "--kfile"):   #get key       
	    try:
                dpath = arg
                print('option -k selected {0}' .format(dpath) )
                with open(kpath) as file:
		    key_data = file.read()
                    print('key_data = {0}'.format(key_data) )
                    file.close
                    pass
            except IOError as e:
                print('Key file [{0}] does not exist or can not be read!' .format(arg) )
                sys.exit()

    print ('Encode data file is [{0}]' .format(epath) )
    print ('Decode file is [{0}]' .format(dpath) )
    print ('Key file is [{0}]' .format(kpath) )
    
    print("The cipher text is:")
    print('encode_data=[{0}], key_data=[{1}]' .format( encode_data, key_data) )
    cyphered = xor_crypt_string(encode_data, key_data)
    b64e = base64.b64encode(cyphered)
    decode_data = b64e
    print('B64encoded cyphered = [{0}]' .format(b64e) )

    print('-------------------------------------------------------------------')

    print("The plain text fetched:")
    print('decode_data = [{0}], key_data = [{1}]' .format( decode_data, key_data) )
    b64d = base64.b64decode(decode_data)
    message = xor_crypt_string(b64d, key_data)
    print('Message = [{0}]' .format(message) )
    print('Done!')


if __name__ == "__main__":
    main(sys.argv[1:])
