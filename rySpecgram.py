'''
rySpecgram.py
2016/08/16

把畫頻譜接到新麥克風上。



ryApp.py

這支程式是我第一次寫出頻譜的作品，
值得紀念，現在跑起來還是覺得很穩。
主要是基於 pygame
2016/07/27

2014/04/20

運用 RyAudio.py 的即時語音頻譜。

This program use many Chinese names
for variables, functions and classes

First presentation
on PyCon APAC 2014

Adapted from the following tasks

================
影音一起處理
================
ryCameraMic01.py
----------------

做了那麼久的 DSP，
這次終於能把視訊與音訊兜在一起。

呂仁園，2014/03/30
'''
#
# This program refered much from the following tutorial program
#
# 1. Basic image capturing and displaying using the camera module
'''
Pygame Tutorials
Camera Module Introduction

by Nirav Patel
nrp@eclecti.cc

Revision 1.0, May 25th, 2009

http://www.pygame.org/docs/tut/camera/CameraIntro.html

http://www.pygame.org/docs/ref/camera.html

'''




import numpy        as np


import colorsys
import time

import threading
import collections
import os

#from ryMic002_wavFile   import *
#from ryMic003_deque   import *

from ryMic   import *
from ryPitch__ import *
from ryLyric import *


#from ryASR              import *



def 頻率轉顏色(頻率, 倍數= 1):

    頻率 *= 倍數
    r, g, b= colorsys.hsv_to_rgb(頻率, 1, .8)
    r = int(r*256)%256
    g = int(g*256)%256
    b = int(b*256)%256
    rgb顏色= (r,g,b)

    return rgb顏色

