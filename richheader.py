#-*- coding: utf-8 -*-
import sys
import struct
class richheader:
    def __init__(self,fp):
        data=fp.read()
        end=struct.unpack('<I', data[0x3c:0x40])[0]
        print hex(end)
        data=data[0x80:end]
        rich_addr=data.find(b'Rich')
        self.xorkey=data[rich_addr+4:rich_addr+8]
        self.data=data[:rich_addr]
        self.clear_data=''
        for i in range(len(self.data)):
            self.clear_data+=chr(ord(self.data[i])^ord(self.xorkey[i%4]))
        print list(self.clear_data)
        self.info=[]
        for i in range(16,len(self.clear_data),8):
            info=Info(struct.unpack('<I',self.clear_data[i:i+4])[0],struct.unpack('<I',self.clear_data[i+4:i+8][0]))
            self.info.append(info)
        print self.info

class Info:
    def __init__(self,compid,count):
        self.compid=compid
        self.prodid=compid>>16
        self.build=compid&0xffff
        self.count=count
        

fp=open(sys.argv[1],'rb')
richheader(fp)