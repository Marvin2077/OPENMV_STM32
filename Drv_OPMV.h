
#include "stm32f1xx_hal.h"

#define RXBUFFER_LEN 12

typedef struct
{
	long int 	x_cm;
	long int  y_cm;
	int openmv;
}OPMV_info;

extern OPMV_info User_openmv;
void Openmv_GetOneByte(uint8_t data);



