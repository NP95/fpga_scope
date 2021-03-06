import numpy as np
import random
from PIL import Image
import sys



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def zoom(im, mag):
    w, h = im.size
    im.resize((w*mag, h*mag)).show()



def lut_ascii_art(im):
    if im.size == (6,8):
        m =  (8*(np.asarray(im) > 0))
        m = np.zeros((6,8))
        
        for y in range(8):
            ln = u""
            for x in range(6):
                m[x,y] = not(1*(im.getpixel((x,y)) > 0))
                if m[x,y] == 0:
                    ln += bcolors.OKBLUE + u"\u2588" + bcolors.ENDC
                else:
                    ln += u"\u2588"
            print ln                
    else:
        print "[ERR] wrong char map size"





def verilog_logic_gen(im, lut_name):
                    
    if im.size == (6,8):
        
        m =  (8*(np.asarray(im) > 0))
        m = np.zeros((6,8))
        
        for y in range(8):
            for x in range(6):
                m[x,y] = not(1*(im.getpixel((x,y)) > 0))
                    
        lut = m.T.astype(int)
        
        logic_str = ""
        for row in range(8):
            for col in range(6):
                if lut[row,col]:
                    logic_str += "    (row == %i && col == %i) ||\n" % (row, col)                

        logic_str = ('(   %s\n' % lut_name)+logic_str[:-4]+'\n)'
        print logic_str
        
    else:
        print "[ERR] wrong char map size"



#####################

## load image
imfile = sys.argv[1]

im = Image.open(imfile).convert("1")
w, h = im.size




import string
char_set = string.digits + string.ascii_uppercase + string.ascii_lowercase + '/' + ' '
lut_addr = 0


print """//
//  CHAR LOGIC
//
module char_logic(char_addr,
                  row,
                  col,
                  on_char
                  );
                                    
input [5:0] char_addr;
input [2:0] row;
input [2:0] col;

output on_char;

assign on_char ="""



for x in range(w/6):
    for y in range(h/8):
        char = im.crop((x*6,y*8, x*6 + 6,y*8 + 8) )
        
        
        #lut_ascii_art(char)
        #zoom(char,32)
        lut_name = '//CHAR: "%s"' % char_set[lut_addr]
        if lut_addr > 0:
            print "||"
        
        print "(char_addr == %i) &" % lut_addr
        verilog_logic_gen(char, lut_name)
        lut_addr += 1
        
        
print ";"
print "endmodule"
























