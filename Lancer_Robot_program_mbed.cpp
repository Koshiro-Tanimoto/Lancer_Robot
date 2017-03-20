#include "mbed.h"
#include "rtos.h"

///////////Parameter config/////////////
#define Motor_Speed 100
#define Play_time 32
#define kp_max 5
#define ki_max 0
#define kd_max 0
#define kp_const 0
#define ki_const 0
#define kd_const 0
////////////////////////////////////////

//Ticker
Ticker rc;

//Pinmode of motor controll
PwmOut motor1(p26);
PwmOut motor2(p25);
PwmOut motor3(p24);
PwmOut motor4(p23);
PwmOut servo1(p21);

//Pinmode of gain config
AnalogIn Kp_gain(p20);
AnalogIn Ki_gain(p19);
AnalogIn Kd_gain(p18);

//LED config
DigitalOut led1(LED1);
DigitalOut led2(LED2);
DigitalOut led3(LED3);
DigitalOut led4(LED4);

//Serial config(from Raspberry Pi)
Serial RasPi(USBTX, USBRX);
//Serial pc(p13,p14);

//Global parameters
//float KP = 0.78, KI = 0.13, KD = 0.5;
const float attach_time = 0.0005;
float KP = 0, KI = 0, KD = 0;
int l_flag=0, s_flag=0, turn_flag=0, end_flag=0, curve_flag = 0;
int mdev=0, pid_dev=0, lance = 1280;
///////////////////////////////////////////////////////////////////////////////

//Attach function
void rd(){
    if(mdev > 0) turn_flag = 1;
    else if(mdev < 0) turn_flag = 2;
    else turn_flag = 0;
    pid_dev = abs(mdev);
    s_flag = l_flag;
}

//Lance controll function
void s_controll(){
    while(1){
        switch(s_flag){
            case 1:
            curve_flag = 1;
            break;
            case 2:
            led2 = 1;
            led3 = 0;
            servo1.pulsewidth_us(1730); //right
            wait(3);
            break;
            case 3:
            led2 = 0;
            led3 = 1;
            servo1.pulsewidth_us(850);  //left
            wait(3);
            break;
            default:
            led2 = 0;
            led3 = 0;
            servo1.pulsewidth_us(1280); //center
            break;
        }
    }
}

//Serial communication
void RasPi_serial(){
     char rdev[4],ldev[2];
     
     if(RasPi.readable() == 1){
         RasPi.scanf("%s",&rdev);
         RasPi.scanf("%s",&ldev);
         mdev = atoi(rdev);
         l_flag = atoi(ldev);
     }
}

//Gain config function
void gain_config(){
    KP = kp_max * Kp_gain + kp_const;
    KI = ki_max * Ki_gain + ki_const;
    KD = kd_max * Kd_gain + kd_const;
}

//Calculation of pid gain 
int PID_function() {  
    int diff[1] = {}, integral, pid_gain, p, i, d;
    
    diff[0] = diff[1];
    diff[1] = pid_dev;
    integral += (diff[1] + diff[0]) / 2.0 * attach_time;
    
    p = KP * diff[1];
    i = KI * integral;
    d = KD * (diff[1]-diff[0]) / attach_time;
    
    pid_gain = p + i + d;
    if(pid_gain > Motor_Speed) pid_gain = Motor_Speed;
    return pid_gain;
}

//Body controll function
void body_controll(int gain){
    switch(turn_flag){
        case 0: //Straight
               led1 = 1;
               led4 = 1;
               motor1.pulsewidth_ms(Motor_Speed);
               motor3.pulsewidth_ms(Motor_Speed);
               break;
        case 1: //Left turn  
               led1 = 1;
               led4 = 0;
               motor1.pulsewidth_ms(Motor_Speed - gain);
               motor3.pulsewidth_ms(Motor_Speed);
               break;
        case 2: //Right turn
               led1 = 0;
               led4 = 1;
               motor1.pulsewidth_ms(Motor_Speed);
               motor3.pulsewidth_ms(Motor_Speed - gain);
               break;       
    }     
} 

//Main function
int main() {  
    int gain;
    
    //Serial baud config
    RasPi.baud(115200);
    //pc.baud(115200);
    
    //Pluse config
    motor1.period_ms(100);
    motor2.period_ms(100);
    motor3.period_ms(100);
    motor4.period_ms(100);
    servo1.period_ms(20);
    
    //LED Initialization
    led1 = 0;
    led2 = 0;
    led3 = 0;
    led4 = 0;
    
    //Interrupt processing
    rc.attach(&rd,attach_time);
    
    //Thread config
    Thread T1(s_controll);
    
    //Main process
    while(1){
            RasPi_serial();
            if(mdev == 999){
                 led1 = 0;
                 led2 = 0;
                 led3 = 0;
                 led4 = 0;
                 motor1.pulsewidth_ms(0);
                 motor3.pulsewidth_ms(0);
            }
            else{
               gain_config();
               gain = PID_function();
               body_controll(gain);
            }
            //RasPi.printf("KP:%3.5f KI:%3.5f KD:%3.5f dev:%3d\r\n",KP,KI,KD,mdev);
            //RasPi.printf("dev:%3d  L_flag:%2d\r\n",mdev,l_flag);
    }
}