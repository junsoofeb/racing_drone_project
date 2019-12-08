import setup_path 
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)

state = client.getMultirotorState()
s = pprint.pformat(state)
print("-----------------------------------------------------")
print("현재 state: %s" % s)

imu_data = client.getImuData()
s = pprint.pformat(imu_data)
print("imu_data: %s" % s)

#barometer_data = client.getBarometerData()
#s = pprint.pformat(barometer_data)
#print("barometer_data: %s" % s)

#magnetometer_data = client.getMagnetometerData()
#s = pprint.pformat(magnetometer_data)
#print("magnetometer_data: %s" % s)

gps_data = client.getGpsData()
s = pprint.pformat(gps_data)
print("gps_data: %s" % s)

print('이륙하려면 "s"를 누르세요!')
#airsim.wait_key('이륙하려면 "s"를 누르세요!')
client.takeoffAsync().join()


state = client.getMultirotorState()
print("-----------------------------------------------------")
print("현재 state: %s" % pprint.pformat(state))

print('"w"을 누르면 드론이 5 m/s 로 전진합니다.  (10, 0, 0) ')
#airsim.wait_key('"w"을 누르면 드론이 5 m/s 로 전진합니다.  (10, 0, 0) ')
client.moveToPositionAsync(10, 0, 0, 5).join()


state = client.getMultirotorState()
print("-----------------------------------------------------")
print("현재 state: %s" % pprint.pformat(state))

print('"a"을 누르면 드론이 5 m/s 로 오른쪽으로 이동합니다.  (0, 10, 0) ')
#airsim.wait_key('"a"을 누르면 드론이 5 m/s 로 오른쪽으로 이동합니다.  (0, 10, 0) ')
client.moveToPositionAsync(0, 10, 0, 5).join()


state = client.getMultirotorState()
print("-----------------------------------------------------")
print("현재 state: %s" % pprint.pformat(state))


print('"w"을 누르면 드론이 5 m/s 로 전진합니다.  (10, 0, 0) ')
#airsim.wait_key('"d"을 누르면 드론이 5 m/s 로 왼쪽으로 이동합니다.  (0, -10, 0) ')
client.moveToPositionAsync(0, -10, -0, 5).join()


state = client.getMultirotorState()
print("-----------------------------------------------------")
print("현재 state: %s" % pprint.pformat(state))


client.hoverAsync().join()

#state = client.getMultirotorState()
#print("state: %s" % pprint.pformat(state))


print('"c"를 눌러서 드론으로 영상을 촬영합니다.')
#airsim.wait_key('"c"를 눌러서 드론으로 영상을 촬영합니다.')
# get camera images from the car
responses = client.simGetImages([
    airsim.ImageRequest("0", airsim.ImageType.DepthVis),  #depth visualization image
    airsim.ImageRequest("1", airsim.ImageType.DepthPerspective, True), #depth in perspective projection
    airsim.ImageRequest("1", airsim.ImageType.Scene), #scene vision image in png format
    airsim.ImageRequest("1", airsim.ImageType.Scene, False, False)])  #scene vision image in uncompressed RGBA array
print('Retrieved images: %d' % len(responses))

tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_drone")
print ("촬영된 이미지가 %s 에 저장되었습니다." % tmp_dir)
try:
    os.makedirs(tmp_dir)
except OSError:
    if not os.path.isdir(tmp_dir):
        raise

for idx, response in enumerate(responses):

    filename = os.path.join(tmp_dir, str(idx))

    if response.pixels_as_float:
        print("Type %d, size %d" % (response.image_type, len(response.image_data_float)))
        airsim.write_pfm(os.path.normpath(filename + '.pfm'), airsim.get_pfm_array(response))
    elif response.compress: #png format
        print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
        airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)
    else: #uncompressed array
        print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
        img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8) # get numpy array
        img_rgb = img1d.reshape(response.height, response.width, 3) # reshape array to 4 channel image array H X W X 3
        cv2.imwrite(os.path.normpath(filename + '.png'), img_rgb) # write to png

print('"q"를 눌러서 드론을 원상태로 되돌립니다.')
#airsim.wait_key('"q"를 눌러서 드론을 원상태로 되돌립니다.')

client.armDisarm(False)
client.reset()

# that's enough fun for now. let's quit cleanly
client.enableApiControl(False)
