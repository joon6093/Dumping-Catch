import requests
import json
import time
import os
import pytz
import datetime
from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus, unquote
from urllib2 import Request, urlopen
from urllib import urlencode, quote_plus, unquote

# 환경 변수로 설정된 API 키와 액세스 토큰을 읽습니다.
service_key = os.environ.get('SERVICE_KEY')
accessToken = os.environ.get('ACCESS_TOKEN')

# 텍스트를 음성으로 변환하는 함수입니다.
def text_speak(text):
    os.system("espeak -v ko " + text)

# API를 호출하고 검색된 텍스트를 읽어주는 함수입니다.
def API(text):
    url = 'http://apis.data.go.kr/5690000/sjLargeWaste/sj_00000260'
    params = {'serviceKey': service_key, 'pageIndex': '1', 'pageUnit': '20', 'dataTy': 'json', 'searchCondition': 'tkawy_Dw', 'searchKeyword': '수'}

    response = requests.get(url, params=params)
    song = json.loads(response.content)

    list = []
    for emd in song[u'body'][u'items']:
        list.append(emd[u'emd'])

    for i in range(0, int(len(list))):
        text_speak(list[i])
    time.sleep(1)

# API에 사용할 날짜를 가져오는 함수입니다.
def get_api_date():
    standard_time = [2, 5, 8, 11, 14, 17, 20, 23]
    time_now = datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%H')
    check_time = int(time_now) - 1
    day_calibrate = 0
    while not check_time in standard_time:
        check_time -= 1
        if check_time < 2:
            day_calibrate = 1
            check_time = 23

    date_now = datetime.now(tz=pytz.timezone('Asia/Seoul')).strftime('%Y%m%d')
    check_date = int(date_now) - day_calibrate

    return (str(check_date - 1), (str(check_time) + '00'))

# API에서 날씨 데이터를 가져오는 함수입니다.
def get_weather_data():
    api_date, api_time = get_api_date()
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"
    auth = service_key
    key = "serviceKey=" + auth
    date = "&base_date=" + api_date
    time = "&base_time=" + api_time
    nx = "&nx=86"
    ny = "&ny=96"
    numOfRows = "&numOfRows=100"
    code = "&dataType=JSON"
    api_url = url + key + date + time + nx + ny + numOfRows + code
    request = Request(api_url)
    request.get_method = lambda: 'GET'

    data = urlopen(request).read()
    data_json = json.loads(data)

    parsed_json = data_json['response']['body']['items']['item']

    target_date = parsed_json[0]['fcstDate']  # get date and time
    target_time = parsed_json[0]['fcstTime']

    date_calibrate = target_date  # date of TMX, TMN
    if target_time > 1300:
        date_calibrate = str(int(target_date) + 1)

    passing_data = {}
    for one_parsed in parsed_json:
        if one_parsed['fcstDate'] == target_date and one_parsed['fcstTime'] == target_time:  # get today's data
            passing_data[one_parsed['category']] = one_parsed['fcstValue']

        if one_parsed['fcstDate'] == date_calibrate and (
                one_parsed[u'category'] == 'TMX' or one_parsed['category'] == 'TMN'):  # TMX, TMN at calibrated day
            passing_data[one_parsed['category']] = one_parsed['fcstValue']

    return passing_data

# 대기질 데이터를 가져오는 함수입니다.
def dust_API():
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty'
    stationName = '4공단'

    decode_key = unquote(service_key)
    queryParams = '?' + urlencode({quote_plus('ServiceKey'): decode_key, quote_plus('stationName'): stationName,
                                   quote_plus('dataTerm'): 'DAILY', quote_plus('returnType'): 'json', quote_plus('ver'): '1.0',
                                   quote_plus('pageNo'): 1})

    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    response_body = json.loads(response_body)

    return response_body

# 메시지를 전송하는 함수입니다.
def sendText(message):
    url = 'https://notify-api.line.me/api/notify'
    payload = 'message="' + message.encode("utf-8") + '"'
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        'Authorization': "Bearer " + accessToken
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    responseJson = json.loads(((response.text).encode('utf-8')))
    return responseJson