class Ry頻譜類:



    def __init__(我, 麥= None):



        我.幕寬, 我.幕高= 我.幕寬高= size = (512, 512) #512) #(512, 512) #( 640, 480 )


        if 麥 is None:
            x= Ry辨類()
            我.音= x.麥
        else:
            我.音= 麥
        


        #
        # for specgram, 頻譜， 調色盤，把 頻譜值 對應到顏色。
        #
        我.i譜框= 0
        
        我.譜框數= 我.音.框數 * 8  ## 把譜留在畫面上多一點時間
        我.specgram= np.random.random([我.譜框數, 我.音.每框點數//2])
        
        我.譜寬高= (我.譜框數, 我.音.每框點數//2)    #specgram.shape

        我.深度= 8 # 試過 10, 16 都不行
        
        我.調色盤= []
        for n in range(int(2**我.深度)):

            k= n/2**我.深度
            色= 頻率轉顏色(k)

            我.調色盤 += [色]
            
        
        我.主迴圈執行中=  False
        
        我.頻譜線= threading.Thread(target= 我.頻譜線程)
        
        
        我.時間點歌詞= dict()
        我.時間點們= []
        
        if LrcToki != {}:
            我.時間點歌詞= LrcToki
            我.時間點們= sorted(list(我.時間點歌詞.keys()))
        


    
    def 頻譜線程(我):
        

        import  pygame  as pg
        
        # 把 import pygame 放在線程之內，用線程跑時，pygame display 才會正常運作 (GUI部分)

        ###############################
        做成譜的音框數= 2
        ham= np.hamming(做成譜的音框數 * 我.音.每框點數) #len(x))
        
        clk= pg.time.Clock()
        
        pg.font.init()        
        
        #aFont= pg.font.SysFont('Times', 20)
        
        中文字型路徑= '{}{}'.format( os.environ['SYSTEMROOT'], 
                            '\\Fonts\\mingliu.ttc')
        aFont= pg.font.Font(中文字型路徑, 20)
        
        pitchMatching= 0
        
        aLyric= bLyric= cLyric= ''
        iLyric= 0
        
        wav_i框_0, wav_i框_1, wav_i框_2= 0,0,0
        曾來過= False
        
        if 我.時間點歌詞!={}:
            wav_i框_0= wav_i框_1= wav_i框_2= list(我.時間點歌詞.keys())[0]
            
        def 取音訊且顯示頻譜於幕(我, 鍵盤= None):
            nonlocal pitchMatching, aLyric, bLyric, cLyric, iLyric
            nonlocal wav_i框_0, wav_i框_1, wav_i框_2, 曾來過

            #做成譜的音框數= 2
            # 這是 mic
            #b0= 我.音.框們[-做成譜的音框數:]  
            # 連取 2音框，做成1譜框，譜看起來會更平滑吧
            #b0= b''.join(b0)
            
            #
            # 但 .框們 現在是一個 deque, 不能 用 x1:x2
            # 因此 簡單的改成如下
            #
            b0= b''
            for k in range(-做成譜的音框數,0):
                b0 += 我.音.框們[k]

            
            
            
            x0= np.fromstring(b0,'int16')
            
            
            
                   
            # 這是 wav 檔
            #b= 我.音.wav框們[-做成譜的音框數:]  
            # 連取 2音框，做成1譜框，譜看起來會更平滑吧       
            #b= b''.join(b)
            
            b1= b''
            for k in range(-做成譜的音框數,0):
                b1 += 我.音.wav框們[k]

            
            x1= np.fromstring(b1,'int16')
                
            # mic + wav 檔
            x= x1 + x0
            
            # 以下轉頻譜
            
            x= x * ham  #np.hamming(len(x)) # 拿出去，改善速度
            
            xFFT= np.fft.fft(x)[0:我.音.每框點數//2] # 這時，僅剩 Fs/4 的頻率範圍了，解析度更高了吧。
            
            xP=   np.absolute(xFFT*xFFT.conj())
            
            #我.i譜框= 我.音.i框  # 框同步
            
            我.specgram[我.i譜框%我.譜框數]= xP
            
            我.i譜框 += 1
            
            頻譜= 我.specgram #.copy()

            #
            # up_down flip, 頻譜上下對調，讓低頻在下，高頻在上，比較符合直覺。
            #
            頻譜= 頻譜[:,-1::-1]

            #
            # 這個 頻譜 大小要如何自動調整才能恰當的呈現在螢幕上，還有待研究一下。
            #
            頻譜= (np.log(頻譜)+10)*10

            
            
       
            
            
            
            #
            # 錦上添花
            #
            # 加這行讓頻譜會轉，有趣！！
            #
            if 鍵盤 == pg.K_e:
                頻譜= np.roll(頻譜, -int(我.i譜框 % 我.譜框數), axis=0)
                
                x= (我.譜框數-1)  * 我.幕寬 / 我.譜框數
                h= 我.幕高
                pg.draw.line(我.幕, pg.Color('white'),(x,h),(x,0) , 10)
                

                pg.display.update()


            #
            # pygame 的 主要貢獻:  頻譜 ---> 音幕
            #
            pg.surfarray.blit_array(我.音幕, 頻譜.astype('int'))

            #
            # pygame 的 次要貢獻: 調整一下 我.譜寬高 音幕 ---> aSurf
            #
            aSurf= pg.transform.scale(我.音幕, (我.幕寬, 我.幕高)) #//4))

            #
            # 黏上幕  aSurf ---> display
            #

            #aSurf= pg.transform.average_surfaces([aSurf, 我.攝影畫面])
            我.幕.blit(aSurf, (0,0))


            
            #
            # 江永進的建議，在頻譜前畫一條白線，並把能量、頻率軌跡畫出。
            #
            
            if 鍵盤 != pg.K_e:
                x= (我.i譜框 % 我.譜框數)  * 我.幕寬 / 我.譜框數
            else:
                x= (我.譜框數-1)  * 我.幕寬 / 我.譜框數
                
            h= 我.幕高
            w= 我.幕寬
            pg.draw.line(我.幕, pg.Color('gray'),(x,h),(x,0) , 10)
            

            # 把 f0 放在這裡。
            f0= freq_from_autocorr(x0, 我.音.每框點數) #我.麥.取樣率)
            f1= freq_from_autocorr(x1, 我.音.每框點數) #我.麥.取樣率)
            
            pitchHit= False
            if (f0/f1 < 1.06 and f0/f1 > 1/1.06):       pitchMatching += 1; pitchHit= True
            elif (f0/2/f1 < 1.06 and f0/2/f1 > 1/1.06): pitchMatching += 1; pitchHit= True
            elif (f0/4/f1 < 1.06 and f0/4/f1 > 1/1.06): pitchMatching += 1; pitchHit= True
            elif (f0*2/f1 < 1.06 and f0*2/f1 > 1/1.06): pitchMatching += 1; pitchHit= True
            else: pass
            
            pitchScore_y= (h - pitchMatching)%h  # for y axis
            pitchScore_x= ((pitchMatching//h+1)*10) % w # for x axis
            
            pg.draw.rect(我.幕, pg.Color('blue'),[(pitchScore_x, pitchScore_y),(60,20)])
            #pg.draw.line(我.幕, pg.Color('blue'),(0, pitchScore_y),(pitchScore_x, pitchScore_y), 2)
            pg.draw.line(我.幕, pg.Color('blue'),(0, h),(0, pitchScore_y), pitchScore_x*2) #2)
            
            aText= aFont.render('{}'.format(pitchMatching), True, (255,255,255))
            我.幕.blit(aText, (pitchScore_x, pitchScore_y))
            
            # 把 f0 放在這裡。
            #x= (我.i譜框 % 我.譜框數)  * 我.幕寬 / 我.譜框數
            #h= 我.幕高
            f0 *= 16 # f0 先放大16倍，
            f1 *= 16
            f0_h= h - f0
            f1_h= h - f1
            我.fQ += [(f0_h, f1_h)] 
            
            while len(我.fQ)>32: 我.fQ.popleft()     # 保持 16 框就好
            
            for n in range(len(我.fQ)):
                x00= x+ (n-len(我.fQ)) *8 #*16 # 橫軸 放大 16 倍
                y00= 我.fQ[n][0]
                y01= 我.fQ[n][1]
                pg.draw.ellipse(我.幕, pg.Color('white'), [(x00, y00), (10,10)])
                pg.draw.ellipse(我.幕, pg.Color('black'), [(x00, y01), (10,10)])
                if (n==len(我.fQ)-1) and (pitchHit == True):
                    pg.draw.ellipse(我.幕, pg.Color('blue'), [(x00, y01), (20,20)], 10)
                    pg.draw.rect(我.幕, pg.Color('blue'),[(x00, y01),(60,20)])                    
                    我.幕.blit(aText, ((x00, y01)))
                
            
            #aLyric= '.wav_i框= {:10d}, aLyric......, '.format(我.音.wav_i框)#i譜框) # wav_i框
            '''
            if 鍵盤 == pg.K_UP:
                iLyric -= 1
                iLyric = iLyric%len(LyricToki)
                aLyric= LyricToki[iLyric-2]
                bLyric= LyricToki[iLyric-1]
                cLyric= LyricToki[iLyric]
                
            elif 鍵盤 == pg.K_DOWN:
                iLyric += 1
                iLyric = iLyric%len(LyricToki)
                aLyric= LyricToki[iLyric-2]
                bLyric= LyricToki[iLyric-1]
                cLyric= LyricToki[iLyric]
            '''
           
            if (    我.時間點歌詞 != {} ):
                #iLyric= (iLyric+1)%len(我.時間點歌詞)
                
                if (    我.音.wav_i框<我.時間點們[(iLyric+1)%len(我.時間點歌詞)] 
                    and 我.音.wav_i框>=我.時間點們[(iLyric)%len(我.時間點歌詞)]
                    and 曾來過 == False
                    ): #我.音.wav_i框 in 我.時間點們: #我.時間點歌詞.keys():

                    #wav_i框_2= wav_i框_1
                    #wav_i框_1= wav_i框_0
                    #wav_i框_0= 我.時間點們[iLyric] #我.音.wav_i框
                    
                    aLyric= 我.時間點歌詞[我.時間點們[(iLyric-1)%len(我.時間點歌詞)]]
                    bLyric= 我.時間點歌詞[我.時間點們[(iLyric)%len(我.時間點歌詞)]]
                    cLyric= 我.時間點歌詞[我.時間點們[(iLyric+1)%len(我.時間點歌詞)]]
                    
                    #iLyric += 1
                    iLyric= (iLyric+1)%len(我.時間點歌詞)
                    曾來過= True
                    
                    #cLyric= '' #我.時間點歌詞[wav_i框_0] # 這個 「下一句」 有點麻煩！！！ 
                    
                    # 這個 「下一句」 有點麻煩！！！
                    '''
                    iLyric= (我.時間點們.index(wav_i框_0)+1)%len(我.時間點們)
                    
                    wav_i框_plus1= 我.時間點們[iLyric]
                    cLyric= 我.時間點歌詞[wav_i框_plus1]
                    
                    '''
                if ( 我.音.wav_i框>=我.時間點們[iLyric]):
                    #iLyric += 1
                    曾來過= False
                    

            aText= aFont.render('[{}], {}'.format(iLyric-2, aLyric), True,   pg.Color('gray'))
            bText= aFont.render('[{}], {}'.format(iLyric-1, bLyric), True,   pg.Color('yellow'))
            cText= aFont.render('[{}], {}'.format(iLyric,   cLyric), True,   pg.Color('gray'))
            
            textPosX= 30
            textPosY= 30
            pg.draw.rect(我.幕, pg.Color('black'),[(textPosX,textPosY),(我.幕寬-textPosX*2,20)]) 
            我.幕.blit(aText, (textPosX, textPosY))
            pg.draw.rect(我.幕, pg.Color('black'),[(textPosX,textPosY+30),(我.幕寬-textPosX*2,20)]) 
            我.幕.blit(bText, (textPosX, textPosY+30))
            pg.draw.rect(我.幕, pg.Color('black'),[(textPosX,textPosY+60),(我.幕寬-textPosX*2,20)]) 
            我.幕.blit(cText, (textPosX, textPosY+60))    
                
            pg.display.update()

           
        def 滑鼠游標顯示(我, 滑鼠x, 滑鼠y, 鍵盤= None):

            大小=         10 #max(10, 音訊能量 )
            位置及大小=  (滑鼠x - 大小/2, 滑鼠y - 大小/2, 大小, 大小)

 
            色=      (255, 255, 255) #頻率轉顏色(頻率)

            pg.draw.ellipse(我.幕, 色, 位置及大小)
            pg.display.update()

        ###############################

        #'''
        pg.init()

        我.幕= pg.display.set_mode( 我.幕寬高, 0 )
        pg.display.set_caption('rySpecgram.py, using RyMic, on PyCon JP 2016, by Renyuan Lyu')
        
        我.音幕= pg.Surface( 我.譜寬高, depth= 我.深度) # for specgram

        我.音幕.set_palette(我.調色盤)
        #'''
        我.fQ= collections.deque()
        
        print('頻譜主迴圈....')

        滑鼠按著=      False
        滑鼠x= 滑鼠y=  0
        鍵盤=          None

        i歌詞時間點們= []
        i歌詞= 0

        我.音.等待第一圈錄音圓滿_wav()
        我.音.等待第一圈錄音圓滿()
        
        我.主迴圈執行中=  True

        while 我.主迴圈執行中:
            
            i框= 我.音.wav_i框
            if i框==0:
                print('{}'.format(i歌詞時間點們))
                
                xL= i歌詞時間點們
                yL= sorted(xL, key= lambda xL: xL[2])
                yD= dict([(x1,x3) for (x0, x1, x2,x3) in yL])
                
                print('{}'.format(yD))
                
                #我.時間點歌詞= yD
                
                
                i歌詞= 0
                i歌詞時間點們= []
                iLyric= 0
                曾來過= False
            
            #
            # 取得 使用者 輸入 事件
            #
            事件群= pg.event.get()

            #
            # 處理 使用者 輸入 事件
            #
            for e in 事件群:
                #
                # 首先 優先處理 如何結束，優雅的結束！
                #
                # 用滑鼠點擊 X (在 視窗 右上角) 結束！
                #
                if e.type in [pg.QUIT]:
                    我.主迴圈執行中= False
                    pg.quit()
                    break
                #
                # 用鍵盤 按 Esc (在 鍵盤 左上角) 結束！
                #
                elif e.type in [pg.KEYDOWN]:
                    鍵盤= e.key
                    if e.key in [pg.K_ESCAPE]:
                        我.主迴圈執行中= False
                        pg.quit()
                        break
                    
                    
                    elif e.key in [pg.K_SPACE]:
                        
                        pass
                    
                    elif e.key in [pg.K_UP, pg.K_DOWN]:
                        
                        if e.key == pg.K_UP:
                            iLyric -= 1
                        elif e.key == pg.K_DOWN:
                            iLyric += 1
                            
                        iLyric = iLyric%len(LyricToki)
                        
                        aLyric= LyricToki[iLyric-2]
                        bLyric= LyricToki[iLyric-1] # 記住中間這個
                        cLyric= LyricToki[iLyric]   
                        
                        i歌詞時間點= 我.音.wav_i框
                        a歌詞=     bLyric           # 記住中間這個 (黃色那個)
                        a歌詞編號= iLyric-1
                        
                        a歌詞資訊= (i歌詞, i歌詞時間點, a歌詞編號, a歌詞)
                        
                        i歌詞時間點們 += [a歌詞資訊]
                        
                        i歌詞 += 1
                        
                        print('a歌詞資訊= {}'.format(a歌詞資訊))
                        
                        
                        
                        
                        
                        
                        pass
                        
                    else:
                        pass
                        
                elif e.type in [pg.KEYUP]:
                    鍵盤= None
                #
                # 以下 3 個 if , 用來 處理 滑鼠
                #
                elif e.type in [pg.MOUSEBUTTONDOWN]:
                    滑鼠按著= True
                    滑鼠x, 滑鼠y= x,y= e.pos

                elif e.type in [pg.MOUSEBUTTONUP]:
                    滑鼠按著= False
                    滑鼠x, 滑鼠y= x,y= e.pos

                elif e.type in [pg.MOUSEMOTION]:
                    if (滑鼠按著 is True):
                        滑鼠x, 滑鼠y= x,y= e.pos
                else:
                    pass


            if 我.主迴圈執行中 == False:
                break
            #
            # 音訊
            #
            取音訊且顯示頻譜於幕(我, 鍵盤) # 用 K_efgh 來控制音訊處理

            #
            # 滑鼠
            #
            if (滑鼠按著 is True):  # 用 K_ijk 來控制滑鼠處理
                滑鼠游標顯示(我, 滑鼠x, 滑鼠y, 鍵盤) 
            #
            # 畫面更新
            #
            pg.display.flip()
            
            while (我.音.wav_i框 - i框 == 0 ): pass # .wav_i框 會在 ryMic reset 成 0
            
            #clk.tick(10) # 類似 vpython 之 rate
            
        #
        # 跳出主迴圈了
        #
        print('我.主迴圈執行中= ', 我.主迴圈執行中)
        #我.攝影機.stop()
        #我.音.結束()
        
        #我.音.stop()
        
        pg.quit()
        
    
    
    def start(我):
            
        我.頻譜線.start() # 用 thread 執行時，關不掉！！(quit 不了)

if __name__ == '__main__':

    
    麥= Ry麥類()
    麥.start()
    
    頻譜= Ry頻譜類(麥)
    頻譜.start()
    
    
    
    