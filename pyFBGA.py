from ctypes import *
import time


class PyFBGA():

    '''Rewrite functions in FBGA_DA.dll

    Make a class to simplify working with FBGA_DA.dll
    '''

    def __init__(self, path, ip, port, count):
        '''init object

        path:   FBGA_DA.dll's path
        ip:     the server's ip address
        port:   the server's port
        count:  instruments' counts

        example: ('D:\Work\FBGA_DR.dll', '172.22.49.143', 9100, 4)
        '''

        class SSensorVal(Structure):
            _fields_ = [('nSensorNumber', c_ushort),
                        ('fWaveLen', c_float),
                        ('fPhyVal', c_double)]

        self.dll = CDLL(path)               # load dll
        self.ip = c_char_p(ip)
        self.port = c_int(port)

        SSensorVals = SSensorVal * count   # define struct's arrays
        self.count = c_int(count)          # define 'SensorCount'
        self.pCount = pointer(self.count)   # define 'pSensorCount'
        self.data = SSensorVals()        # Get a struct's array
        self.pData = pointer(self.data)         # Get it's pointer

    def connect(self):
        '''connect to server

        return  1 if OK
               -1 if socket error
               -2 if conncet failed
        '''

        return self.dll.FBGA_Connect(self.ip, self.port)

    def get_data(self):
        '''Get data from server and instruments

        data take to self.data
        return 1 if OK
              -1 if Failed
        '''

        self.time = time.ctime()

        return self.dll.FBGA_GetSensorVal(self.pData, self.pCount)

    def disconnect(self):
        '''Disconnect from server
        '''

        return self.dll.FBGA_Disconnect()

    def trans_list(self):
        '''trans data from struct_array to tuples'list
        '''

        self.lData = [self.time]
        for i in self.data:
            self.lData.append((i.nSensorNumber,
                               i.fWaveLen,
                               i.fPhyVal))

# if __name__ == '__main__':
#     test = PyFBGA('FBGA_DR.dll', '172.22.49.143', 9100, 4)
#     print test.connect()
#     # print test.get_data()
#     # test.trans_list()
#     # print test.lData
#     while True:
#         test.get_data()
#         test.trans_list()
#         print test.lData[1], test.lData[2], test.lData[3], test.lData[4]
#     print test.disconnect()
