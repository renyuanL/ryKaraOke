#import mcpi.minecraft as minecraft
#import mcpi.block     as block

from mcpi.minecraft import *
from mcpi.block     import *

import server
import sys

mc= Minecraft()
mc.postToChat("Hello, I'm Renyuan. 仁園です !!!!")

p= 位置= Vec3(0,0,0)
d= 方向= Vec3(1,0,0) # 向東
mc.player.setPos(p)
mc.player.setDirection(d)

'''
pL= [(0,0,0), (1,0,0), (0,1,0), (0,0,1)]
for n,p in enumerate(pL):
    mc.setBlock(Vec3(p), n)
'''
    
mc.setBlock(Vec3((0,0,0)), GOLD_BLOCK)


for n in range(1,11):
    mc.setBlock(Vec3((n,0,0)), 1)
for n in range(1,11):
    mc.setBlock(Vec3((0,n,0)), 2)
for n in range(1,11):
    mc.setBlock(Vec3((0,0,n)), 3)

pos= mc.player.getPos(); 
d= mc.player.getDirection();
mc.setBlocks(pos+d*10,pos+d*10+Vec3(10,10,10), GOLD_BLOCK)

from ryMic import *

ry麥= Ry麥類()
ry麥.start()

 