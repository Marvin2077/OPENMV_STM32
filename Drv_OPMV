#include "Drv_OPMV.h"

OPMV_info User_openmv;
extern signed temp1, temp2;
signed temp1= 0, temp2= 0;
//通讯用
void Openmv_GetOneByte(uint8_t data)
{
	static signed RxBuffer2[10];
	static uint8_t rxstate1 =0;
	static uint8_t Rxcounter2 =0;
	if(rxstate1 == 0 && data == 0x2c)
	{
		rxstate1 = 1;
		RxBuffer2[Rxcounter2++] = data;
	}
	else if(rxstate1 == 1 && data == 0x12)
	{
		rxstate1 = 2;
		RxBuffer2[Rxcounter2++] = data;
	}
	
	else if (rxstate1 == 2)
	{
		RxBuffer2[Rxcounter2++] = data;
		if(data == 0x5B)
		{
		rxstate1= 3;
		}
	}
		else
		{
			rxstate1 = 0;
			Rxcounter2 = 0;
		}
		if (rxstate1 == 3)
		{
			if(RxBuffer2[Rxcounter2-1]==0x5B)
			{
				
				temp1 = RxBuffer2[3]<<8|RxBuffer2[2];    //x
     		temp2 = RxBuffer2[5]<<8|RxBuffer2[4];    //y

				if(temp1>1000)
				{
					temp1 =-(65536 -temp1);
				}
				if(temp2>1000)
				{
					temp2 =-(65536 -temp2);
				}
				if(temp1 > -80 && temp1 < 80)
				{
					 User_openmv.x_cm = temp1;
					 if(User_openmv.x_cm>1000)
					 {
						 User_openmv.x_cm =-(65536 - User_openmv.x_cm);
					 }
				}
				
				if(temp2 > -80 && temp2 < 0)
				{
					 User_openmv.y_cm = temp2;
					 if(User_openmv.y_cm>1000)
					 {
						 User_openmv.y_cm =-(65536 - User_openmv.y_cm);
					 }
				}
				rxstate1 = 0;
				Rxcounter2 = 0;
				User_openmv.openmv= 1;
				
			}
			else
			{
				rxstate1 = 0;
				Rxcounter2 = 0;
			}
		}
}

