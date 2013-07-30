# -*- coding:utf-8 -*-

import pygame
from pygame.locals import *

import datetime
# import time

class Veh():
    '''Veh class, each will print a veh's info
    '''

    def __init__(self, vehtype, speed, acce, lane, weight, space, datetime):
        '''Init object

        A para's expamle:

        vehtype:    1           (int)
        speed:      65          (int)
        acce:       939         (int)
        lane:       1           (int)
        weight:     (790, 770)  (tuple of int)
        space:      2564        (int)
        datetime:               (a standard datetime object)
        '''

        self.vehtype    = vehtype
        self.speed      = speed
        self.acce       = acce
        self.weight     = weight
        self.space      = space
        self.datetime   = datetime

        if lane == 1:
            self.x = 90
            self.y = 720
        else:
            self.x = 960 - 90 - 345
            self.y = -100

        self.color  = (255, 255, 255)

    def BuildString(self):
        '''Build String

        Make strings like this:
        self.str1 = '车型: 2轴车    时间: 2012.7.21 13:04:09'
        self.str2 = '车速: 83 km/h    加速度: 0 mm/s^2'
        self.str3 = '轴重: 800,, 800 kg'
        self.str4 = '轴距: 2423 mm'
        '''

        self.str1 = u'车型: {0}轴车 时间: {1}'.format(self.vehtype, self.datetime.strftime('%Y.%m.%d %H:%M:%S'))
        self.str2 = u'车速: {0} km/h  加速度: {1} mm/s^2'.format(self.speed, self.acce)
        self.str3 = u'轴重: {0}, {1} kg'.format(self.weight[0], self.weight[1])
        self.str4 = u'轴距: {0} mm'.format(self.space)

    def BuildTextSurface(self):
        '''Bulid text surfaces

        Make surfaces like this:
        self.surface1 = fone.render('车型 ... ', True, (255, 255, 255))
        ...
        max of width: 340+
        height: 23

        '''

        # font = pygame.font.Font('MiniJXH.ttf', 20)
        font = pygame.font.SysFont('Microsoft YaHei', 19)

        self.surface1 = font.render(self.str1, True, self.color)
        self.surface2 = font.render(self.str2, True, self.color)
        self.surface3 = font.render(self.str3, True, self.color)
        self.surface4 = font.render(self.str4, True, self.color)
        self.back_surface = pygame.image.load('rect_resize.jpg').convert()

    def Up(self, movespeed, top, screen, time):
        '''Move veh up to top

        Para's explantion:
        movespeed: speed of move, pixel/s, int
        top: the end of move, you just need to tell me the y coord, int
        '''

        time = float(time) / 1000.0 # conver from ms to s
        distance = movespeed * time

        screen.blit(self.back_surface, (self.x - 5, self.y - 4))
        screen.blit(self.surface1, (self.x, self.y))
        screen.blit(self.surface2, (self.x, self.y + 23))
        screen.blit(self.surface3, (self.x, self.y + 23 * 2))
        screen.blit(self.surface4, (self.x, self.y + 23 * 3))

        if self.y < top + 1:
            return 0
        else:
            self.y = self.y - distance
            return 1

    def Down(self, movespeed, bottom, screen, time):
        '''Move veh down to bottom

        Para's explantion:
        movespeed: speed of move, pixel/s, int
        bottom: the end of move, you just need to tell me the y coord, int
        '''

        time = float(time) / 1000.0 # conver from ms to s
        distance = movespeed * time

        screen.blit(self.back_surface, (self.x - 5, self.y - 4))
        screen.blit(self.surface1, (self.x, self.y))
        screen.blit(self.surface2, (self.x, self.y + 23))
        screen.blit(self.surface3, (self.x, self.y + 23 * 2))
        screen.blit(self.surface4, (self.x, self.y + 23 * 3))

        if self.y > bottom - 1:
            return 0
        else:
            self.y = self.y + distance
            return 1