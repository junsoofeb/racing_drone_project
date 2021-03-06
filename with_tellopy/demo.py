import time
import keyboard
from PIL import Image
import tellopy
import datetime
import os
import sys

log_flag = 0
log_save_time = datetime.datetime.now().strftime('%Y%m%d')

# datetime.datetime.utcnow().strftime('%H %M %S%f')[:-5]   --> hh mm sss

first_save_state = 0
first_save_action = 0

def save_state(data):
    global first_save_state
    if first_save_state == 1: # 저장된 적 있음
        f = open(f"C:/Users/feb25/Desktop/tello/racing_drone/log/{name}_{log_save_time}.txt", "r", encoding="utf-8")        
        past_time = f.readlines()[-1][ : 10].split(' ')[2] # 로그 데이터의 sss
        f.close()
        now = datetime.datetime.utcnow().strftime('%H %M %S%f')[:-5] # 현재 시간의 sss
        if( now.split(' ')[2] != past_time ): 
            f = open(f"C:/Users/feb25/Desktop/tello/racing_drone/log/{name}_{log_save_time}.txt", "a", encoding="utf-8")        
            f.write(now + ' ' + data + '\n')
            f.close()    
    else: # 첫 저장
        f = open(f"C:/Users/feb25/Desktop/tello/racing_drone/log/{name}_{log_save_time}.txt", "a", encoding="utf-8")
        first_save_state = 1
        now = datetime.datetime.utcnow().strftime('%H %M %S%f')[:-5]
        f.write(now  + ' ' + data + '\n')
        f.close()    

    
def save_action(command):
    global first_save_action
    if  first_save_action == 1:
        f = open(f"C:/Users/feb25/Desktop/tello/racing_drone/log/{name}_{log_save_time}.txt", "r", encoding="utf-8")
        past_time = f.readlines()[-1][ : 10].split(' ')[2]
        f.close()
        now = datetime.datetime.utcnow().strftime('%H %M %S%f')[:-5]
        if( now.split(' ')[2] != past_time ):
            f = open(f"C:/Users/feb25/Desktop/tello/racing_drone/log/{name}_{log_save_time}.txt", "a", encoding="utf-8")            
            f.write(now + ' ' + command + '\n')
            f.close()    
    else:      
        f = open(f"C:/Users/feb25/Desktop/tello/racing_drone/log/{name}_{log_save_time}.txt", "a", encoding="utf-8")
        first_save_action = 1        
        now = datetime.datetime.utcnow().strftime('%H %M %S%f')[:-5]
        f.write(now + ' ' + command + '\n')
        f.close()    
        
def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_LOG_DATA and log_flag == 1:
        idx = str(data).find("POS")
        save_state(str(data)[idx + 4 : idx + 22])
        #print('%s: %s' % (event.name, str(data)))        
        #tello_log += str(data)
    
# lap time 계산용
start_time = None

name = 'parkjunsoo'
# 추가 정보 입력도 필요??
#name = input("이름 :")
#print("사용자의 정보가 저장되었습니다.")

# 드론 조종 메뉴얼
#img = Image.open('./control_map.png')
#img.show()


manual = """
=================================================== 조작 방법 ===================================================

                                o : 시작, t : 이륙, l : 착륙 , p : 긴급 종료
                                
                                w : 전진, s : 후진, a : 왼쪽으로,  d : 오른쪽으로
                                
                                q : 반시계 방향 회전  e: 시계 방향  회전
                                
                                u : 수직 상승, j : 수직 하강, h : 제자리 정지
                                        
=================================================================================================================
                                조작 방법을 숙지하셨으면, 'o'를 눌러 조종을 시작하세요.
"""

print(manual)
start_flag = 0
take_off_flag = 0
land_flag = 0
action_flag = 0

drone = tellopy.Tello()
drone.subscribe(drone.EVENT_LOG_DATA, handler)

