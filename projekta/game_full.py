#Kaatman Bird
#Revised 2019-01-11 16:28
# -*- coding: utf-8 -*-

from psychopy import visual, event, core
import multiprocessing as mp
import pygame as pg
import pandas as pd
import filterlib as flt
import blink as blk
from pyOpenBCI import OpenBCIGanglion

def blinks_detector(quit_program, blink_det, blinks_num, blink,):
    def detect_blinks(sample):
        if SYMULACJA_SYGNALU:
            smp_flted = sample
        else:
            smp = sample.channels_data[0]
            smp_flted = frt.filterIIR(smp, 0)
        #print(smp_flted)

        brt.blink_detect(smp_flted, -38000)
        if brt.new_blink:
            if brt.blinks_num == 1:
                #connected.set()
                print('CONNECTED. Speller starts detecting blinks.')
            else:
                blink_det.put(brt.blinks_num)
                blinks_num.value = brt.blinks_num
                blink.value = 1

        if quit_program.is_set():
            if not SYMULACJA_SYGNALU:
                print('Disconnect signal sent...')
                board.stop_stream()


####################################################
    SYMULACJA_SYGNALU = False
####################################################
    mac_adress = 'eb:3a:66:e2:04:06'
####################################################

    clock = pg.time.Clock()
    frt = flt.FltRealTime()
    brt = blk.BlinkRealTime()

    if SYMULACJA_SYGNALU:
        df = pd.read_csv('dane_do_symulacji/data.csv')
        for sample in df['signal']:
            if quit_program.is_set():
                break
            detect_blinks(sample)
            clock.tick(200)
        print('KONIEC SYGNAŁU')
        quit_program.set()
    else:
        board = OpenBCIGanglion(mac=mac_adress)
        board.start_stream(detect_blinks)

if __name__ == "__main__":


    blink_det = mp.Queue()
    blink = mp.Value('i', 0)
    blinks_num = mp.Value('i', 0)
    #connected = mp.Event()
    quit_program = mp.Event()

    proc_blink_det = mp.Process(
        name='proc_',
        target=blinks_detector,
        args=(quit_program, blink_det, blinks_num, blink,)
        )

    # rozpoczęcie podprocesu
    proc_blink_det.start()
    print('subprocess started')

    ############################################
    # Poniżej należy dodać rozwinięcie programu
    ############################################

#############################################haha
import pygame, random, time, sys
print("Karolak Bird")
pygame.init()
clock = pygame.time.Clock()
try:
    pygame.display.set_icon(pygame.image.load("zerotwo.png"))
    bird = pygame.image.load("karolak.png")
    bird_dead = pygame.image.load("karolakdie.png")
except:
    print("yo I can't find the game files")
    print("Exiting...")
    pygame.quit()
    sys.exit()
window = pygame.display.set_mode((720,720))
pygame.font.init()
pygame.display.set_caption('Karolak Bird')
font, font2 = pygame.font.SysFont('Arial', 72), pygame.font.SysFont('Arial', 36)
title = font.render('Karolak Bird', True, (0,0,0), None)
caption = font2.render('Press SPACE to Start', True, (0,0,0), None)
global start, vel, ypos, hscore, p1, p2, tscore, died
start = False
vel = 0
ypos = 300
hscore = 0
pipe = [720,random.randint(0,380)]
tscore = 0
died = False
while True:
    window.fill((120,120,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start == False:
                    ypos = 300
                    start = True
                vel = 7.
    if blink.value == 1:
        print('BLINK!')
        blink.value = 0
        if start == False:
            ypos = 300
            start = True

    if start:
        window.blit(bird,(50,ypos))
        ypos = ypos - vel
        vel = vel - 0.5
        pygame.draw.rect(window,(0,255,0),(pipe[0],0,50,pipe[1]))
        pygame.draw.rect(window,(0,255,0),(pipe[0],pipe[1]+300,50,720))
        window.blit(font2.render('Score: ' + str(tscore), True, (0,0,0), None),(10,10))
        pipe[0] = pipe[0] - 5
        if pipe[0] < -50:
            pipe[0] = 720
            pipe[1] = random.randint(0,380)
            tscore = tscore + 1
            if tscore > hscore:
                hscore = tscore
    else:
        if died:
            window.blit(bird_dead,(100,500))
        window.blit(title,(100,100))
        window.blit(caption,(100,300))
        window.blit(font2.render('High score - ' + str(hscore), True, (0,0,0), None),(100,400))
    if (pipe[0] < 164 and pipe[0] > 14) and (ypos+192 > pipe[1]+300 or ypos < pipe[1]):
        ypos = 528
    if ypos >= 528:
        ypos = 528
        caption = font2.render('You died', True, (0,0,0), None)
        start = False
        tscore = 0
        pipe[0] = 720
        died = True
    elif ypos < 0:
        ypos = 0
        vel = -abs(vel)
    clock.tick(60)
    if time.time() - int(time.time()) < 0.02 and int(time.time()) % 5 == 0:
        print("FPS: " + str(int(clock.get_fps())))
    pygame.display.flip()

############

# Zakończenie podprocesów
    proc_blink_det.join()
