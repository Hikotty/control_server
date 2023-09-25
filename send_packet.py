import requests
import time

header = {
    "Accept":"*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
    "Authorization": "Basic YWRtaW46cGFzc3dvcmQ=",
    "Connection": "keep-alive",
    "Cookie": "PHPSESSID=ggtn1ic8rnhs69lf1sf3f1srp6",
    "Host": "192.168.11.5",
    "Referer": "http://192.168.11.4/cw/send",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

err = 0
for i in range(10*60*5):
    try:
        r = requests.get('http://192.168.11.7/api/v1/cw/send?length=2000',headers=header,timeout=((1,1)))
        print(r,int(time.time()),r.text)
        #time.sleep(0.1)
    except:
        if KeyboardInterrupt:
            print(err)
            exit()
        else:
            print("errored",int(time.time()))
            err += 1