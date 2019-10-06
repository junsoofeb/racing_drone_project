import threading
import socket
import sys
import time
import keyboard

host = ''
port = 9000
locaddr = (host,port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sockert.socket() 소켓을 생성
tello_address = ('192.168.10.1', 8889)
sock.bind(locaddr)
# 서버의 ip('192.168.10.1')와 포트번호(8889)를 고정

drone_speed = None
rotate_speed = 100
rotate_distance = 40

def recv():
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518)
            # sock.recv(1518) 데이터 수신 대기(최대 수신 가능 data의 크기 1518-byte))
            print(data.decode(encoding="utf-8"))
            # data.decode() 받은 데이터 출력
        except Exception:
            print ('\nSend MSG ERROR . . .\n')
            break


recvThread = threading.Thread(target=recv)
# threading.Thread(target=recv) 쓰레드가 호출 가능한 오브젝트로 recv를 지정
recvThread.start()
# 쓰레드 시작. 쓰레드 오브젝트 당 최대 1번만 호출 가능.

def sendmsg(msg):
    try:
        msg = msg.encode(encoding="utf-8")
        sent = sock.sendto(msg, tello_address)
        # sock.sendto(bytes, address) 소켓으로 data 전송
    except :
        print ('\nsendmsg() 동작 중 에러발생 . . .\n')
        sock.close()  
    
def start():
    sendmsg('command')

def takeoff():
    sendmsg('takeoff')

def land():
    sendmsg('land')

def set_speed(x):
    sendmsg(f'speed {x}')

def get_speed():
    sendmsg('speed?')

def forward(x):
    sendmsg(f'forward {x}')

def back(x):
    sendmsg(f'back {x}')

def right(x):
    sendmsg(f'right {x}')

def left(x):
    sendmsg(f'left {x}')
    
def up(x):
    sendmsg(f'up {x}')

def down(x):
    sendmsg(f'down {x}')

# 기체 회전 각도는 1 ~ 360 degree
def rotate_right(x):
    sendmsg(f'cw {x}')

def rotate_left(x):
    sendmsg(f'ccw {x}')



'''
# 속도 지정..
command ===> speed x 

set speed to x cm/s
x: 10-100

def set_speed(x, y, z):
    sendmsg(f'speed {x}')
    sendmsg(f'speed {y}')
    sendmsg(f'speed {z}')
'''

# action , state 저장용
action_list = []
state_list = []

# state 계산용
start_time = None
previous_position = [ [0, 0, 0] ]


# 전후좌우 위, 아래 이동거리는 20 ~ 500
# test에서는 안전을 위해 이동 거리 20으로 설정

# x_t+1 = x_t + drone_spee(t+1 - t)
# x, y, z 속도는 동일..

# 실 측정결과 약 30cm 이동!  drone_speed * (t+1 - t) 가 30

def x_pos(x_position = 0, signal = 0):
    if signal == 0:
        current_x_position = x_position + 30
    else:
        current_x_position = x_position - 30
        
    return current_x_position

def y_pos(y_position = 0, signal = 0):
    if signal == 0:
        current_y_position = y_position + 30
    else:
        current_y_position = y_position - 30
    
    return current_y_position

def z_pos(z_position = 0, signal = 0):
    if signal == 0:
        current_z_position = z_position + 30
    else:
        current_z_position = z_position - 30
        
    return current_z_position

# 추가 정보 입력도 필요??
name = input("이름 :")
print("사용자의 정보가 저장되었습니다.")

manual = """
=================================================== 조작 방법 ===================================================

                                            ------ 시작 및 이동 ------

                                        o : 시작, t : 이륙, l : 착륙 , p : 긴급 종료

                                        w : 전진, s : 후진, a : 왼쪽,  d : 오른쪽

                                        u : 수직 상승, j : 수직 하강

                                              ------ 드론 회전 ------

                                        q : 왼쪽 45°  회전, e : 오른쪽 45°  회전

                                        z : 왼쪽 135° 회전, c : 오른쪽 135° 회전
                                        
=================================================================================================================

                                조작 방법을 숙지하셨으면, 'o'를 눌러 조종을 시작하세요.
"""

