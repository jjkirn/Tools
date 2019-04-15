#
# Converts ASCII encoded binary file of 1s an 0s to raw binary file
#
# JJK 4/13/19
#
from __future__ import print_function
import binascii
import struct
import sys, getopt


def process(inpath, outpath):

   fo = open (outpath,"wb")  # open the outfile for write binary

   temp = ""
   mycnt = 0
   flag = True
   # loop through the input file character by character
   with open(inpath,"r") as fi:
      while flag:  # loop through file till EOF
         for i in range (0,8): # loop through 8 binary digits
            # Process a character at a time
            c = fi.read(1)
            if not c:
               print ('End of file')
               flag = False
               break  # exit for-loop if EOF

            if c  == '\r' or c == '\n':
               # print ('Either a cr or lf')
               continue  # skip end of line chars

            if c == '0' or c == '1':   # make sure input data is a '0' or a '1'
                mycnt +=1
            else:                      # else exit program with error
               print ('***Bad Data in file - exiting***')
               print ('char = {0}' .format(c) )
               flag = False
               break  # exit for-loop if "Bad data"

            temp += temp.join(c)  # join the 8 binary digits togther

         if not flag:  # exit for loop if EOF or "Bad Data"
            break

         # print (hex(int(temp,2)))  # show the 8 binary digits as hex(ascii)
         var  =  struct.pack("B",int(temp,2))  #convert binary digits to raw binary
         # print (var)  # show raw binary
         barray = bytearray(var)  # put raw binary into bytearry for writing to outfile
         fo.write(barray)  # write raw binary to outfile
         temp = ""  # clear temp for next pass

   print ('Characters processed = {0}, bytes processed = {1}' .format(mycnt,mycnt/8) )
   fo.close  # close all files
   fi.close

def main(argv):
   # Default input and output file, can be overwritten by -i and -o options
   inpath = 'binary.txt'   # input file, generated by tweet_exten.py
   outpath = 'out.bin'     # output file

   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('bincvt2.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('bincvt2.py -i <inputfile> -o <outputfile>')
         sys.exit()

      elif opt in ("-i", "--ifile"):
         try:
            inpath = arg
            with open(inpath) as file:
               file.close
               pass
         except IOError as e:
            print('Input file [{0}] does not exist or can not be read!' .format(arg) )
            sys.exit()

      elif opt in ("-o", "--ofile"):
         outpath = arg
   print ('Input file is {0}' .format(inpath) )
   print ('Output file is {0}' .format(outpath) )
   process(inpath,outpath)
   print('Done!')

if __name__ == "__main__":
   main(sys.argv[1:])
