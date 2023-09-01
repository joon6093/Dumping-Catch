#음성 및 텍스트 처리와 관련된 함수
import os
import gspeech
import threading
import time
import datetime
from hardware_control import VERTICAL_motor_doAngle, HORIZON_motor_doAngle
from api_functions import API, get_weather_data, dust_API, text_speak, sendText
from grovepi import *

# Google 음성 인식을 초기화합니다.
gsp = gspeech.Gspeech()

# 음성을 텍스트로 변환하는 함수입니다.
def STT_fun():
	while True:
		stt = gsp.getText()
		#print (stt)
		time.sleep(0.01)
		if ('쓰레기장' in stt):
			#print '바로 앞 전봇대'
			text_speak("바로앞전봇대")
			time.sleep(0.5)
		if ('월요일' in stt):
			#print '쓰레기차가 월요일에 오는 장소를 말합니다.'
			API('월')
			time.sleep(0.5)
		if ('화요일' in stt):
			#print '쓰레기차가 화요일에 오는 장소를 말합니다.'
			API('화')
			time.sleep(0.5)
		if ('수요일' in stt):
			#print '쓰레기차가 수요일에 오는 장소를 말합니다.'
			API('수')
			time.sleep(0.5)
		if ('목요일' in stt):
			#print '쓰레기차가 목요일에 오는 장소를 말합니다.'
			API('목')
			time.sleep(0.5)
		if ('금요일' in stt):
			#print '쓰레기차가 금요일에 오는 장소를 말합니다.'
			API('금')
			time.sleep(0.5)
		if ('토요일' in stt):
			#print '쓰레기차가 토요일에 오는 장소를 말합니다.'
			API('토')
			time.sleep(0.5)
		if ('일요일' in stt):
			#print '쓰레기차가 일요일에 오는 장소를 말합니다.'
			API('일')
			time.sleep(0.5)
			
		if ('카메라 위로' in stt):
			#print '카메라를 조금 더 위로 설정합니다'
			VERTICAL_motor_doAngle(right_angle)
		if ('카메라 아래로' in stt):
			#print '카메라를 조금 더 아래로 설정합니다'
			VERTICAL_motor_doAngle(left_angle)
		if ('카메라 왼쪽으로' in stt):
			#print '카메라를 조금 더 왼쪽으로 설정합니다'
			HORIZON_motor_doAngle(left_angle)
		if ('카메라 오른쪽으로' in stt):
			#print '카메라를 조금 더 오른쪽 설정합니다'
			HORIZON_motor_doAngle(right_angle)
			
		if ('살려 줘' in stt):
			#print '담당 경찰관에게 연락합니다.'
			sendText('주변 사람이 구조요청을 보냅니다')
			text_speak("곧경찰이출동합니다조금만기다리세요10분안에도착할예정입니다.")
			time.sleep(1)
			digitalWrite(buzzer_pin,1)
			time.sleep(0.1)
			digitalWrite(buzzer_pin,0)
		
		if ('쓰레기 배출 지정일' in stt):
			#print '쓰레기배출지정일을 말합니다'
			text_speak('일요일화요일목요일은종량제봉투월요일수요일은재활용품금요일토요일은배출금지')
			time.sleep(1)
			
		if ('오늘 배출' in stt):
			if(datetime.today().weekday()==1 or datetime.today().weekday()==3 or datetime.today().weekday()==6):
				text_speak('일반쓰레기배출하는날입니다일반쓰레기만버려주세요')
				time.sleep(1)
			if(datetime.today().weekday()==0 or datetime.today().weekday()==2):
				text_speak('재활용품배출하는날입니다재활용품만버려주세요')
				time.sleep(1)
			if(datetime.today().weekday()==4 or datetime.today().weekday()==5):
				text_speak('배출금지요배출하지마세요')
				time.sleep(1)
				
		if ('오늘쓰레기차' in stt):
			if (datetime.today().weekday()==1):
				#print '쓰레기차가 월요일에 오는 장소를 말합니다.'
				API('월')
			if (datetime.today().weekday()==2 in stt):
				#print '쓰레기차가 화요일에 오는 장소를 말합니다.'
				API('화')
			if (datetime.today().weekday()==3 in stt):
				#print '쓰레기차가 수요일에 오는 장소를 말합니다.'
				API('수')
			if (datetime.today().weekday()==4 in stt):
				#print '쓰레기차가 목요일에 오는 장소를 말합니다.'
				API('목')
			if (datetime.today().weekday()==5 in stt):
				#print '쓰레기차가 금요일에 오는 장소를 말합니다.'
				API('금')
			if (datetime.today().weekday()==6 in stt):
				#print '쓰레기차가 토요일에 오는 장소를 말합니다.'
				API('토')
			if (datetime.today().weekday()==7 in stt):
				#print '쓰레기차가 일요일에 오는 장소를 말합니다.'
				API('일')
		if ('오늘 날씨' in stt):
			if(get_weather_data()[u'SKY']=='1'):
				#print('오늘 날씨는 맑습니다쓰레기를 잘 버려주세요')
				text_speak('오늘날씨는맑습니다쓰레기를잘버려주세요')
				setText_norefresh("today is Sunny")
				time.sleep(1)
			elif(get_weather_data()[u'SKY']=='2'):
				#print('오늘 날씨는 구름입니다쓰레기를 잘 버려주세요')
				text_speak('오늘날씨는구름입니다쓰레기를잘버려주세요')
				setText_norefresh("today is Cloud")
				time.sleep(1)
			elif(get_weather_data()[u'SKY']=='3'):
				#print('오늘 날씨는 구름조금입니다쓰레기를 잘 버려주세요')
				text_speak('오늘날씨는구름조금입니다쓰레기를잘버려주세요')
				setText_norefresh("today is a little Cloud")
				time.sleep(1)
			elif(get_weather_data()[u'SKY']=='4'):
				#print('오늘 날씨는 흐립니다쓰레기를 잘 버려주세요')
				text_speak('오늘날씨는흐립니다쓰레기를잘버려주세요')
				setText_norefresh("today is blur")
				time.sleep(1)
			
		if ('오늘 강수' in stt):
			if(get_weather_data()[u'PTY']=='0'):
				#print('오늘강수는맑습니다쓰레기를잘버려주세요')
				text_speak('오늘강수는맑습니다쓰레기를잘버려주세요')
				setText_norefresh("today is Sunny")
				time.sleep(1)
			elif(get_weather_data()[u'PTY']=='1'):
				#print('오늘 강수는 비입니다쓰레기를 잘 버려주세요')
				text_speak('오늘강수는비입니다쓰레기를잘버려주세요')
				setText_norefresh("today is rain")
				time.sleep(1)
			elif(get_weather_data()[u'PTY']=='2'):
				#print('오늘 날씨는 비와 눈이 같이 옵니다. 쓰레기를 잘 버려주세요')
				text_speak('오늘날씨는비와눈이같이옵니다쓰레기를잘버려주세요')
				setText_norefresh("today is rain and snow")
				time.sleep(1)
			elif(get_weather_data()[u'PTY']=='3'):
				#print('오늘 날씨는 눈입니다. 쓰레기를 잘 버려주세요')
				text_speak('오늘날씨는눈입니다쓰레기를잘버려주세요')
				setText_norefresh("today is snow")
				time.sleep(1)
		
		if ('미세먼지' in stt):
			if(int(dust_API()['response']['body']['items'][0]['pm25Value'])>=76):
				#print('오늘 미세먼지는 매우나쁩니다. 쓰레기를 잘 버려주세요')
				text_speak('오늘미세먼지는매우나쁩니다쓰레기를잘버려주세요')
				setText_norefresh("today is fine dust very bad")
				time.sleep(1)
			elif(int(dust_API()['response']['body']['items'][0]['pm25Value'])>=36):
				#print('오늘미세먼지는나쁩니다쓰레기를잘버려주세요')
				text_speak('오늘 미세먼지는 나쁩니다. 쓰레기를 잘 버려주세요')
				setText_norefresh("today is fine dust bad")
				time.sleep(1)
			elif(int(dust_API()['response']['body']['items'][0]['pm25Value'])>=15):
				#print('오늘미세먼지는 보통입니다. 쓰레기를 잘 버려주세요')
				text_speak('오늘미세먼지는보통입니다쓰레기를잘버려주세요')
				setText_norefresh("today is fine dust soso")
				time.sleep(1)
			else:
				#print('오늘 미세먼지는 좋습니다. 쓰레기를 잘 버려주세요')
				text_speak('오늘미세먼지는좋습니다쓰레기를잘버려주세요')
				setText_norefresh("today is fine dust good")
				time.sleep(1)
				
		if ('재밌는 이야기' in stt):
				#print('재밌는 이야기를 들려드리겠습니다.')
				text_speak('왕이넘어지면킹콩')
				setText_norefresh("왕이넘어지면킹콩")
				time.sleep(0.5)
				
		if ('이름' in stt):
				#print('제 이름은 무투잡이에요')
				text_speak('제이름은무투잡이에요쓰레기버리는사람을잡아요')
				time.sleep(0.5)