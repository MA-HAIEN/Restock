import json, os, urllib.request

URL = "https://jumpshop-benelic.com/collections/all/products/18051836"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]
TOPIC = os.environ["NTFY_TOPIC"]

def notify(msg):
    try:
        urllib.request.urlopen(urllib.request.Request(WEBHOOK,
            data=json.dumps({"content": msg}).encode(),
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}), timeout=15)
    except Exception as e:
        print("DC 失敗:", e)
    try:
        urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + TOPIC,
            data=msg.encode("utf-8"), headers={"Priority": "5"}), timeout=15)
    except Exception as e:
        print("ntfy 失敗:", e)

req = urllib.request.Request(URL + ".js", headers={"User-Agent": "Mozilla/5.0"})
ok = json.loads(urllib.request.urlopen(req, timeout=15).read()).get("available", False)
print("有貨" if ok else "缺貨")

prev = open("state.txt").read().strip() if os.path.exists("state.txt") else "false"

if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
    notify("✅ GitHub 測試：雲端監控正常運作中（目前" + ("有貨" if ok else "缺貨") + "）")

if ok and prev != "true":
    notify("@everyone 🎉【GitHub】獵人數據卡補貨了！快去買：\n" + URL)

open("state.txt", "w").write("true" if ok else "false")
