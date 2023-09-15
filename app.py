from fastapi import FastAPI, Body
import threading
import time
import requests
import socket

app = FastAPI()

# グローバル変数を使用してスレッドの制御を行う
should_send_packet = False

def get_local_ip():
    """
    現在のローカルIPアドレスを取得する。
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # ループバックアドレスを使用しないため、大きなアドレスに接続します。
        # これにより、適切なネットワークインタフェースが選択されます。
        s.connect(("10.255.255.255", 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

def load_settings():
    with open("setting.txt", "r") as file:
        ip_address = file.readline().strip()  # 一行目: IPアドレス
        auth_info = file.readline().strip()  # 二行目: 認証情報
    return ip_address, auth_info

# 初回起動時に設定を読み込む
ip_address, auth_info = load_settings()

def send_packet(ip, auth):

    header = {
        "Accept":"*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ja,en-US;q=0.9,en;q=0.8",
        "Authorization": "Basic YWRtaW46cGFzc3dvcmQ=",
        "Connection": "keep-alive",
        "Cookie": "PHPSESSID={auth}",
        "Host": ip,
        "Referer": "http://{ip}/cw/send",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    err = 0
    while should_send_packet:
        try:
            r = requests.get('http://{ip}/api/v1/cw/send?length=2000',headers=header,timeout=((1,1)))
            print(r,int(time.time()),r.text)
            #time.sleep(0.1)
        except:
            if KeyboardInterrupt:
                print(err)
                exit()
            else:
                print("errored",int(time.time()))
                err += 1

@app.post("/change_setting")
def change_setting(new_ip: str = Body(...), new_auth: str = Body(...)):
    global ip_address, auth_info
    ip_address = new_ip
    auth_info = new_auth
    
    # setting.txt を更新
    with open("setting.txt", "w") as file:
        file.write(f"{new_ip}\n{new_auth}")
    return {"status": "Settings updated successfully."}

@app.get("/start")
def start():
    global should_send_packet
    if not should_send_packet:
        should_send_packet = True
        thread = threading.Thread(target=send_packet, args=(ip_address, auth_info))
        thread.start()
    return {"status": "Started sending packets."}

@app.get("/finish")
def finish():
    global should_send_packet
    should_send_packet = False
    return {"status": "Stopped sending packets."}

if __name__ == "__main__":
    import uvicorn
    local_ip = get_local_ip()
    print(f"Your current local IP address is: {local_ip}")
    uvicorn.run(app, host="0.0.0.0", port=8000)
