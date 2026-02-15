import os
import time
import requests
import json
import uuid
from io import BytesIO
from datetime import datetime, timezone, timedelta
from PIL import Image
import re
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# 🛡️ 妃爱的极客终极武装：抛弃系统，强行绑定梯子真实端口！
# 👇 欧尼酱！请把下面的 7897 换成你刚才在软件里看到的真实端口数字！
PROXY_PORT = "62686"  

os.environ['HTTP_PROXY'] = f"http://127.0.0.1:{PROXY_PORT}"
os.environ['HTTPS_PROXY'] = f"http://127.0.0.1:{PROXY_PORT}"
os.environ['ALL_PROXY'] = f"socks5://127.0.0.1:{PROXY_PORT}"

print(f"🔗 妃爱已强行将引擎接管至代理端口: {PROXY_PORT}")

# 👑 加载欧尼酱的赛博密钥库
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
print(f"🕵️ 侦测 Token 状态: {NOTION_TOKEN}")
DATABASE_ID = os.getenv("DATABASE_ID")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BANGUMI_USERNAME = os.getenv("BANGUMI_USERNAME")
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_IDS = [sid.strip() for sid in os.getenv("STEAM_IDS", "").split(",")] if os.getenv("STEAM_IDS") else []

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_PUBLIC_DOMAIN = os.getenv("R2_PUBLIC_DOMAIN", "").rstrip("/")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# 🌌 绝对时空锚点 (东八区：新加坡/北京时间)
TZ_8 = timezone(timedelta(hours=8))

# ==========================================
# 🛡️ 极客柔术：Notion API 抗熔断请求包装器
# ==========================================
def safe_notion_request(method, url, json_data=None):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            res = requests.request(method, url, headers=HEADERS, json=json_data, timeout=15)
            if res.status_code == 429:
                sleep_time = 2 ** attempt
                print(f"    ⚠️ 触发 Notion 限流，退避休眠 {sleep_time} 秒...")
                time.sleep(sleep_time)
                continue
            return res
        except requests.exceptions.RequestException as e:
            print(f"    ⚠️ 网络波动 ({e})，正在重试...")
            time.sleep(2)
    return None

