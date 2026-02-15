import os
import requests

print("=== 🔧 妃爱的赛博网络诊断仪 ===")
print(f"当前环境变量 HTTP_PROXY: {os.environ.get('HTTP_PROXY', '无 (裸奔状态)')}")
print(f"当前环境变量 HTTPS_PROXY: {os.environ.get('HTTPS_PROXY', '无 (裸奔状态)')}")

try:
    print("\n📡 正在越过高墙，向 Notion 核心服务器发送物理探测波...")
    # 发送一个最简单的试探请求，10秒超时
    res = requests.get("https://api.notion.com", timeout=10)
    print(f"✨ 奇迹发生！成功建立物理连接！状态码: {res.status_code}")
except Exception as e:
    print(f"\n💥 抓到赛博幽灵的真面目了！欧尼酱，请把下面这两行核心报错发给妃爱：")
    print(f"[{type(e).__name__}]")
    print(f"{e}")