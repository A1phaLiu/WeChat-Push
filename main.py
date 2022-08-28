from requests import get,post
import random

APPID = 'wxf5c15875f7f9cf79'
APPSECRET = '5ca058e131cfe2996c1a1ac0580a4fe1'
KEY = '2f6a0a0c89a347aca7245ac92e4f6d99'    #和风天气API
users = [{'name':'lrx',
            'user':'ospjp502g67JVKKnqQur4CJ7_Ph4',
            'city':'周至县'},
         {'name':'hjg',
            'user':'ospjp50ABcys42u1wlAPol6AvIt4',
            'city':'天河区'}
]

def get_color():
    # 获取随机颜色
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)

def get_access_token():
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={APPSECRET}'
    try:
        access_token = get(url).json()['access_token']
    except KeyError:
        print("请求token出错")
    return access_token

def get_locationID(city):
    url_geoapi = f'https://geoapi.qweather.com/v2/city/lookup?key={KEY}&location={city}&range=cn'
    locationID = get(url_geoapi).json()['location'][0]['id']
    return locationID

def get_weather(city):
    locationID = get_locationID(city)
    url_weather = f'https://devapi.qweather.com/v7/weather/now?key={KEY}&location={locationID}'
    resp = get(url=url_weather).json()['now']
    weather = resp['text']
    temp = resp['temp']
    feelsLike = resp['feelsLike']
    return weather,temp,feelsLike

def get_ciba():
    url = "http://open.iciba.com/dsapi/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    r = get(url, headers=headers)
    note_en = r.json()["content"]
    note_zh = r.json()["note"]
    return note_zh, note_en

def get_time():
    url = 'http://quan.suning.com/getSysTime.do'
    resp = get(url).json()['sysTime1']
    year,month,day = resp[0:4],resp[4:6],resp[6:8]
    return year,month,day

def send_message(user, city):
    url = f'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={accessToken}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    data = {
        "touser" : user,
        "template_id" : "8c4Kltqo-6D6c8Z7uO50kqT51m8O30wEeBa3ECC3EIw",
        "data":{
            "date":{
                "value": f"{year}年{month}月{day}日",
                "color": get_color()
            },
            "city":{
                "value": city,
                "color": get_color()
            },
            'weather':{
                'value': weather,
                "color": get_color()
            },
            'temp':{
                'value': temp,
                "color": get_color()
            },
            'feelsLike':{
                'value': feelsLike,
                "color": get_color()
            },
            'note_en':{
                'value': note_en,
                "color": get_color()
            },
            'note_zh':{
                'value': note_zh,
                "color": get_color()
            }
        }
    }
    response = post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    # 获取accessToken
    accessToken = get_access_token()
    # 获取当前日期
    year,month,day = get_time()
    # 获取词霸每日金句
    note_zh, note_en = get_ciba()

    for user in users:
        # 获取当地实时天气
        weather,temp,feelsLike = get_weather(user['city'])
        # 公众号推送消息
        send_message(user['user'],user['city'])