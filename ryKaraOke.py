# -*- coding: utf-8 -*-
"""
ryKaraOkeFollowScoring001.py
放 wav 檔，
跟唱，
show pitch
evaluation

ry3語ASR_tk.py

純文字模式展現，
再轉回 TK，文字區 比較單純。

除了 3語， 基頻及音高音符 也一並展出。

Created on Mon Aug  8 21:31:03 2016

@author: renyu
"""

import time
import threading

from tkinter import *
from tkinter.scrolledtext import *

import numpy as np


######################################################
#from ryMic002_wavFile   import *
#from ryMic003_deque   import *
from ryMic  import *

ry麥= Ry麥類()
ry麥.start()
time.sleep(1)

######################################################
from rySpecgram import *

ry頻譜= Ry頻譜類(ry麥)
ry頻譜.start()

time.sleep(1)
######################################################

from ryASR import *

ry辨= Ry辨類(ry麥) # 16 == 1 秒
麥=   ry麥         #ry辨.麥

#"""

from visual import *
l= label()

b0= sphere(make_trail= True, retain= 100, material= materials.earth, opacity= .5, radius= .5)
xaxis= arrow(axis= vector(1,0,0), color= color.red)
yaxis= arrow(axis= vector(0,1,0), color= color.green)
zaxis= arrow(axis= vector(0,0,1), color= color.blue)

#scene.center=   b0.pos


畫面x軸寬= 1024 #512
i框在x軸循環= 麥.i框%畫面x軸寬

def th0F():
    global i框在x軸循環 #, l_zhTW, l_ja, l_en
    
    麥.等待第一圈錄音圓滿()
    vx= 8 #16 # 音符球在x軸上的速度。
    while True:

        i框= 麥.i框


        
        
        i框在x軸循環= (i框 *vx) % 畫面x軸寬
        
        b0.pos= vector(i框在x軸循環, 0, 0)
        
        
        xaxis.pos= yaxis.pos= zaxis.pos= b0.pos
        
        #scene.center=   b0.pos
        l.pos=          b0.pos + vector(0,-10,0)
        
        l.text= '''i框= {}'''.format(i框)

       
        while 麥.i框 - i框 <1: pass # 在此等待，同步專用
        
        rate(1000)

th0= threading.Thread(target= th0F)
th0.start()

b4= sphere(make_trail= True, retain=32, 
        color= color.yellow, trail_type= 'points') #'curve')#'points')

b4.trail_object.size=   10
#b4.trail_object.radius=   2

l4= label(color= color.yellow)

#from ryF0Estimate000 import freq_from_autocorr, pitchQuantization, noteNameL #(sig, fs)
from ryPitch import freq_from_autocorr, pitchQuantization, noteNameL #(sig, fs)

def th4F():
    global noteName
    
    #麥.等待第一圈錄音圓滿()
    麥.等待第一圈錄音圓滿_wav()
      
    while True: 

        i框= 麥.wav_i框
        

        f0, noteName= ry辨.wav基頻,  ry辨.wav音符
        
        f0 = f0*2 # 在圖上比較好看，只為畫圖！
               
        b4.pos= vector(i框在x軸循環, f0, 0)
               
        l4.pos= vector(i框在x軸循環, f0, +20)
        l4.text= '{}'.format(noteName)
       
        while 麥.wav_i框 - i框 <1: pass
        
        rate(1000)

th4= threading.Thread(target= th4F)
th4.start()



b401= sphere(make_trail= True, retain=32, 
        color= color.white, trail_type= 'points')

b401.trail_object.size=   10

l401= label(color= color.white)
l402= label(color= color.cyan)

音符評分=       0 
音符及格評分= .5
累計音符評分=  0
譜線高度= 440*2