print(manual)
command_flag = 0
take_off_flag = 0
land_flag = 0

# UDP 통신이라 신호보내면 중간에 못 바꾼다. -> 키 입력시간 2초 간격을 줌 
# 또한 멀티 입력 불가 -> ex) 직진하면서 동시에 오른쪽으로 주행 불가!!
# 해결책 ==> 드론의 이동속도를 적당히 빠르게 해서, 동작 후 보고 조종할 수 있도록   대신 단타로.. 누르고 있기 허용하면 위험..
# 드론 속도가 느리면 사용자가 원하는 위치까지 갈때까지 키를 누르고 있기 때문..


# 드론 전진 방향이 x 축  앞으로 == +  뒤로 == -
# 드론 수직이 y 축      위로 == +  아래로 == -
# 드론 좌우가 z축       오른쪽 == + 왼쪽 == -
while True:  
    try:
        if keyboard.is_pressed('w') or keyboard.is_pressed('W'):
                try:
                    forward(40)
                except :
                    print("forward error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                finally:
                    print('w')
                    action_list.append('w')
                    x = x_pos(previous_position[-1][0])
                    y = previous_position[-1][1]
                    z = previous_position[-1][2]
                    previous_position.append([x, y, z])
                    time.sleep(2)
                    print('앞으로 이동 완료')
        elif keyboard.is_pressed('d') or keyboard.is_pressed('D'):
                try:
                    right(40)
                except :
                    print("right error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                finally:
                    print('d')  
                    action_list.append('d')
                    x = previous_position[-1][0]
                    y = previous_position[-1][1]
                    z = z_pos(previous_position[-1][2])
                    previous_position.append([x, y, z])
                    time.sleep(2)
                    print('오른쪽으로 이동 완료')
        elif keyboard.is_pressed('a') or keyboard.is_pressed('A'):
                try:
                    left(40)
                except:
                    print("left error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                finally:
                    print('a')  
                    action_list.append('a')
                    x = previous_position[-1][0]
                    y = previous_position[-1][1]
                    z = z_pos(previous_position[-1][2], -1)
                    previous_position.append([x, y, z])
                    time.sleep(2)
                    print('왼쪽으로 이동 완료')
        elif keyboard.is_pressed('s') or keyboard.is_pressed('S'):
                try:
                    back(40)
                except:
                    print("back error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                finally:
                    print('s')
                    action_list.append('s')
                    x = x_pos(previous_position[-1][0], -1)
                    y = previous_position[-1][1]
                    z = previous_position[-1][2]
                    previous_position.append([x, y, z])
                    time.sleep(2)
                    print('뒤쪽으로 이동 완료')
        elif keyboard.is_pressed('u') or keyboard.is_pressed('U'):
                try:
                    up(40)
                except :
                    print("up error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                finally:                
                    print('u')           
                    action_list.append('u')
                    x = previous_position[-1][0]
                    y = y_pos(previous_position[-1][1])
                    z = previous_position[-1][2]
                    previous_position.append([x, y, z])                
                    time.sleep(2)
                    print('위로 이동 완료')
        elif keyboard.is_pressed('j') or keyboard.is_pressed('J'):
                try:
                    down(40)
                except :
                    print("down error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                finally:
                    action_list.append('j')
                    print('j')  
                    x = previous_position[-1][0]
                    y = y_pos(previous_position[-1][1], -1)
                    z = previous_position[-1][2]
                    previous_position.append([x, y, z])
                    time.sleep(2)
                    print('아래로 이동 완료')
        elif keyboard.is_pressed('q') or keyboard.is_pressed('Q'):
                try:
                    rotate_left(45)
                except Exception as e:
                    print("rotate_left_f error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(e)
                finally:                
                    print('q')           
                    action_list.append('q')
                    time.sleep(2)                    
                    print('왼쪽 45° 회전 완료')
        elif keyboard.is_pressed('e') or keyboard.is_pressed('E'):
                try:
                    rotate_right(45)                   
                except :
                    print("rotate_right_f error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                finally:                
                    print('e')           
                    action_list.append('e')
                    time.sleep(2)                    
                    print('오른쪽 45° 회전 완료')
        elif keyboard.is_pressed('z') or keyboard.is_pressed('Z'):
                try:
                    rotate_left(135)
                except :
                    print("rotate_left_b error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                finally:                
                    print('z')           
                    action_list.append('z')
                    time.sleep(2)
                    print('왼쪽 135° 회전 완료')
        elif keyboard.is_pressed('c') or keyboard.is_pressed('C'):
                try:
                    rotate_right(135)
                except :
                    print("rotate_right_b error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                finally:                
                    print('c')           
                    action_list.append('c')
                    time.sleep(2)
                    print('오른쪽 135° 회전 완료')
        elif keyboard.is_pressed('t') or keyboard.is_pressed('T'):
            if take_off_flag == 0:
                action_list.append('t')
                print('이륙합니다.\n조종을 준비하세요!')
                takeoff()                
                cnt = 3
                while( cnt != 0):
                    print("%d 초 뒤 부터 시간 측정이 시작됩니다." % cnt)
                    cnt -= 1
                    time.sleep(1)
                
                print("시간 측정 시작!\n조종을 시작하세요!")    
                take_off_flag = 1
                start_time = time.time()
                continue
            else:
                continue
        elif keyboard.is_pressed('l') or keyboard.is_pressed('L'):
            if land_flag == 0:
                action_list.append('l')
                print('이제 착륙합니다.')
                land()
                time.sleep(0.1)
                
                print(f"{name} 님의 Racing Lap Time: %0.3f Seconds"%((time.time() - start_time )))
                land_flag = 1
                # action 문서화
                #f = open(f"C:/Users/feb25/Desktop/tello/get_action/action_list_{name}.txt", "w")
                #for action in action_list:
                #    f.write(action + ' ')
                #f.close()

                print("action_list 작성 완료\n")
                
                # state 문서화
                #f = open("C:/Users/feb25/Desktop/tello/get_action/state_list_{name}.txt", "w")
                #for state_list in previous_position:
                #    for state in state_list:
                #        f.write(state + ' ', end = " ")
                #f.close()
                
                print(action_list)

                print("\nstate_list 작성 완료\n")
                
                print(previous_position)
                sock.close()
                print("\n소켓 통신 종료")
                sys.exit()
            else:
                continue
        elif keyboard.is_pressed('o') or keyboard.is_pressed('O'):
            if command_flag == 0:
                action_list.append('o')
                try:
                    print("\n드론 조종을 시작합니다.\n")       
                    start()
                    time.sleep(0.1)
                    # 설정 가능한 drone_speed 범위 10 ~ 100 cm/sec   
                    drone_speed = 20
                    # test에서는 안전을 위해 느리게 설정함
                    print("속도 : 20 cm/sec 으로 설정있습니다.")
                    set_speed(drone_speed)
                    time.sleep(0.1)
                    print("'T'를 눌러 이륙하세요. 이륙 후 착륙하려면 'L'을 누르세요." )
                    command_flag = 1
                except:
                    print("command msg error!!!!!!")
                    continue
            else:
                continue
            
        elif keyboard.is_pressed('p') or keyboard.is_pressed('P'):
            land()
            time.sleep(0.1)
            print("\n\n비상 착륙 완료, 프로그램이 종료됩니다.\n\n")
            sock.close()
            sys.exit()
            
        # 지정된 키가 아니면 루프 반복
        else:
            time.sleep(0.1)
            continue
    except:
        time.sleep(0.1)        
        break