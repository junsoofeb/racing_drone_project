import time
import keyboard
from PIL import Image
import tellopy
import datetime
import os
import sys
import threading
import schedule
import socket



drone = tellopy.Tello()


log_flag = 0
log_save_time = datetime.datetime.now().strftime('%Y%m%d%H%M')

# datetime.datetime.utcnow().strftime('%H %M %S%f')[:-5]   --> hh mm sss

first_save_state = 0

def save_state(data):
    global first_save_state
    if first_save_state == 1: # 저장된 적 있음
        f = open(f"C:/Users/feb25/Desktop/tello/racing_drone/log/{name}_{log_save_time}.txt", "r", encoding="utf-8")        
        past_time = f.readlines()[-1][ : 10].split(' ')[2]
        f.close()
        now = datetime.datetime.utcnow().strftime('%H %M %S%f')[:-5]
        if( now.split(' ')[2] != past_time ):
            f = open(f"C:/Users/feb25/Desktop/tello/racing_drone/log/{name}_{log_save_time}.txt", "a", encoding="utf-8")        
            f.write(now + ' ' + data + '\n')
            f.close()    
    else: # 첫 저장
        f = open(f"C:/Users/feb25/Desktop/tello/racing_drone/log/{name}_{log_save_time}.txt", "w+", encoding="utf-8")
        first_save_state = 1
        now = datetime.datetime.utcnow().strftime('%H %M %S%f')[:-5]
        f.write(now  + ' ' + data + '\n')
        f.close()    

    
def save_action(command):
    now = datetime.datetime.utcnow().strftime('%H %M %S%f')[:-5]
    f = open(f"C:/Users/feb25/Desktop/tello/racing_drone/log/{name}_{log_save_time}.txt", "a", encoding="utf-8")            
    f.write(now + ' ' + command + '\n')
    f.close()    
        
def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_LOG_DATA and log_flag == 1:
        save_state(str(data))
        # POS 만 추출하려면 아래 코드 사용
        #idx = str(data).find("POS")
        #save_state(str(data)[idx + 4 : idx + 22])

            
drone.subscribe(drone.EVENT_LOG_DATA, handler)
            
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

                                            ------- 시작 및 종료 -------

                                o : 시작,   ESC : 긴급 종료,    t : 이륙,    l : 착륙
                            
                                
                                            ---------  이동 ---------

                                                    w : 전진
                                                    
                                
                                    q : 반시계 방향 회전            e: 시계 방향 회전
                                
                                
                        a : 왼쪽으로                                             d : 오른쪽으로

                                                    s : 후진 
                                                    
                                            ---------  기어 ---------

                                    1 : 기어 1단    2: 기어 2단     3 : 기어 3단
                                        
                                    * 기어가 높을수록 빠른 속도, default == 기어 1단

                                
                                        ------- 고도 조절 및 정지 -------
                                
                            u : 수직 상승,         j : 수직 하강,      space bar : 제자리 정지
                                
                                
=================================================================================================================
                                조작 방법을 숙지하셨으면, 'o'를 눌러 조종을 시작하세요.
