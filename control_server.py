from fastapi import FastAPI
import threading
import time
import requests

app = FastAPI()

# グローバル変数を使用してスレッドの制御を行う
should_send_packet = False

def send_packet():
    target_endpoint = "http://example.com/target_endpoint"  # このURLは実際のターゲットエンドポイントに変更してください。
    
    while should_send_packet:
        # ここでパケット送信の処理を行います。
        requests.post(target_endpoint, data={"key": "value"})  # これはサンプルです。
        time.sleep(1)  # 1秒ごとにパケットを送信します。

@app.get("/start")
def start():
    global should_send_packet
    if not should_send_packet:
        should_send_packet = True
        thread = threading.Thread(target=send_packet)
        thread.start()
    return {"status": "Started sending packets."}

@app.get("/finish")
def finish():
    global should_send_packet
    should_send_packet = False
    return {"status": "Stopped sending packets."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
