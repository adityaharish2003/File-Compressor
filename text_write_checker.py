import numpy as np
a = np.random.randint(255,size = 310000)
b = []
with open('trial.txt','wb') as test:
    test.write(bytes(a))

with open('trial.txt','rb') as test:
    byte = test.read(1)
    
    while(len(byte)>0):
        b.append(ord(byte))
        byte = test.read(1)