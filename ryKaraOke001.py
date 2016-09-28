# -*- coding: utf-8 -*-
"""
ryKaraOke001.py 

純文字模式展現 ==> tk
2D 繪圖 ==> Pygame


@author: renyu
"""

import time
import threading

from tkinter import *
from tkinter.scrolledtext import *

import numpy as np


######################################################
from ryMic  import *

ry麥= Ry麥類()
ry麥.start()

######################################################
from rySpecgram import *

ry頻譜= Ry頻譜類(ry麥)
ry頻譜.start()

######################################################

#from ryASR import *
from ryPitch import *

ry音高= Ry音高類(ry麥) # 16 == 1 秒
######################################################


#
# 以下開始簡單的文字區 GUI，開4個【捲式】文字區。
#

tk= Tk()

tk.grid_rowconfigure(   1,weight=1)
tk.grid_columnconfigure(0,weight=1)
tk.grid_columnconfigure(1,weight=1)


lb0= Label(tk, text= 'Teacher, 教師, 先生')
lb1= Label(tk, text= 'Student, 學生, 生徒')
lb0.grid(row= 0, column=0) # 左邊，for teacher
lb1.grid(row= 0, column=1) # 右邊，for student


st0= ScrolledText(tk)
st1= ScrolledText(tk)
st0.grid(row= 1, column=0) # 左邊，for teacher
st1.grid(row= 1, column=1) # 右邊，for student


#st2= ScrolledText(tk)
#st3= ScrolledText(tk)

#st2.grid(row= 1, column=0)
#st3.grid(row= 1, column=1)




#
# 音符線程
#

from ryPitch import * #pitchQuantization2midiNum


import difflib  # 這是 評分 的關鍵模組


音符評分= 0 
音符及格評分= .5
累計音符評分= 0

評分段落預留長度= 10
音符評分段落=     []
wav音符評分段落=  []


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
    
    while ry音高.基頻音符們 == []: pass # 等到開始有辨認結果才開始以下
    
    前文= ''
    前時= 0    
    while True: #t<T:

        時, f0, qf0, 音符= ry音高.基頻音符們[-1]
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
    
    while ry音高.wav基頻音符們 == []: pass # 等到開始有辨認結果才開始以下
    
    wav音符評分段落= []
    #評分段落預留長度= 100
    
    
    前文= ''
    前時= 0    
    while True: #t<T:

        時, f0, qf0, 音符= ry音高.wav基頻音符們[-1]
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
