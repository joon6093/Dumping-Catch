# Flask 웹 서버 라우트
import datetime
import threading
import grovepi
import time
import os
from flask import Flask, render_template, request, Response
from hardware_control import VERTICAL_motor_doAngle, HORIZON_motor_doAngle
from api_functions import API, get_weather_data, dust_API, text_speak, sendText
from voice_text_processing import STT_fun
from math import isnan
from camera import Camera
from grovepi import *

# 하드웨어 초기화
ultrasonic_ranger = 4
buzzer_pin = 2	
dht_sensor_port = 7 
dht_sensor_type = 0 
sound_sensor=0
led=3
pir_sensor=8
pinMode(pir_sensor,"INPUT")

pinMode(led,"OUTPUT")
pinMode(buzzer_pin,"OUTPUT")	# Assign mode for buzzer as output

# 서보 모터의 미리 정의된 각도입니다.
left_angle = 12.5
center_angle = 8.5
right_angle = 5.5

app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
# 메인 Flask 라우트를 정의합니다.
@app.route("/",methods=['GET','POST'])
def main():
	try:
		digitalWrite(led,0)
		now = datetime.now()
		now_time = now.strftime("%Y/%m/%d %H:%M")
		stt=threading.Thread(target=STT_fun)
		stt.start()
		
		[ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)
		if isnan(temp) is True or isnan(hum) is True:
			raise TypeError
		t = str(temp)
		h = str(hum)
		sound_level=grovepi.analogRead(sound_sensor)
		distant = ultrasonicRead(ultrasonic_ranger)
		
		if (distant <= 5):
			digitalWrite(led,1)
			digitalWrite(buzzer_pin,1)
			time.sleep(0.1)
			digitalWrite(buzzer_pin,0)
			digitalWrite(buzzer_pin,1)
			time.sleep(0.1)
			digitalWrite(buzzer_pin,0)
			#print '누군가 전봇대에 기대고있습니다. 담당 경찰관에게 연락합니다.'
			sendText('술취한사람이있거나 사람이 굉장히 많습니다. 현장 확인 바랍니다.')
			setText_norefresh("POLICE:9321213" + now_time)
			text_speak("정신차리세요")
			
		elif (distant <= 20):
			digitalWrite(led,1)
			digitalWrite(buzzer_pin,1)
			time.sleep(0.1)
			digitalWrite(buzzer_pin,0)
			digitalWrite(buzzer_pin,1)
			time.sleep(0.1)
			digitalWrite(buzzer_pin,0)
			text_speak("불법투기멈춰종량제봉투를사용해주세요")
			setText_norefresh("POLICE:9321213" + now_time)
			
		elif (grovepi.digitalRead(pir_sensor)):
			setText_norefresh("I SEE YOU CAMERA IS ROTATE")
			digitalWrite(led,1)
			#print '카메라근처에 모션 감지'
			text_speak("다보입니다불법투기하지마세요")	
		else:
			digitalWrite(led,0)
			setText_norefresh("GOOD MORNING")
			
		weather="errror"
		if(get_weather_data()[u'SKY']=='1'):
			weather="today is Sunny"
		elif(get_weather_data()[u'SKY']=='2'):
			weather="today is Cloud"
		elif(get_weather_data()[u'SKY']=='3'):
			weather="today is a little Cloud"
		elif(get_weather_data()[u'SKY']=='4'):
			weather="today is blur"
		
		preci="errror"
		if(get_weather_data()[u'PTY']=='0'):
			preci="today is Sunny"
		elif(get_weather_data()[u'PTY']=='1'):
			preci="today is rain"
		elif(get_weather_data()[u'PTY']=='2'):
			preci="today is rain and snow"
		elif(get_weather_data()[u'PTY']=='3'):
			preci="today is snow"
		
		if (hum>90): #rain or snow
			if(temp>=0):  #rain
				setText_norefresh("weather:rain")
			else: #snow
				setText_norefresh("weather:snow")
		else:
			setText_norefresh("POLICE:9321213" + now_time)
			
		dust="error"
		if(int(dust_API()['response']['body']['items'][0]['pm25Value'])>=76):
			dust="today is fine dust very bad"
		elif(int(dust_API()['response']['body']['items'][0]['pm25Value'])>=36):
			dust="today is fine dust bad"
		elif(int(dust_API()['response']['body']['items'][0]['pm25Value'])>=15):
			dust="today is fine dust soso"
		else:
			dust="today is fine dust good"
			
		##print(sound_level)
		if(sound_level>500):
			#print '측정 된 소음이 커 담당 경찰관에게 연락합니다.'
			sendText('주변 소음이 굉장히 큽니다. 현장 확인 바랍니다.')
			text_speak("조금있으면경찰관이출동할예정입니다")
				
		if request.method=='POST':
			SPEAKER=request.form['speaker_text']
			SPEAKER_BUTTON=request.form.get('speaker_button')
			HORIZON_RIGHT_BUTTON=request.form.get('HORIZON_RIGHT')
			HORIZON_CENTER_BUTTON=request.form.get('HORIZON_CENTER')
			HORIZON_LEFT_BUTTON=request.form.get('HORIZON_LEFT')
			VERTICAL_UP_BUTTON=request.form.get('VERTICAL_UP')
			VERTICAL_CENTER_BUTTON=request.form.get('VERTICAL_CENTER')
			VERTICAL_DOWN_BUTTON=request.form.get('VERTICAL_DOWN')
			if HORIZON_RIGHT_BUTTON:
				HORIZON_motor_doAngle(right_angle)
			if HORIZON_CENTER_BUTTON:
				HORIZON_motor_doAngle(center_angle)
			if HORIZON_LEFT_BUTTON:
				HORIZON_motor_doAngle(left_angle)
			if VERTICAL_UP_BUTTON:
				VERTICAL_motor_doAngle(right_angle)
			if VERTICAL_CENTER_BUTTON:
				VERTICAL_motor_doAngle(center_angle)
			if VERTICAL_DOWN_BUTTON:
				VERTICAL_motor_doAngle(left_angle)
			if SPEAKER_BUTTON:
				text_speak(SPEAKER)	
				
		image_list=os.listdir('/home/pi/last_project/static/')
		
	except TypeError:
		#print("Error")
	except IOError:
		#print("Error")
	except KeyboardInterrupt:
		HORIZON_motor_p.cleanup()
		VERTICAL_motor_p.cleanup()
		digitalWrite(led,0)

	templateData={
	'title':'무투잡',
	'tempis':t,
	'weather':weather,
	'preci':preci,
	'hum':h,
	'dust':dust,
	'image_list':image_list
	}

	return render_template('last_project.html',**templateData)

# 비디오 피드 라우트를 정의합니다.
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
