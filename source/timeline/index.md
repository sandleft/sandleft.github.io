---
title: 动态线
date: 2026-02-14 10:30:00
type: "timeline"
aside: false
---

<link rel="stylesheet" href="https://npm.elemecdn.com/lxgw-wenkai-screen-webfont/style.css" media="print" onload="this.media='all'">
<style>
  #memos-timeline {
    max-width: 800px;
    margin: 0 auto;
    font-family: "LXGW WenKai Screen", sans-serif; /* 注入清雅的落笔感 */
  }
  .memo-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 24px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    border-left: 4px solid #8e8e8e; /* 沉稳的灰边，区分不同的思绪碎片 */
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  .memo-card:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  }
  .memo-time {
    font-size: 0.85em;
    color: #999;
    margin-bottom: 16px;
    border-bottom: 1px dashed #f0f0f0;
    padding-bottom: 8px;
    letter-spacing: 0.5px;
  }
  .memo-content {
    font-size: 1.05em;
    line-height: 1.8;
    color: #333;
  }
  .memo-content img {
    max-width: 100%;
    border-radius: 8px;
    margin-top: 12px;
  }
  .memo-content p { margin: 0 0 10px 0; }
  .loading-text { text-align: center; color: #999; padding: 40px 0; font-style: italic; }
</style>

<div id="memos-timeline">
  <div class="loading-text">正在从云端金库抽取灵光瞬间...</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<script>
  // 【严谨配置区】
  const memosHost = "https://sandleft-sandleft-memos.hf.space"; // 抱抱脸的绝对路径
  const limit = 20; // 每次拉取的条数
  const container = document.getElementById('memos-timeline');

  async function fetchMemos() {
    try {
      // 极致安全：不带任何 Token 请求，Memos 会自动过滤并只返回 Public 数据
      const res = await fetch(`${memosHost}/api/v1/memos?pageSize=${limit}`);
      const data = await res.json();
      
      // Memos v0.24.0 的数据解构
      const memos = data.memos || [];

      if (memos.length === 0) {
        container.innerHTML = "<div class='loading-text'>偏厅空空如也，等待第一缕墨香。</div>";
        return;
      }

      let html = '';
      memos.forEach(memo => {
        // 时间戳的优雅格式化
        const date = new Date(memo.createTime).toLocaleString('zh-CN', {
          year: 'numeric', month: '2-digit', day: '2-digit',
          hour: '2-digit', minute: '2-digit'
        });
        
        // 核心：使用 Marked.js 渲染 Markdown，完美支持欧尼酱的加粗、引用和列表
        const parsedContent = marked.parse(memo.content);
        
        html += `
          <div class="memo-card">
            <div class="memo-time">${date}</div>
            <div class="memo-content">${parsedContent}</div>
          </div>
        `;
      });
      container.innerHTML = html;

    } catch (error) {
      console.error("电路故障，抓取失败:", error);
      container.innerHTML = "<div class='loading-text'>赛博线路波动，请检查抱抱脸引擎是否处于 Running 状态。</div>";
    }
  }

  fetchMemos();
</script>