# ==========================================
# 🖼️ R2 图像压缩直传引擎
# ==========================================
def upload_cover_to_r2(image_url, item_id):
    if not image_url or not R2_ACCOUNT_ID: return image_url
    print("    🎨 启动 R2 图像引擎，开始压缩与直传...")
    try:
        s3 = boto3.client('s3',
            endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
            aws_access_key_id=os.getenv("R2_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("R2_SECRET_KEY"),
            region_name="auto"
        )
        
        res = requests.get(image_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        if res.status_code != 200: return image_url
        
        img = Image.open(BytesIO(res.content))
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        
        webp_buffer = BytesIO()
        img.save(webp_buffer, format="WEBP", quality=85)
        webp_buffer.seek(0)
        
        file_key = f"covers/cov_{item_id}_{uuid.uuid4().hex[:6]}.webp"
        s3.put_object(Bucket=R2_BUCKET_NAME, Key=file_key, Body=webp_buffer, ContentType='image/webp')
        
        final_url = f"{R2_PUBLIC_DOMAIN}/{file_key}"
        print(f"    ✨ R2 转化成功: {final_url}")
        return final_url
    except Exception as e:
        print(f"    ❌ R2 处理失败 ({e})，降级使用原图链接。")
        return image_url

# ==========================================
# 📡 三大平台探测器 (全量榨取版)
# ==========================================
def fetch_bangumi_full(bgm_id):
    result = {}
    res = requests.get(f"https://api.bgm.tv/v0/subjects/{bgm_id}", headers={'User-Agent': 'sandleft/auto-sync'}, timeout=10)
    if res.status_code != 200: return None
    data = res.json()
    
    # --- 请在这个位置插入以下代码 ---
    language_name = ""
    for info in data.get("infobox", []):
        if info.get("key") in ["语言", "语种"]:
            language_name = info.get("value", "")
            break
            
    result.update({
        "title": data.get("name_cn") or data.get("name"),
        "cover_raw": data.get("images", {}).get("large", ""),
        "summary": (data.get("summary") or "")[:2000],
        "score_public": data.get("rating", {}).get("score", 0),
        "year": data.get("date", "")[:4] if data.get("date") else "",
        "language": language_name # 👈 新增这一行！
    })

    if BANGUMI_USERNAME:
        res_user = requests.get(f"https://api.bgm.tv/v0/users/{BANGUMI_USERNAME}/collections/{bgm_id}", headers={'User-Agent': 'sandleft/auto-sync'}, timeout=10)
        if res_user.status_code == 200:
            ud = res_user.json()
            result["score_geek"] = ud.get("rate", 0)
            result["review"] = ud.get("comment", "")
            result["tags"] = ud.get("tags", [])
            status_map = {1: "想看", 2: "已完成", 3: "进行中", 4: "搁置", 5: "抛弃"}
            result["status"] = status_map.get(ud.get("type"), "")
            if ud.get("updated_at"):
                result["play_date"] = ud.get("updated_at").split("T")[0]
    return result

def fetch_steam_full(app_id):
    result = {}
    res_info = requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}&l=schinese", timeout=10)
    if res_info.status_code != 200: return None
    data = res_info.json()
    if not (data and str(app_id) in data and data[str(app_id)].get("success")): return None
    
    game_data = data[str(app_id)]["data"]
    
    # 提取开发者与发行商填入22列表格
    devs = ", ".join(game_data.get("developers", []))
    pubs = ", ".join(game_data.get("publishers", []))
    
    # --- 请在这个位置插入以下代码 ---
    raw_lang = game_data.get("supported_languages", "")
    clean_lang = re.sub(r'<[^>]+>', '', raw_lang) # 极客斩：切碎所有 HTML 标签
    lang_list = [l.strip() for l in clean_lang.split(',')]
    language_name = ", ".join(lang_list[:3]) if lang_list else "" # 只取前3种语言，防止表格塞爆
    
    result.update({
        "title": game_data.get("name"),
        "cover_raw": game_data.get("header_image", "").split("?")[0],
        "summary": (game_data.get("short_description") or "")[:2000],
        "year": game_data.get("release_date", {}).get("date", "")[-4:] if game_data.get("release_date") else "",
        "author": devs[:50],  
        "publisher": pubs[:50], 
        "language": language_name # 👈 新增这一行！
    })
    
    res_reviews = requests.get(f"https://store.steampowered.com/appreviews/{app_id}?json=1&language=all&purchase_type=all", timeout=10)
    if res_reviews.status_code == 200:
        rev = res_reviews.json().get("query_summary", {})
        if rev.get("total_reviews", 0) > 0:
            result["score_public"] = round((rev["total_positive"] / rev["total_reviews"]) * 10, 1)
            result["steam_review_desc"] = rev.get("review_score_desc", "")

    if STEAM_API_KEY and STEAM_IDS:
        for sid in STEAM_IDS:
            res_play = requests.get(f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={STEAM_API_KEY}&steamid={sid}&format=json", timeout=10)
            if res_play.status_code == 200:
                games = res_play.json().get("response", {}).get("games", [])
                target_game = next((g for g in games if str(g.get("appid")) == str(app_id)), None)
                if target_game:
                    playtime_hours = round(target_game.get("playtime_forever", 0) / 60, 1)
                    result["time_spent"] = f"{playtime_hours} 小时"
                    
                    last_played_unix = target_game.get("rtime_last_played", 0)
                    if last_played_unix > 0:
                        # 强制使用东八区时间，杜绝云端部署时的时区漂移！
                        result["play_date"] = datetime.fromtimestamp(last_played_unix, TZ_8).strftime('%Y-%m-%d')
                    print(f"    🎮 截获 Steam 时长 (账号尾号 {sid[-4:]}): {playtime_hours} 小时")
                    break
    return result

def fetch_tmdb(tmdb_id, media_type="movie"):
    # 额外抓取 credits 演职员表
    url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}&language=zh-CN&append_to_response=credits"
    res = requests.get(url, timeout=10)
    if res.status_code != 200: return None
    data = res.json()
    
    date_key = "release_date" if media_type == "movie" else "first_air_date"
    poster = data.get("poster_path")
    
    # 解析导演与第一主演
    crew = data.get("credits", {}).get("crew", [])
    director = next((c["name"] for c in crew if c["job"] == "Director"), "")
    cast = data.get("credits", {}).get("cast", [])
    main_actor = cast[0]["name"] if cast else ""

    # --- 请在这个位置插入以下代码 ---
    lang_map = {'en': '英语', 'ja': '日语', 'zh': '汉语', 'ko': '韩语', 'fr': '法语', 'de': '德语', 'ru': '俄语'}
    orig_lang = data.get("original_language", "")
    language_name = lang_map.get(orig_lang, orig_lang.upper())
    
    return {
        "title": data.get("title") if media_type == "movie" else data.get("name"),
        "cover_raw": f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{poster}" if poster else "",
        "summary": (data.get("overview") or "")[:2000],
        "score_public": round(data.get("vote_average", 0), 1),
        "year": data.get(date_key, "")[:4] if data.get(date_key) else "",
        "author": main_actor[:50], 
        "publisher": director[:50],
        "language": language_name # 👈 新增这一行！
    }
    
# ==========================================
# 🧠 核心架构：游标分页与数据组装
# ==========================================
def run_auto_fill():
    print("🚀 妃爱的 R2 直传 & 万象引力引擎 3.1 (终极完整版) 启动！")
    
    query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    filter_data = {
        "filter": {
            "and": [
                { "property": "采集ID", "rich_text": { "is_not_empty": True } },
                { "property": "类别", "select": { "is_not_empty": True } },
                {
                    "or": [
                        { "property": "简介", "rich_text": { "is_empty": True } },
                        { "property": "强制刷新", "checkbox": { "equals": True } }
                    ]
                }
            ]
        }
    }
    
    pages, has_more, next_cursor = [], True, None
    while has_more:
        payload = filter_data.copy()
        if next_cursor: payload["start_cursor"] = next_cursor
        res = safe_notion_request("POST", query_url, json_data=payload)
        if not res or res.status_code != 200:
            print(f"❌ 读取 Notion 失败！状态码: {res.status_code if res else '网络物理断开'}, 详情: {res.text if res else '无'}")
            return
        data = res.json()
        pages.extend(data.get("results", []))
        has_more = data.get("has_more", False)
        next_cursor = data.get("next_cursor")

    if not pages:
        print("✅ 扫描完毕！暂无需要处理的档案。")
        return

    print(f"🎯 共锁定 {len(pages)} 条待处理档案，开始作业...")

    for page in pages:
        page_id = page["id"]
        props = page["properties"]
        
        item_id = props["采集ID"]["rich_text"][0]["plain_text"].strip()
        category = props["类别"]["select"]["name"].strip()
        is_force_refresh = props.get("强制刷新", {}).get("checkbox", False)
        
        print(f"\n[{category}] ID: {item_id} {'(强制刷新)' if is_force_refresh else ''}")
        
        fetched_data = None
        try:
            if category in ["动画", "漫画", "galgame", "图书", "动漫"]: fetched_data = fetch_bangumi_full(item_id)
            elif category == "电影": fetched_data = fetch_tmdb(item_id, "movie")
            elif category in ["电视剧", "日剧", "美剧"]: fetched_data = fetch_tmdb(item_id, "tv")
            elif category in ["游戏", "单机游戏"]: fetched_data = fetch_steam_full(item_id)
            else: continue
        except Exception as e:
            print(f"    ❌ 探测异常: {e}")
            continue

        if not fetched_data:
            print("    ❌ 探测器空手而归。")
            continue
            
        final_cover_url = upload_cover_to_r2(fetched_data.get("cover_raw"), item_id)
        update_props = { "properties": {} }
        
        # 基础校验与写入
        if not props.get("名称", {}).get("title") and fetched_data.get("title"):
            update_props["properties"]["名称"] = {"title": [{"text": {"content": fetched_data["title"]}}]}
            
        if final_cover_url: update_props["properties"]["封面"] = {"url": final_cover_url}
        if fetched_data.get("summary"): update_props["properties"]["简介"] = {"rich_text": [{"text": {"content": fetched_data["summary"]}}]}
        if fetched_data.get("year"): update_props["properties"]["年份"] = {"rich_text": [{"text": {"content": fetched_data["year"]}}]}
        if fetched_data.get("score_public", 0) > 0: update_props["properties"]["大众评分"] = {"number": fetched_data["score_public"]}
        # 把这段加在属性赋值的区域里
        if fetched_data.get("language") and not props.get("语言", {}).get("rich_text"): 
            update_props["properties"]["语言"] = {"rich_text": [{"text": {"content": fetched_data["language"]}}]}
        
        # 主创元数据补全 (充分利用 22 列)
        if fetched_data.get("author") and not props.get("作者/主演", {}).get("rich_text"): 
            update_props["properties"]["作者/主演"] = {"rich_text": [{"text": {"content": fetched_data["author"]}}]}
        if fetched_data.get("publisher") and not props.get("发行/导演", {}).get("rich_text"): 
            update_props["properties"]["发行/导演"] = {"rich_text": [{"text": {"content": fetched_data["publisher"]}}]}

        # 私人数据写入
        if fetched_data.get("score_geek", 0) > 0: update_props["properties"]["我的评分"] = {"number": fetched_data["score_geek"]}
        if fetched_data.get("review"): update_props["properties"]["简评/箴言"] = {"rich_text": [{"text": {"content": fetched_data["review"]}}]}
        if fetched_data.get("status"): update_props["properties"]["状态"] = {"select": {"name": fetched_data["status"]}}
        if fetched_data.get("time_spent"): update_props["properties"]["时长"] = {"rich_text": [{"text": {"content": fetched_data["time_spent"]}}]}
        
        # 标签清洗：严格剔除逗号与空值
        if fetched_data.get("tags"): 
            clean_tags = [str(t).replace(",", "-").strip()[:20] for t in fetched_data["tags"] if str(t).strip()]
            update_props["properties"]["细化标签"] = {"multi_select": [{"name": t} for t in clean_tags[:10]]}
            
        if fetched_data.get("play_date"): 
            update_props["properties"]["时间"] = {"date": {"start": fetched_data["play_date"]}}

        update_props["properties"]["强制刷新"] = {"checkbox": False}

        # 提交到 Notion
        res = safe_notion_request("PATCH", f"https://api.notion.com/v1/pages/{page_id}", json_data=update_props)
        if res and res.status_code == 200:
            print(f"    ✨ 完美归档！《{fetched_data.get('title')}》入库。")
            
            # 增量追加 Steam 好评率块
            steam_desc = fetched_data.get("steam_review_desc")
            if steam_desc and not is_force_refresh:
                block_data = {
                    "children": [{
                        "object": "block",
                        "type": "callout",
                        "callout": {
                            "rich_text": [{"type": "text", "text": {"content": f"Steam 真实受众反馈：【{steam_desc}】({fetched_data.get('score_public')} 分)。"}}],
                            "icon": {"type": "emoji", "emoji": "👾"}
                        }
                    }]
                }
                safe_notion_request("PATCH", f"https://api.notion.com/v1/blocks/{page_id}/children", json_data=block_data)
        else:
            print(f"    ❌ Notion 注入失败: {res.text if res else 'Timeout'}")
            
        time.sleep(1)

if __name__ == "__main__":
    run_auto_fill()