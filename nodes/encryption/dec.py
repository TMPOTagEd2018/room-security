from Crypto.Cipher import AES
import base64
import os
import glob


path = '/Users/dev/Desktop/testfiles/'

for filename in glob.iglob(path + '**/*', recursive=True):
    print(filename)
    # if not os.path.exists(filename):
    #     SystemExit()
    if os.path.isfile(filename) == True:
        file = open(filename, "rb")
        text = file.read()
        print(text)
        def decryption(info):
            PADDING = '{'
            key = 'CE10BDC7BDF43EDE08D8A856AF1DD6B8'
            cipher = AES.new(key)
            plain = cipher.decrypt(base64.b64decode(info))
            return plain.decode().rstrip(PADDING)
        outputText = decryption(text)
        print('Pre output text')
        print(outputText)
        print('Text done')

        file = open(filename, "w+")
        file.write(outputText)
        file.close()
        print('File done')
    
print('Program done')


