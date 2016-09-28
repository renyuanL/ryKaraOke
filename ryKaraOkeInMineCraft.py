'''
#
# ryKaraOkeInMineCraft.py
#
'''

#
# Code by Alexander Pruss and under the MIT license
#

from mine import *
from math import *
import time
import os

from ryMic import *
ry麥= Ry麥類()
ry麥.start()
ry麥.等待第一圈錄音圓滿()
ry麥.等待第一圈錄音圓滿_wav()



from ryPitch__  import *

def getF0():
    
    b0= b''
    b1= b''
    for k in range(-2,0):
        b0 += ry麥.框們[k]
        b1 += ry麥.wav框們[k]
    
    x0= np.fromstring(b0,'int16')
    x1= np.fromstring(b1,'int16')
    
    
    # 把 f0 放在這裡。
    f0= freq_from_autocorr(x0,  ry麥.取樣率)#.每框點數) #我.麥.取樣率)
    f1= freq_from_autocorr(x1,  ry麥.取樣率)#.每框點數) #我.麥.取樣率)
    
    en0= abs(x0).mean()
    en1= abs(x1).mean()
    
    
    
    x0聲音夠大= False
    x1聲音夠大= False
    if en0 > ry麥.初框['mean']    + ry麥.初框['std']*3:    x0聲音夠大= True
    if en1 > ry麥.wav初框['mean'] + ry麥.wav初框['std']*3: x1聲音夠大= True
    
    if x0聲音夠大==False: f0=1.0
    if x1聲音夠大==False: f1=1.5 # 避開2倍 那會當作正確
    
    return f0/10, f1/10


mc =  Minecraft()


t=0
dt= 1 #1/16
T= 100

mc.player.setPos(0, 100, 0)
mc.player.setDirection(0, 0, 1)

pos0= pos= mc.player.getPos()

posL= []
while True:
   
   f0, f1= getF0()
   print('f0, f1= {:.0f} {:.0f}'.format(f0,f1))
   
   pos.x += -(t%100 -50)
   pos.z += 50
   
   pos.y += f1 #f0 #pos.y - 1

   
   posL += [pos]
   for pos in posL:
       mc.setBlock(pos, block.GOLD_BLOCK)
   
   if len(posL) > 16:
       p0= posL.pop(0)
       if p0 not in posL:
           mc.setBlock(p0, block.AIR)
   #time.sleep(dt)
   t += dt
