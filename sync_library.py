import os
import json
import requests
import re
import uuid
# 引入环境变量读取模块
from dotenv import load_dotenv, find_dotenv

# ==========================================
# 👑 妃爱的绝对防御：从 .env 保险箱中读取密钥
# ==========================================
load_dotenv(find_dotenv())

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

# 严谨的熔断检测：如果读不到密码，立刻停止并警告！
if not NOTION_TOKEN or not DATABASE_ID:
    print("❌ 致命错误：在 .env 文件中未找到 Notion 密钥！请检查！")
    exit()
POSTS_DIR = "source/_posts/library"
JSON_PATH = "source/library.json"
CONTENT_MARKER = "<!-- 📝 欧尼酱的专属正文从下方开始，请勿删除此行 -->"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def safe_extract(prop):
    if not prop: return ""
    ptype = prop.get("type")
    try:
        if ptype == "title": return prop["title"][0]["plain_text"] if prop["title"] else ""
        if ptype == "rich_text": return prop["rich_text"][0]["plain_text"] if prop["rich_text"] else ""
        if ptype == "number": return prop["number"] if prop["number"] is not None else ""
        if ptype == "select": return prop["select"]["name"] if prop["select"] else ""
        if ptype == "multi_select": return [x["name"] for x in prop["multi_select"]]
        if ptype == "date": return prop["date"]["start"] if prop["date"] else ""
        if ptype == "url": return prop["url"] if prop["url"] else ""
        if ptype == "files": 
            if not prop["files"]: return ""
            return prop["files"][0].get("file", {}).get("url") or prop["files"][0].get("external", {}).get("url", "")
        if ptype == "formula":
            form_type = prop["formula"].get("type")
            return prop["formula"].get(form_type) if form_type else ""
        if ptype == "status": return prop["status"]["name"] if prop["status"] else ""
    except Exception:
        return ""
    return ""

