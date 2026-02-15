import os
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
print(f"🔍 1. 物理雷达扫描 .env 路径: '{env_path}'")

load_dotenv(env_path)
print(f"🔑 2. 保险箱内 Token 状态: '{os.getenv('NOTION_TOKEN')}'")