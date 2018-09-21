#-*- coding: utf-8 -*-
import sys
import struct
class richheader:
    def __init__(self,fp):
        data=fp.read()
        end=struct.unpack('<I', data[0x3c:0x40])[0]#end address of rich header // rich header의 끝 주소
        #print hex(end)
        data=data[0x80:end]
        rich_addr=data.find(b'Rich')#find 'Rich' // Rich 문자열을 찾는다.
        self.xorkey=data[rich_addr+4:rich_addr+8]
        self.data=data[:rich_addr]
        self.clear_data=''
        for i in range(len(self.data)):
            self.clear_data+=chr(ord(self.data[i])^ord(self.xorkey[i%4]))#extract clear_data // clear_data 추출
        #print list(self.clear_data)
        self.info=[]#information list // 정보 리스트
        for i in range(16,len(self.clear_data),8):
            compid=struct.unpack('<I',self.clear_data[i:i+4])[0]
            count=struct.unpack('<I',self.clear_data[i+4:i+8])[0]
            info=Info(compid,count)
            self.info.append(info)
        #print self.info
    
    def prodid_similarity(self,and_info):
        set1=[]
        set2=[]
        for i,j in zip(self.info,and_info.info):#make set
            set1.append(i.prodid)
            set2.append(j.prodid)
        result=len(set(set1)&set(set2))#Intersection sets // 교집합시키기
        print result
        return result


class Info:
    def __init__(self,compid,count):
        self.compid=compid
        self.prodid=compid>>16
        self.build=compid&0xffff
        self.count=count
        

fp1=open(sys.argv[1],'rb')
a1=richheader(fp1)
fp2=open(sys.argv[2],'rb')
a2=richheader(fp2)

a1.prodid_similarity(a2)