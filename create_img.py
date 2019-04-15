#
# Create an result.png from a text file (default=tuple.txt) containing RGB tuples like (rrr,ggg,bbb) where tuples are in decimal
#
# J. Kirn 4/15/19
#
from __future__ import print_function
import re
import sys, getopt
from PIL import Image

def process(inpath, outpath, W, H):
   # read RGB data tuple into array (https://stackoverflow.com/questions/48094176/read-tuples-from-text-file?rq=1)
   x=0
   tuples = []
   for t in open(inpath).read().split():
      r,g,b = t.strip('()').split(',')
      tuples.append((int(r), int(g), int(b)))
      x+=1
      #print('tuples = {0}' .format(tuples) )
   print('Number of tuples = {0}' .format(x) )

   #
   # -- create image from RGB tuple array
   #
   img = Image.new('RGB', [W, H], 0x000000)  #create blank image

   i_pixel = 0
   x=0
   y=0

   for x in range(W):
     for y in range(H):
         #print('y={0}' .format(x) )
         #print('i_pixel={0}' .format(i_pixel))
         #print('tuples[{0}] = {1}' .format(i_pixel, tuples[i_pixel]) )
         img.putpixel((x, y), tuples[i_pixel])  # insert pixel(s) into image
         i_pixel += 1

   img.save(outpath)

def main(argv):
   # Default input and output file, can be overwritten by -i and -o options
   inpath = 'tuple.txt'    # input file
   outpath = 'result.png'  # output file
   # image size (0-478) for test image, future can make this an input
   W = 21
   H = 21

   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('create_img.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('create_img.py -i <inputfile> -o <outputfile>')
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
   process(inpath,outpath,W,H)
   print('Done!')

if __name__ == "__main__":
   main(sys.argv[1:])