while True:  
    try:
        if keyboard.is_pressed('w') or keyboard.is_pressed('W'):
            try:
                if action_flag == 0:
                    save_action('w')
                    action_flag = 1
                drone.set_yaw(0) #양수주면 오른쪽 회전      
                drone.set_throttle(0) #양수 위로상승                              
                drone.forward(20)
            except :
                print("\n\n\n\n\nforward error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            action_flag = 0
        elif keyboard.is_pressed('h') or keyboard.is_pressed('H'):
            try:
                if action_flag == 0:
                    save_action('h')
                    action_flag = 1
                drone.set_pitch(0) #양수 전진
                drone.set_throttle(0) #양수 위로상승
                drone.set_roll(0)  #양수 오른쪽으로
                drone.set_yaw(0) #양수 시계방향 회전
            except:
                print("\n\n\n\n\nhold error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            action_flag = 0
        elif keyboard.is_pressed('d') or keyboard.is_pressed('D'):
            try:
                if action_flag == 0:
                    save_action('d')
                    action_flag = 1
                drone.set_throttle(0) #양수 위로상승
                drone.set_yaw(0) #양수주면 오른쪽 회전                    
                drone.right(20)
            except :
                print("right error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            action_flag = 0
        elif keyboard.is_pressed('a') or keyboard.is_pressed('A'):
            try:
                if action_flag == 0:
                    save_action('a')
                    action_flag = 1
                drone.set_throttle(0) #양수 위로상승
                drone.set_yaw(0) #양수주면 오른쪽 회전                    
                drone.left(20)
            except:
                print("left error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            action_flag = 0
        elif keyboard.is_pressed('s') or keyboard.is_pressed('S'):
            try:
                if action_flag == 0:
                    save_action('s')
                    action_flag = 1
                drone.set_throttle(0) #양수 위로상승
                drone.set_yaw(0) #양수주면 오른쪽 회전                    
                drone.backward(20)
            except:
                print("back error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            action_flag = 0
        elif keyboard.is_pressed('q') or keyboard.is_pressed('Q'):
            try:
                if action_flag == 0:
                    save_action('q')
                    action_flag = 1
                drone.counter_clockwise(45)
            except Exception as e:
                print("diagonal_left_f error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(e)
            action_flag = 0
        elif keyboard.is_pressed('e') or keyboard.is_pressed('E'):
            try:
                if action_flag == 0:
                    save_action('e')
                    action_flag = 1
                drone.clockwise(45)
            except Exception as e:
                print("diagonal_right_f error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(e)
            action_flag = 0
        elif keyboard.is_pressed('u') or keyboard.is_pressed('U'):
            try:
                if action_flag == 0:
                    save_action('u')
                    action_flag = 1
                drone.set_yaw(0) #양수주면 오른쪽 회전                    
                drone.up(20)
            except :
                print("up error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            action_flag = 0
        elif keyboard.is_pressed('j') or keyboard.is_pressed('J'):
            try:
                if action_flag == 0:
                    save_action('j')
                    action_flag = 1
                drone.set_yaw(0) #양수주면 오른쪽 회전                    
                drone.down(20)
            except :
                print("down error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            action_flag = 1
        elif keyboard.is_pressed('t') or keyboard.is_pressed('T'):
            if take_off_flag == 0:
                log_flag = 1
                save_action('t')
                drone.takeoff()                
                print('이제 이륙합니다.\n조종을 준비하세요!')
                cnt = 3
                take_off_flag = 1
                while( cnt != 0):
                    print("%d 초 뒤에 시작됩니다." % cnt)
                    cnt -= 1
                    time.sleep(1)
                print('이륙 완료!')
                start_time = time.time()
                print("시간 측정 시작!\n조종을 시작하세요!")    
                time.sleep(0.1)        
            else:
                continue
        elif keyboard.is_pressed('l') or keyboard.is_pressed('L'):
            if land_flag == 0:
                land_flag = 1
                save_action('l')
                drone.set_pitch(0) #양수 전진
                drone.set_throttle(0) #양수 위로상승
                drone.set_roll(0)  #양수 오른쪽으로
                drone.set_yaw(0) #양수 시계방향 회전
                drone.land()
                print('이제 착륙합니다.')
                time.sleep(4)
                log_flag = 0
                lap_time = round(time.time() - start_time, 3)
                print(f"\n\n\n\n\n{name} 님의 Racing Lap Time: %0.3f Seconds\n\n\n\n\n" % (lap_time))            
                drone.quit()
                sys.exit()
            else:
                continue
        elif keyboard.is_pressed('o') or keyboard.is_pressed('O'):
            if start_flag == 0:
                try:
                    # PC와 드론 연결
                    drone.connect()
                    drone.wait_for_connection(10.0)
                except:
                    print("드론 연결 실패!!!!!!")
                    sys.exit()
                print("\n드론 조종을 시작합니다.\n")       
                print("\n'T'를 눌러 이륙하세요. 이륙 후 착륙하려면 'L'을 누르세요." )
                start_flag = 1
            else:
                continue
            
        elif keyboard.is_pressed('p') or keyboard.is_pressed('P'):
            try:
                drone.set_pitch(0) #양수 전진
                drone.set_throttle(0) #양수 위로상승
                drone.set_roll(0)  #양수 오른쪽으로
                drone.set_yaw(0) #양수 시계방향 회전
                drone.land()
            except :
                print("비상착륙 에러!!!!")
                continue
            finally:
                drone.quit()
                print("\n\n비상 착륙 완료, 프로그램이 종료됩니다.\n\n")
                sys.exit()
        # 지정된 키가 아니면 루프 반복
        else:
            continue
    except:
        if land_flag == 0:
            print("while문 동작 중 에러!") 
            drone.quit()
            sys.exit()
            break
        else:
            drone.quit()
            sys.exit()
            break