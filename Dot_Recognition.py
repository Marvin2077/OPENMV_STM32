from pyb import LED,Timer,UART
import sensor,image,time ,math,struct,ustruct

#初始化颜色
Red_threshold =(35, 100, 9, 127, 36, 127)#  寻色块用 红色
Blue_threshold =(0, 48, -20, 59, -66, -28)#  寻色块用 蓝色
Green_threshold =(30, 100, -64, -8, -32, 32)#  寻色块用 蓝色

#初始化传感器
sensor.reset()
sensor.set_pixformat(sensor.RGB565)#设置相机模块的像素模式
sensor.set_framesize(sensor.QQVGA)#设置相机分辨率160*120
#sensor.set_framesize() 设置图像的大小，非常重要
sensor.skip_frames(time=3000)#时钟 跳过一些无用帧待传感器稳定
sensor.set_auto_whitebal(False)#若想追踪颜色则关闭白平衡
clock = time.clock()#初始化时钟


#定义数据传输
uart = UART(3,9600)
A = 240
B = 240
C = 240
D = 240
def sending_data(A,B,C,D):
    global uart;
    #打包格式=[0x2c,0x12,int,int,0x5B]
    #data = bytearray(frame)
    data1 = ustruct.pack("<bbhhhhb",
            0x2c,   #帧头1
            0x12,   #帧头2
            int(A),# up sample by 4 Data 1
            int(B),
            int(C),# up sample by 4 Data 1
            int(D),
            0x5B)
    uart.write(data1);

def sending_data():
        global uart;
        #打包格式=[0x2c,0x12,int,int,0x5B]
        #data = bytearray(frame)
        data1 = ustruct.pack("<bbhhhhb",
                0x2c,   #帧头1
                0x12,   #帧头2
                0x5B)
        uart.write(data1);

#定义一个点类
class Dot(object):
    flag = 0
    color = 0
    x = 0
    y = 0
    #opmv_flag = 0
#实例化
Dot=Dot()

#色块识别函数
#定义函数：找到画面中最大的指定色块
def FindMax(blobs):
    max_size=1
    if blobs:
        max_blob = 0
        for blob in blobs:
            blob_size = blob.w()*blob.h()
            if ( (blob_size > max_size) & (blob_size > 100)   ) :#& (blob.density()<1.2*math.pi/4) & (blob.density()>0.8*math.pi/4)
                if ( math.fabs( blob.w() / blob.h() - 1 ) < 2.0 ) :
                    max_blob=blob
                    max_size = blob.w()*blob.h()
        return max_blob
#遍历blobs中所有的图片找到有最大目标的
def LineFilter(src, dst):
  for i in range(0, len(dst), 1):
      dst[i] = src[i<<1]
#area_threshold 面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉

#pixels_threshold 像素个数阈值，如果色块像素数量小于这个值，会被过滤掉

#merge 合并，如果设置为True，那么合并所有重叠的blob为一个。

#点检测
def DotCheck():
    img = sensor.snapshot(line_filter = LineFilter)#拍一张图像
    red_blobs = img.find_blobs([Red_threshold], pixels_threshold=3, area_threshold=6, merge=True, margin=5)#识别红色物体
    max_blob=FindMax(red_blobs)#找到最大的那个
    if max_blob:
        img.draw_cross(max_blob.cx(), max_blob.cy())#物体中心画十字
        img.draw_rectangle(max_blob.rect())#画圈
        #获取坐标并转换为+-200
        Dot.x = max_blob.cx()-80
        Dot.y = max_blob.cy()-60
        Dot.flag = 1
        #LED灯闪烁
        #LED(3).toggle()
        #LED灯闪烁
        #LED(2).toggle()
    else:
        Dot.flag = 0
        LED(2).off()
        LED(3).off()
    print(Dot.x,Dot.y,Dot.color,Dot.flag)
    sending_data(Dot.x,Dot.y,Dot.color,Dot.flag)
   # Message.UartSendData(Message.DotDataPack(Dot.color,Dot.flag,Dot.x,Dot.y,Message.Ctr.T_ms))
    return Dot.flag

while(True):
    DotCheck()