def fetch_and_build():
    print("🚀 妃爱执行绝对复刻与全量小字排版协议！")
    os.makedirs(POSTS_DIR, exist_ok=True)
    
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    results, has_more, next_cursor = [], True, None
    
    while has_more:
        payload = {"start_cursor": next_cursor} if next_cursor else {}
        res = requests.post(url, headers=HEADERS, json=payload).json()
        results.extend(res.get("results", []))
        has_more = res.get("has_more", False)
        next_cursor = res.get("next_cursor")

    library_list = []

    for page in results:
        props = page["properties"]
        
        col1_name = safe_extract(props.get("名称", {}))
        if not col1_name: continue
        col2_cover = safe_extract(props.get("封面", {}))
        col3_author = safe_extract(props.get("作者/主演", {}))
        col4_status = safe_extract(props.get("状态", {}))
        col5_publisher = safe_extract(props.get("发行/导演", {}))
        col6_category = safe_extract(props.get("类别", {}))
        col7_sub = safe_extract(props.get("目次", {}))
        col8_tags = safe_extract(props.get("细化标签", {}))
        if not isinstance(col8_tags, list): col8_tags = [col8_tags] if col8_tags else []
        col9_synopsis = safe_extract(props.get("简介", {}))
        col10_score_pub = safe_extract(props.get("大众评分", {}))
        col11_score_my = safe_extract(props.get("我的评分", {}))
        col12_review = safe_extract(props.get("简评/箴言", {}))
        col13_year = safe_extract(props.get("年份", {}))
        col14_dl = safe_extract(props.get("资源下载", {}))
        col15_date = safe_extract(props.get("时间", {}))
        col16_duration = safe_extract(props.get("时长", {}))
        col17_backlink = safe_extract(props.get("双向链接", {}))
        # 🌟 妃爱补丁：新增语言字段提取
        col18_language = safe_extract(props.get("语言", {})) 
        
        r1 = float(safe_extract(props.get("维度_文笔/画面", {})) or 0)
        r2 = float(safe_extract(props.get("维度_人设/设定", {})) or 0)
        r3 = float(safe_extract(props.get("维度_情节/结构", {})) or 0)
        r4 = float(safe_extract(props.get("维度_内涵", {})) or 0)
        r5 = float(safe_extract(props.get("维度_情感/氛围", {})) or 0)

        safe_filename = re.sub(r'[\\/:*?"<>|]', '-', col1_name).strip()
        post_link = f"/library/{safe_filename}/"
        
        library_list.append({
            "col1": col1_name, "col2": col2_cover, "col3": col3_author, "col4": col4_status,
            "col5": col5_publisher, "col6": col6_category, "col7": col7_sub, "col8": col8_tags,
            "col9": col9_synopsis, "col10": col10_score_pub, "col11": col11_score_my,
            "col12": col12_review, "col13": col13_year, "col14": col14_dl, "col15": col15_date,
            "col16": col16_duration, "col17": col17_backlink, "col18": col18_language, # 🌟 注入 JSON
            "r1": r1, "r2": r2, "r3": r3, "r4": r4, "r5": r5, "link": post_link
        })
        
        tags_yaml = "[" + ", ".join([f'"{t}"' for t in col8_tags]) + "]"
        tags_display = ", ".join(col8_tags) if col8_tags else "无"
        chart_id = f"c_{uuid.uuid4().hex[:6]}"
        
        radar_script = f"""
{{% raw %}}
<div id="{chart_id}" style="width:100%;height:350px;margin:20px 0;"></div>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
<script>
  setTimeout(function(){{
    var d = document.getElementById('{chart_id}');
    if(d) {{
      var m = echarts.init(d);
      m.setOption({{
        tooltip: {{}},
        radar: {{ indicator: [{{name:'文笔/画面',max:10}},{{name:'人设/设定',max:10}},{{name:'情节/结构',max:10}},{{name:'内涵',max:10}},{{name:'情感/氛围',max:10}}] }},
        series: [{{ type:'radar', data:[{{value:[{r1},{r2},{r3},{r4},{r5}],name:'五维数据',areaStyle:{{color:'rgba(64,158,255,0.4)'}},itemStyle:{{color:'#409EFF'}}}}] }}]
      }});
    }}
  }}, 500);
</script>
{{% endraw %}}
"""

        # 🌟 妃爱补丁：在详情页的 Markdown 中加入“语言”展示
        header_content = f"""---
title: {col1_name}
date: {page.get("created_time")}
permalink: {post_link}
categories: ["{col6_category}"]
tags: {tags_yaml}
cover: "{col2_cover}"
---

> [!info]- 📊 22维赛博档案全览 (点击折叠/展开)
> <div style="font-size: 0.85em; color: #555; line-height: 1.8; margin-top: 10px;">
> <b>名称：</b> {col1_name} <br>
> <b>作者/主演：</b> {col3_author} | <b>发行/导演：</b> {col5_publisher} <br>
> <b>状态：</b> {col4_status} | <b>年份：</b> {col13_year} | <b>语言：</b> {col18_language} <br>
> <b>类别：</b> {col6_category} | <b>目次：</b> {col7_sub} | <b>标签：</b> {tags_display} <br>
> <b>大众评分：</b> {col10_score_pub} | <b>👑 我的评分：</b> <span style="color:#409EFF; font-weight:bold;">{col11_score_my}</span> <br>
> <b>时间：</b> {col15_date} | <b>时长：</b> {col16_duration} <br>
> <b>简介：</b> {col9_synopsis} <br>
> <b>箴言：</b> <i style="color:#444;">{col12_review}</i> <br>
> <b>下载：</b> <a href="{col14_dl}" target="_blank">{col14_dl}</a> <br>
> <b>双向链接：</b> {col17_backlink} <br>
> <b>五维原始数据：</b> 文笔({r1}) · 人设({r2}) · 情节({r3}) · 内涵({r4}) · 情感({r5})
> </div>

{radar_script}

{CONTENT_MARKER}"""

        md_filepath = os.path.join(POSTS_DIR, f"{safe_filename}.md")
        user_content = "\n\n"
        
        if os.path.exists(md_filepath):
            with open(md_filepath, "r", encoding="utf-8") as f:
                old_content = f.read()
            if CONTENT_MARKER in old_content:
                user_content = old_content.split(CONTENT_MARKER, 1)[1]
            else:
                user_content = "\n\n" + old_content
                
        with open(md_filepath, "w", encoding="utf-8") as f:
            f.write(header_content + user_content)
            
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(library_list, f, ensure_ascii=False, indent=2)
        
    print(f"✨ 引擎熄火！包含全量小字列表的最终形态已生成！")

if __name__ == "__main__":
    fetch_and_build()