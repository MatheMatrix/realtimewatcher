# -*- coding: utf-8 -*- 

import pygame
from pygame.locals import *

import wx
from Veh import *
from VehReceiveThread import *

class VehFrame(wx.Frame):
    """Build Veh Frame

    import pygame to make animation
    """

    def __init__(self, parent, id, stat):
        wx.Frame.__init__(self, parent, id, u'车速车载实时监控', size = (960, 720), style = wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.ChangeStat = stat
        stat('Veh')
        # pygame.display.init()
        pygame.init()

        self.vehreceive = VehReceiveThread()
        self.vehreceive.start()

        self.display()

    def GetVeh(self):
        '''Get new Veh
        '''
        if len(self.vehreceive.data) >= 1:
            self.newveh = self.vehreceive.data[0]
            del self.vehreceive.data[0]
        else:
            return [0]

        temp = [1]
        temp.extend(self.newveh)

        return temp

    def display(self):
        '''display
        '''
    
        screen = pygame.display.set_mode((960, 720), HWSURFACE | DOUBLEBUF, 32)
        pygame.display.set_caption(u'车速车载实时图像'.encode('utf-8'))
        background = pygame.image.load("road_shot_resize.jpg").convert()
        screen.blit(background, (0, 0))

        clock = pygame.time.Clock() 

        vehs1 = []
        vehs2 = []  

        while True: 

            screen.blit(background, (0, 0)) 

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    self.Close(True)

            ctime = clock.tick(100)

            # 检测有无新车辆
            newveh = self.GetVeh()

            if newveh[0] == 0:
                pass
            elif newveh[4] == 1:
                vehs1.append(Veh(newveh[1], newveh[2], newveh[3], newveh[4], newveh[5], newveh[6], newveh[7]))
                vehs1[-1].BuildString()
                vehs1[-1].BuildTextSurface()
            else:
                vehs2.append(Veh(newveh[1], newveh[2], newveh[3], newveh[4], newveh[5], newveh[6], newveh[7]))
                vehs2[-1].BuildString()
                vehs2[-1].BuildTextSurface()    

            if len(vehs1) == 5:
                vehs1[0].Up(400, -100, screen, ctime)
                del vehs1[0]
            else:
                pass    

            if len(vehs1) > 0:
                vehs1[0].Up(400, 60, screen, ctime) 

            if len(vehs1) > 1:
                vehs1[1].Up(400, vehs1[0].y + 102 + 30, screen, ctime)  

            if len(vehs1) > 2:
                vehs1[2].Up(400, vehs1[1].y + 102 + 30, screen, ctime)  

            if len(vehs1) > 3:
                vehs1[3].Up(400, vehs1[2].y + 102 + 30, screen, ctime)  
    

            if len(vehs2) == 5:
                vehs2[0].Down(400, 820, screen, ctime)
                del vehs2[0]
            else:
                pass    

            if len(vehs2) > 0:
                vehs2[0].Down(400, 720 - 60 - 102, screen, ctime)   

            if len(vehs2) > 1:
                vehs2[1].Down(400, vehs2[0].y - 102 - 30, screen, ctime)    

            if len(vehs2) > 2:
                vehs2[2].Down(400, vehs2[1].y - 102 - 30, screen, ctime)    

            if len(vehs2) > 3:
                vehs2[3].Down(400, vehs2[2].y - 102 - 30, screen, ctime)    

            pygame.display.flip()

    def __del__(self):
        self.ChangeStat('Veh')