# racing_drone_project
with Tello

***
## with_tellopy/control_and_save_log.py update 완료
***


## 1. keyboard_control.py

tello 드론을 키보드로 조종하는 프로그램.

tellopy, easytello등 라이브러리 사용하지 않고, tello SDK 1.3.0만을 사용해서 구현.

한계 : tello SDK에서는 안정성을 위해 앞의 명령이 끝나야 다음 명령 수행 가능
      ex) 전진하다가 회전을 하고 싶어도, 전진이 다 끝나고 회전 가능

## 2. manual.png

keyboard_control.py에서 사용되는 사용자 메뉴얼 정보
<img width="716" alt="manual" src="https://user-images.githubusercontent.com/46870741/66770267-27476f00-eef2-11e9-8ec0-f70e7551b052.png">


## 3. with_tellopy/control_and_save_log.py

tellopy 라이브러리를 사용하여, 보다 더 간단하고 직관적으로 구현.
라이브러리에서 통신 패킷을 생성해서 보내기 때문에, 즉각적인 명령 수행가능.
log 저장 가능.
ex) 전진하다가 회전하는 등 조종다운 조종이 가능

## 4. control_map.png

tellopy/control_and_save_log.py에서 사용되는 사용자 메뉴얼 정보
<img width="1172" alt="control_map" src="https://user-images.githubusercontent.com/46870741/66770259-2282bb00-eef2-11e9-8a9d-db92392f2164.png">