def th401F():
    global noteName, 譜線高度
    
    麥.等待第一圈錄音圓滿()
      
    while True:
    

        i框= 麥.i框
        

        f0, noteName= ry辨.基頻,  ry辨.音符
        
        f0 = f0*2 # 在圖上比較好看，只為畫圖！
               
        b401.pos= vector(i框在x軸循環, f0, 0)
               
        l401.pos= vector(i框在x軸循環, f0, -20) #-30, 0)
        l401.text= '{}'.format(noteName)
        
        if 音符評分> 音符及格評分:
            b401.color= color.cyan
            b401.trail_object.color= color.cyan
            b401.trail_object.size= 15
        else:
            b401.color= color.white
            b401.trail_object.color= color.white
            b401.trail_object.size= 5
        
        l402.text= '評分= ({:.2f}), ({:.2f})'.format(音符評分, 累計音符評分)
        l402.pos= vector(0, 累計音符評分*100%譜線高度, 0)
        while 麥.i框 - i框 <1: pass
        
        rate(1000)

th401= threading.Thread(target= th401F)
th401.start()


#譜線高度= 440*2

def 畫幾條水平線當作音高參考():
        global 譜線高度

        # 畫 幾條水平線 當作音高參考，
        # 要知道 pitch in semitone (S) 
        # 以及 pitch in Hz (H)之對數關係。
        # 大概是 S= log2(H), 細節要再查一下，
        #
        # S= log2(H/440) * 12
        # H= 440 時， S=   0 == 'note_A'，鋼琴中間附近的 'la'
        # H= 880 時， S=  12 == 'note_a'，高八度的 'la'
        # H= 220 時， S= -12 == 'note_A,'，低八度的 'la'
        #
        # 然後用 色相 = 0 .... 1 均勻分配 12 平均律 的 每個 semitone
        #
        
        #for yy in np.linspace(Z0,50,10):
        
        Z0= 0

        #譜線高度= 440*2 #512
        八度之數= 4   #440,220,110,55
        譜線刻度= Z0 + 譜線高度*np.logspace(-八度之數, 0, num=12*八度之數, base=2) 
        
        #np.ceil(譜線刻度*10)
        '''
        array([  55.        ,   58.36671628,   61.93951945,   65.7310247 ,
         69.75461945,   74.02451059,   78.55577469,   83.36441116,
         88.4673988 ,   93.88275575,   99.62960307,  105.72823229,
        112.20017704,  119.06828909,  126.35681905,  134.09150196,
        142.2996482 ,  151.01023989,  160.25403322,  170.0636671 ,
        180.47377832,  191.52112393,  203.24471095,  215.68593419,
        228.88872231,  242.89969301,  257.76831758,  273.54709562,
        290.29174037,  308.06137545,  326.91874361,  346.93042829,
        368.16708869,  390.70370928,  414.61986456,  440.        ])
        '''
        
        for nn, yy in enumerate(譜線刻度):

            譜線= curve(pos= [(Z0 ,yy, 0), (Z0+畫面x軸寬,yy,0)])
            譜線.color= color.hsv_to_rgb((nn%12/12,1,1))
        
        #
        # 再畫幾條垂直線，當作時間線。用灰色畫就好，比較不會喧賓奪主。
        #
        縱線數= 16
        橫線刻度= np.linspace(0, 畫面x軸寬, 縱線數+1)
        
        for nn,xx in enumerate(橫線刻度): #range(畫面x軸寬):
                縱線= curve(pos= [(xx , 0+Z0, 0), (xx, 譜線高度+Z0,0)])
                灰色= vector(1,1,1)*(1-(nn%4)/4)
                縱線.color= 灰色   
        
        scene.center= vector(畫面x軸寬//2, 譜線高度//2, 0)
        
        scene.autoscale= False
 

畫幾條水平線當作音高參考()


#"""


#
# 以下開始簡單的文字區 GUI，開4個【捲式】文字區。
#

#音符評分= 0 
#音符及格評分= .5

tk= Tk()

tk.grid_rowconfigure(   1,weight=1)
tk.grid_columnconfigure(0,weight=1)
tk.grid_columnconfigure(1,weight=1)

st0= ScrolledText(tk)
st1= ScrolledText(tk)

#st2= ScrolledText(tk)
#st3= ScrolledText(tk)

st0.grid(row= 1, column=0) # 左邊，for teacher
st1.grid(row= 1, column=1) # 右邊，for student

#st2.grid(row= 1, column=0)
#st3.grid(row= 1, column=1)

lb0= Label(tk, text= 'Teacher')
lb1= Label(tk, text= 'Student')
lb0.grid(row= 0, column=0) # 左邊，for teacher
lb1.grid(row= 0, column=1) # 右邊，for student



#
# 示範函式，特別是 st.insert(), st.delete(), st.get()
#
def thF(st= st0, dt= .1):
    i= 0
    t= 0
    #dt= .1    
    T= 100
    
    while t<T:
        文= '{:08.2f},'.format(t)
        #print('st= {}, 文= {}'.format(st,文))
        st.insert('1.0', 文)
        
        t += dt
        i += 1
        time.sleep(dt)
        
        st.delete('1.16','2.0')
    
'''    
th0= threading.Thread(target= thF, kwargs={'st':st0, 'dt': .05})
th1= threading.Thread(target= thF, kwargs={'st':st1, 'dt': .1})
th2= threading.Thread(target= thF, kwargs={'st':st2, 'dt': .2})
th3= threading.Thread(target= thF, kwargs={'st':st3, 'dt': .3})


th0.start()
th1.start()
th2.start()
th3.start()
'''

#
# 音符線程
#

from ryPitch import pitchQuantization2midiNum


import difflib  # 這是 評分 的關鍵模組


評分段落預留長度= 10
音符評分段落=     []
wav音符評分段落=  []

#累計音符評分=     0


abc音符典= {
    0: 'A_',
    1: 'A#',
    2: 'B_',
    3: 'C_',
    4: 'C#',
    5: 'D_',
    6: 'D#',
    7: 'E_',
    8: 'F_',
    9: 'F#',
    10:'G_',
    11:'G#',
    12:'..'
}

def thF音符():
    global 音符評分段落,  音符評分, 累計音符評分
    
    sm=    difflib.SequenceMatcher()
    音符評分= 0
    音符評分段落= []
    累計音符評分= 0
    
    i= 0
    t= 0
    dt= .1    
    T= 100
    
    while ry辨.基頻音符們 == []: pass # 等到開始有辨認結果才開始以下
    
    前文= ''
    前時= 0    
    while True: #t<T:

        時, f0, qf0, 音符= ry辨.基頻音符們[-1]
        #print('st= {}, 文= {}'.format(st,文))
        
        if qf0 != 0:
            semi_tone= int(round(np.log2(qf0/440)*12))%12
        else:
            semi_tone= 12
        

        
        #
        # 音符評分，
        # 以下為重要的參考，
        # 應該是做 Dynamic programming,
        # 除了整體分數之外還有 replace, insert, delete 之訊息。
        # 值得進一步研究，
        # 目前只用匹配的分數，介於 0 ~ 1
        #
        """
        import difflib
        sm=    difflib.SequenceMatcher()

        x= [69, 70, 71, 72]
        y= [69, 70, 80, 71, 72]

        sm.set_seqs(x,y)

        r= sm.ratio()
        qr= sm.quick_ratio()
        mb= sm.get_matching_blocks()
        op= sm.get_opcodes()
        r,qr,mb, op
        '''
        r == 0.8888888888888888,
        qr== 0.8888888888888888,
        mb== [Match(a=0, b=0, size=2), 
          Match(a=2, b=3, size=2), 
          Match(a=4, b=5, size=0)],
        op=[('equal', 0, 2, 0, 2), 
          ('insert', 2, 2, 2, 3), 
          ('equal', 2, 4, 3, 5)])
        '''
        """        
        
        
        
        if 音符=='': 音符='..'
        
        音符= '{}, '.format(abc音符典[semi_tone])
        
        if (時 != 前時):
  
            st= st1 # 右邊
            
            音符評分段落 += [semi_tone]
            while len(音符評分段落) > 評分段落預留長度:
                音符評分段落.pop(0)
                
            if i%評分段落預留長度==0: 
                音符 += '\n[{}:{}]'.format(i,時)
            
            if i%評分段落預留長度==0:
            
                x= wav音符評分段落.copy()
                y= 音符評分段落.copy()
            
                #音符 += '\nwav音符評分段落= {}\n'.format(x)
            
                #音符 += '\n音符評分段落= {}\n'.format(y) 
                
                
                sm.set_seqs(x, y)
                
                音符評分= r= sm.ratio()
                
                if 音符評分 < 音符及格評分: 音符評分= 0
                #
                # 若是 semi_tone == 12 (代表 無音符)太多，
                # 此種 音符評分也算無效
                #
                if y.count(12) > 音符及格評分*評分段落預留長度: 音符評分= 0
                    
                
                累計音符評分 += 音符評分
                           
                音符 += ' >>> 評分= ({:.2f}), ({:4.2f})\n'.format(音符評分, 累計音符評分)
            
             
                
            st.insert('end', 音符)
            st.see('end')
            
            #msg= '[{}], f0= {:04.1f}, qf0= {:04d}, {}\n'.format(時, f0, qf0, 音符)
            #st.insert('10.0', msg)
            #st.delete('30.0','end')
            
            #
            # 清道夫
            #
            '''
            if i%500==0: 
                N= len(st.get('1.0','end'))
                st.delete('1.0','1.{}'.format(N//2))
            '''

            i += 1
        
        t += dt
        time.sleep(dt)
        
        前時= 時

th音符= threading.Thread(target= thF音符)
th音符.start()

#
# 音符線程
#

#wav音符評分段落=[]



def thF_wav音符():
    global wav音符評分段落 
    
    
    i= 0
    t= 0
    dt= .1    
    T= 100
    
    while ry辨.wav基頻音符們 == []: pass # 等到開始有辨認結果才開始以下
    
    wav音符評分段落= []
    #評分段落預留長度= 100
    
    
    前文= ''
    前時= 0    
    while True: #t<T:

        時, f0, qf0, 音符= ry辨.wav基頻音符們[-1]
        #print('st= {}, 文= {}'.format(st,文))
        
        if qf0 != 0:
            semi_tone= int(round(np.log2(qf0/440)*12))%12
        else:
            semi_tone= 12
        

        
        if 音符=='': 音符='..'
        
        
        
        
        
        if (時 != 前時):
  
            st= st0 # 左邊
            
            
            wav音符評分段落 += [semi_tone]
            while len(wav音符評分段落) > 評分段落預留長度:
                wav音符評分段落.pop(0)  

            
            音符= '{}, '.format(abc音符典[semi_tone])
            
            
            
            
            
            

            if i%10==0: 音符 += '\n[{}:{}]\n'.format(i,時)
            
            #if i%100==0: 音符 += '\nwav音符評分段落= {}\n'.format(wav音符評分段落) 
                
            st.insert('end', 音符)
            st.see('end')
            
            #msg= '[{}], f0= {:04.1f}, qf0= {:04d}, {}\n'.format(時, f0, qf0, 音符)
            #st.insert('10.0', msg)
            #st.delete('30.0','end')
            
            #
            # 清道夫
            #
            '''
            if i%500==0: 
                N= len(st.get('1.0','end'))
                st.delete('1.0','1.{}'.format(N//2))
            '''

            i += 1
        
        t += dt
        time.sleep(dt)
        
        前時= 時

th_wav音符= threading.Thread(target= thF_wav音符)
th_wav音符.start()







#######################################################
#
# tk 程式的末端，一進去就出不來了！
#
tk.mainloop()