"""

print(manual)

start_flag, take_off_flag, land_flag = 0, 0, 0
g1_flag, g2_flag, g3_flag, space_flag = 0, 0, 0, 0
w_flag, a_flag, s_flag, d_flag = 0, 0, 0, 0
q_flag, e_flag, u_flag, j_flag = 0, 0, 0, 0

f_dict = {'g1_flag' : 0, 'g2_flag' : 0, 'g3_flag' : 0, 'w_flag' : 0, 'a_flag' : 0, 's_flag' : 0, 'd_flag' : 0, 'q_flag' : 0, 'e_flag' : 0, 'u_flag' : 0, 'j_flag' : 0, 'space_flag' : 0}

def other_flag(flag):
    global f_dict
    for k in f_dict.keys():
        if k != flag:
            f_dict[k] = 0
    

drone_speed = 0
while True:
    try:
        if keyboard.is_pressed('w') or keyboard.is_pressed('W'):
            try:
                drone.set_yaw(0) #양수주면 오른쪽 회전      
                drone.set_throttle(0) #양수 위로상승                              
                drone.forward(drone_speed)
                if f_dict['w_flag'] == 0:
                    save_action('w')
                    f_dict['w_flag'] = 1
                    other_flag('w_flag')
            except :
                print("\n\n\n\n\nforward error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        elif keyboard.is_pressed('space') :
            try:
                drone_speed = 0
                drone.set_pitch(0) #양수 전진
                drone.set_throttle(0) #양수 위로상승
                drone.set_roll(0)  #양수 오른쪽으로
                drone.set_yaw(0) #양수 시계방향 회전
                if f_dict['space_flag'] == 0:
                    save_action('space')
                    f_dict['space_flag'] = 1
                    other_flag('space_flag')
            except:
                print("\n\n\n\n\nhold error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        elif keyboard.is_pressed('d') or keyboard.is_pressed('D'):
            try:

                drone.set_throttle(0) #양수 위로상승
                drone.set_yaw(0) #양수주면 오른쪽 회전                    
                drone.right(drone_speed)
                if f_dict['d_flag'] == 0:
                    save_action('d')
                    f_dict['d_flag'] = 1
                    other_flag('d_flag')
            except :
                print("right error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        elif keyboard.is_pressed('a') or keyboard.is_pressed('A'):
            try:
                drone.set_throttle(0) #양수 위로상승
                drone.set_yaw(0) #양수주면 오른쪽 회전                    
                drone.left(drone_speed)
                if f_dict['a_flag']  == 0:
                    save_action('a')
                    f_dict['a_flag']  = 1
                    other_flag('a_flag')
            except:
                print("left error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        elif keyboard.is_pressed('s') or keyboard.is_pressed('S'):
            try:
                drone.set_throttle(0) #양수 위로상승
                drone.set_yaw(0) #양수주면 오른쪽 회전                    
                drone.backward(drone_speed)
                if f_dict['s_flag']  == 0:
                    save_action('s')
                    f_dict['s_flag']  = 1
                    other_flag('s_flag')
            except:
                print("back error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        elif keyboard.is_pressed('q') or keyboard.is_pressed('Q'):
            try:
                drone.counter_clockwise(drone_speed)
                if f_dict['q_flag']  == 0:
                    save_action('q')
                    f_dict['q_flag'] = 1
                    other_flag('q_flag')
            except Exception as e:
                print("diagonal_left_f error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(e)
        elif keyboard.is_pressed('e') or keyboard.is_pressed('E'):
            try:
                drone.clockwise(drone_speed)
                if f_dict['e_flag']  == 0:
                    save_action('e')
                    f_dict['e_flag'] = 1
                    other_flag('e_flag')
            except Exception as e:
                print("diagonal_right_f error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print(e)
        elif keyboard.is_pressed('u') or keyboard.is_pressed('U'):
            try:
                drone.set_yaw(0) #양수주면 오른쪽 회전                    
                drone.up(drone_speed)
                if f_dict['u_flag']  == 0:
                    save_action('u')
                    f_dict['u_flag'] = 1
                    other_flag('u_flag')
            except :
                print("up error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        elif keyboard.is_pressed('j') or keyboard.is_pressed('J'):
            try:
                drone.set_yaw(0) #양수주면 오른쪽 회전                    
                drone.down(drone_speed)
                if f_dict['j_flag']  == 0:
                    save_action('j')
                    f_dict['j_flag'] = 1
                    other_flag('j_flag')
            except :
                print("down error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            action_flag = 1
        elif keyboard.is_pressed('t') or keyboard.is_pressed('T'):
            if take_off_flag == 0:
                take_off_flag = 1
                drone.takeoff()                
                save_action('t')
                print('이제 이륙합니다.\n조종을 준비하세요!')
                cnt = 3
                while( cnt != 0):
                    print("%d 초 뒤에 시작됩니다." % cnt)
                    cnt -= 1
                    time.sleep(1)
                print('이륙 완료!')
                drone_speed = 15
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
                break
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
                log_flag = 1                
                start_flag = 1
            else:
                continue
        elif keyboard.is_pressed(b"1".decode('ascii')) :
            drone_speed = 30
            if f_dict['g1_flag'] == 0:
                save_action('1')
                f_dict['g1_flag'] = 1
                other_flag('g1_flag')
            continue
        elif keyboard.is_pressed(b"2".decode('ascii')) :
            drone_speed = 45
            if f_dict['g2_flag'] == 0:
                save_action('2')
                f_dict['g2_flag'] = 1
                other_flag('g2_flag')
            continue
        elif keyboard.is_pressed(b"3".decode('ascii')) :
            drone_speed = 60
            if f_dict['g3_flag'] == 0:
                save_action('3')
                f_dict['g3_flag'] = 1
                other_flag('g3_flag')
            continue
        elif keyboard.is_pressed('esc') :
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
        

# 여기서부터는 return base
# 좌표 계산은 로그 파일에서 x,y,z 읽어서 
'''
host = ''
port = 9000
locaddr = (host,port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sockert.socket() 소켓을 생성
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)
# 서버의 ip('192.168.10.1')와 포트번호(8889)를 고정


def recv():
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518)
            # sock.recv(1518) 데이터 수신 대기(최대 수신 가능 data의 크기 1518-byte))
            print(data.decode(encoding="utf-8"))
            # data.decode() 받은 데이터 출력
        except Exception:
            print ('\nrecv() 함수 동작 중 Send MSG ERROR . . .\n')
            break


recvThread = threading.Thread(target=recv)
# threading.Thread(target=recv) 쓰레드가 호출 가능한 오브젝트로 recv를 지정
recvThread.start()
# 쓰레드 시작. 쓰레드 오브젝트 당 최대 1번만 호출 가능.

def sendmsg(msg):
    try:
        msg = msg.encode(encoding = "utf-8")
        sent = sock.sendto(msg, tello_address)
        # sock.sendto(bytes, address) 소켓으로 data 전송
    except :
        print ('\nsendmsg() 동작 중 에러발생 . . .\n')
        sock.close()  
    
def start():
    sendmsg('command')
    
def return_to_base(x, y, z):
    sendmsg(f'go {x} {y} {z}')
    
start()
return_to_base(좌표 계산 결과 넣어)
'''