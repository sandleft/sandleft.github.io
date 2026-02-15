---
title: 库
date: 2026-02-14 23:59:00
type: "library"
aside: false
---

<link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">

<style>
  /* 🪄 基础全屏魔法 */
  #page, .layout, #content-inner, .article-container { max-width: 98% !important; padding: 10px 20px !important; }

  /* 顶部控制台 */
  .lib-controls { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; padding: 15px 20px; background: #fff; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
  .btn-group button { padding: 8px 18px; margin-right: 10px; cursor: pointer; border: none; background: #f0f2f5; border-radius: 6px; font-weight: bold; color: #555; transition: 0.3s; }
  .btn-group button.active { background: #409EFF; color: #ffffff; box-shadow: 0 2px 8px rgba(64,158,255,0.4); }

  /* 🌟 全维动态级联筛选面板 */
  #global-filter-panel { background: #fff; border-radius: 8px; padding: 15px 20px 5px 20px; margin-bottom: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); font-size: 0.9em; display: block; }
  .filter-row { display: flex; align-items: flex-start; margin-bottom: 12px; border-bottom: 1px dashed #f0f0f0; padding-bottom: 10px; }
  .filter-row.no-border { border-bottom: none; margin-bottom: 8px; }
  .filter-label { font-weight: bold; color: #888; width: 50px; flex-shrink: 0; margin-top: 5px; font-size: 0.95em; }
  .filter-items { display: flex; flex-wrap: wrap; gap: 6px; flex-grow: 1; }
  .f-btn { background: transparent; border: 1px solid transparent; padding: 4px 12px; border-radius: 4px; cursor: pointer; color: #333; transition: 0.2s; font-size: 0.95em; }
  .f-btn:hover { color: #409EFF; }
  .f-btn.active { background: #409EFF; color: #fff; font-weight: bold; box-shadow: 0 2px 4px rgba(64,158,255,0.3); }
  
  /* 搜索与排序区 */
  .search-sort-zone { display: flex; gap: 15px; align-items: center; width: 100%; justify-content: space-between; background: #fafbfc; padding: 10px 15px; border-radius: 6px; }
  .search-left { display: flex; gap: 15px; align-items: center; }
  .grid-search-input { padding: 6px 15px; border: 1px solid #ddd; border-radius: 20px; outline: none; transition: 0.3s; width: 280px; font-size: 0.9em; }
  .grid-search-input:focus { border-color: #409EFF; box-shadow: 0 0 5px rgba(64,158,255,0.3); }
  .grid-sort-select { padding: 6px 12px; border: 1px solid #ddd; border-radius: 6px; outline: none; cursor: pointer; background: #fff; font-size: 0.9em; color: #555; }

  /* 海报与表格样式保留 */
  .view-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 18px; }
  .grid-item { position: relative; border-radius: 6px; overflow: hidden; height: 260px; transition: transform 0.2s; cursor: pointer; display: block; background: #111; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
  .grid-item:hover { transform: scale(1.03); z-index: 10; box-shadow: 0 8px 20px rgba(64,158,255,0.4); }
  .grid-cover { width: 100%; height: 100%; object-fit: cover; }
  .grid-title-overlay { position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.5) 50%, transparent 100%); color: #fff; padding: 30px 12px 12px 12px; font-size: 0.9em; font-weight: bold; text-align: left; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.2; }
  .grid-badge { position: absolute; top: 6px; right: 6px; background: rgba(230, 162, 60, 0.9); color: #fff; font-size: 0.75em; padding: 2px 6px; border-radius: 4px; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.3); z-index: 5;}
  .grid-score { position: absolute; top: 6px; left: 6px; background: rgba(0, 0, 0, 0.6); color: #409EFF; font-size: 0.8em; padding: 2px 6px; border-radius: 4px; font-weight: bold; backdrop-filter: blur(4px); border: 1px solid rgba(64,158,255,0.3);}

  .table-wrapper { width: 100%; overflow-x: auto; background: #fff; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
  .view-table { width: 100%; border-collapse: collapse; font-size: 0.75em; word-wrap: break-word; }
  .view-table th, .view-table td { padding: 10px 6px; text-align: center; border-bottom: 1px solid #f0f0f0; border-right: 1px solid #f9f9f9; vertical-align: middle; }
  .view-table th { background: #fafafa; font-weight: bold; color: #333; cursor: pointer; }
  .view-table tr:hover { background: #f4f8ff; cursor: pointer; }
  .mini-cover { width: 100%; max-width: 45px; height: 60px; object-fit: cover; border-radius: 4px; }
  .col-summary { max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-align: left !important; }
  .lib-tag { display: inline-block; background: #555; color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; margin: 2px; white-space: nowrap;}
  table.dataTable { background-color: transparent; color: inherit; }
  .dataTables_wrapper .dataTables_filter { display: none; }
</style>

<div class="lib-controls">
  <div class="btn-group">
    <button id="btn-grid" class="active" onclick="switchView('grid')">🔲 海报矩阵</button>
    <button id="btn-table" onclick="switchView('table')">📄 档案总表</button>
  </div>
  <div style="font-size: 0.85em; color: #888;">赛博雷达已锁定 <span id="total-count" style="font-weight:bold; color:#409EFF; font-size: 1.2em;">0</span> 份灵魂印记</div>
</div>

<div id="global-filter-panel">
  <div class="filter-row">
    <div class="filter-label">频道</div>
    <div class="filter-items" id="f-category"></div>
  </div>
  <div class="filter-row" id="row-sub">
    <div class="filter-label">体裁</div>
    <div class="filter-items" id="f-sub"></div>
  </div>
  <div class="filter-row" id="row-year">
    <div class="filter-label">年份</div>
    <div class="filter-items" id="f-year"></div>
  </div>
  <div class="filter-row" id="row-status">
    <div class="filter-label">状态</div>
    <div class="filter-items" id="f-status"></div>
  </div>
  <div class="filter-row" id="row-lang">
    <div class="filter-label">语言</div>
    <div class="filter-items" id="f-lang"></div>
  </div>
  <div class="filter-row no-border" id="row-tags">
    <div class="filter-label">标签</div>
    <div class="filter-items" id="f-tags"></div>
  </div>
  
  <div class="filter-row no-border" style="margin-top: 15px;">
    <div class="search-sort-zone">
      <div class="search-left">
        <input type="text" id="g-search" class="grid-search-input" placeholder="🔍 全局穿透搜索 (名称/简介/标签)..." onkeyup="applyGlobalFilters()">
      </div>
      <div class="sort-right">
        <span style="font-size: 0.9em; color:#888; font-weight:bold; margin-right: 5px;">排序:</span>
        <select id="g-sort" class="grid-sort-select" onchange="applyGlobalFilters()">
          <option value="time_desc">最新入库优先</option>
          <option value="year_desc">发行年份 (新->旧)</option>
          <option value="score_desc">我的评分 (高->低)</option>
          <option value="score_pub_desc">大众评分 (高->低)</option>
        </select>
      </div>
    </div>
  </div>
</div>

<div id="grid-container" class="view-grid"></div>
<div id="table-container" style="display: none;">
  <div class="table-wrapper">
    <table id="koyso-library-table" class="view-table display">
      <thead><tr>
        <th style="width:40px;">封面</th><th style="min-width:100px;">名称</th><th style="min-width:60px;">作者</th>
        <th>状态</th><th>发行</th><th>频道</th><th>语言</th><th>体裁</th>
        <th style="min-width:120px;">标签</th><th style="min-width:150px;">简介</th><th>众评</th><th style="color:#409EFF;">我评</th>
        <th style="min-width:100px;">箴言</th><th>年份</th><th>时间</th><th>时长</th>
        <th>双链</th><th>文笔</th><th>人设</th><th>情节</th><th>内涵</th><th>情感</th><th>下载</th>
      </tr></thead>
      <tbody id="table-tbody"></tbody>
    </table>
  </div>
</div>

<script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
<script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

<script>
  let libData = [];
  let curView = 'grid';
  let tableEngine = null; 
  let fState = { cat: '全部', sub: '全部', year: '全部', stat: '全部', lang: '全部', tag: '全部', search: '', sort: 'time_desc' };

  fetch('/library.json').then(res => res.json()).then(data => {
    libData = data; 
    document.getElementById('total-count').innerText = data.length;
    
    renderDynamicFilters(); 
    renderInitialTableDOM(libData); 
    applyGlobalFilters(); 
  });

  // ==========================================
  // 🧠 核心：动态级联提取与渲染
  // ==========================================
  function renderDynamicFilters() {
    let subset = fState.cat === '全部' ? libData : libData.filter(item => item.col6 === fState.cat);

    let allCats = new Set();
    libData.forEach(i => { if(i.col6) allCats.add(i.col6); });

    let subs = new Set(), years = new Set(), stats = new Set(), langs = new Set(), tagCounts = {};
    subset.forEach(item => {
      if(item.col7) subs.add(item.col7);
      if(item.col13) years.add(item.col13);
      if(item.col4) stats.add(item.col4);
      if(item.col18) langs.add(item.col18);
      if(item.col8) item.col8.forEach(t => tagCounts[t] = (tagCounts[t]||0) + 1);
    });

    let yearArr = Array.from(years).sort((a,b) => b.localeCompare(a));
    let topTags = Object.keys(tagCounts).sort((a,b) => tagCounts[b]-tagCounts[a]).slice(0, 18);

    if(fState.sub !== '全部' && !subs.has(fState.sub)) fState.sub = '全部';
    if(fState.year !== '全部' && !years.has(fState.year)) fState.year = '全部';
    if(fState.stat !== '全部' && !stats.has(fState.stat)) fState.stat = '全部';
    if(fState.lang !== '全部' && !langs.has(fState.lang)) fState.lang = '全部';
    if(fState.tag !== '全部' && !topTags.includes(fState.tag)) fState.tag = '全部';

    const buildBtns = (type, items, currentState) => {
      let html = `<button class="f-btn ${currentState === '全部' ? 'active' : ''}" onclick="setFilter('${type}', '全部')">全部</button>`;
      items.forEach(i => {
        html += `<button class="f-btn ${currentState === i ? 'active' : ''}" onclick="setFilter('${type}', '${i}')">${i}</button>`;
      });
      return html;
    };

    document.getElementById('f-category').innerHTML = buildBtns('cat', Array.from(allCats), fState.cat);
    document.getElementById('f-sub').innerHTML = buildBtns('sub', Array.from(subs), fState.sub);
    document.getElementById('f-year').innerHTML = buildBtns('year', yearArr, fState.year);
    document.getElementById('f-status').innerHTML = buildBtns('stat', Array.from(stats), fState.stat);
    document.getElementById('f-lang').innerHTML = buildBtns('lang', Array.from(langs), fState.lang);
    document.getElementById('f-tags').innerHTML = buildBtns('tag', topTags, fState.tag);
    
    // 🌟 遗漏三修复：终极智能隐藏，没有数据的维度行直接物理蒸发！
    document.getElementById('row-sub').style.display = subs.size > 0 ? 'flex' : 'none';
    document.getElementById('row-year').style.display = years.size > 0 ? 'flex' : 'none';
    document.getElementById('row-status').style.display = stats.size > 0 ? 'flex' : 'none';
    document.getElementById('row-lang').style.display = langs.size > 0 ? 'flex' : 'none';
    document.getElementById('row-tags').style.display = topTags.length > 0 ? 'flex' : 'none';
  }

  // 🌟 遗漏一修复：修正了标签点击会报错的致命 ID 映射 Bug！
  window.setFilter = function(type, val) {
    fState[type] = val;
    if(type === 'cat') renderDynamicFilters(); 
    else {
      let containerId = 'f-' + (type === 'cat' ? 'category' : type === 'stat' ? 'status' : type === 'lang' ? 'lang' : type === 'tag' ? 'tags' : type);
      Array.from(document.getElementById(containerId).children).forEach(btn => {
        if(btn.innerText === val) btn.classList.add('active');
        else btn.classList.remove('active');
      });
    }
    applyGlobalFilters();
  };

  // ==========================================
  // 🔮 全维交叉过滤与排序
  // ==========================================
  window.applyGlobalFilters = function() {
    fState.search = document.getElementById('g-search').value.toLowerCase();
    fState.sort = document.getElementById('g-sort').value;
    
    let result = libData.filter(item => {
      if(fState.cat !== '全部' && item.col6 !== fState.cat) return false;
      if(fState.sub !== '全部' && item.col7 !== fState.sub) return false;
      if(fState.year !== '全部' && item.col13 !== fState.year) return false;
      if(fState.stat !== '全部' && item.col4 !== fState.stat) return false;
      if(fState.lang !== '全部' && item.col18 !== fState.lang) return false;
      if(fState.tag !== '全部' && !(item.col8 || []).includes(fState.tag)) return false;
      if(fState.search) {
        const text = (item.col1 + (item.col8||[]).join('') + (item.col9||'')).toLowerCase();
        if(!text.includes(fState.search)) return false;
      }
      return true;
    });

    result.sort((a, b) => {
      if(fState.sort === 'time_desc') return (b.col15||'').localeCompare(a.col15||'');
      if(fState.sort === 'year_desc') return (b.col13||'').localeCompare(a.col13||'');
      if(fState.sort === 'score_desc') return (parseFloat(b.col11) || 0) - (parseFloat(a.col11) || 0);
      if(fState.sort === 'score_pub_desc') return (parseFloat(b.col10) || 0) - (parseFloat(a.col10) || 0);
      return 0;
    });

    renderGridHtml(result);
    document.getElementById('total-count').innerText = result.length;

    if(tableEngine) {
      const escapeRegExp = string => string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); 
      const buildRegex = val => val === '全部' ? '' : '^' + escapeRegExp(val) + '$';
      
      // 🌟 遗漏四修复：标签的防误杀正则！将标签包围在 > < 中，完美避免“后宫”匹配到“反后宫”！
      const buildTagRegex = val => val === '全部' ? '' : escapeRegExp('>' + val + '<');
      
      tableEngine.column(5).search(buildRegex(fState.cat), true, false); 
      tableEngine.column(7).search(buildRegex(fState.sub), true, false); 
      tableEngine.column(13).search(buildRegex(fState.year), true, false); 
      tableEngine.column(3).search(buildRegex(fState.stat), true, false); 
      tableEngine.column(6).search(buildRegex(fState.lang), true, false); 
      tableEngine.column(8).search(buildTagRegex(fState.tag), true, false); 
      tableEngine.search(fState.search); 
      tableEngine.draw();
    }
  };

  // 🌟 遗漏二修复：找回了欧尼酱珍贵的专属主观评分数字！
  function renderGridHtml(dataArray) {
    const box = document.getElementById('grid-container');
    box.innerHTML = ''; 
    if(dataArray.length === 0) {
      box.innerHTML = '<div style="color:#888; text-align:center; width:100%; padding:40px 0; font-size:1.1em;">🕳️ 赛博雷达未能捕捉到符合条件的档案...</div>';
      return;
    }
    dataArray.forEach(item => {
      let badgeHtml = '';
      let scoreHtml = '';
      let score = parseFloat(item.col11) || 0;
      let scorePub = parseFloat(item.col10) || 0;
      
      if(scorePub > 0) scoreHtml = `<div class="grid-score">${scorePub} 分</div>`;
      if(score >= 8.5) badgeHtml = `<div class="grid-badge">⭐ ${score} 强推</div>`;
      else if (score > 0) badgeHtml = `<div class="grid-badge" style="background:rgba(64,158,255,0.9);">${score} 分</div>`;

      box.insertAdjacentHTML('beforeend', `
        <a class="grid-item" href="${item.link}">
          ${scoreHtml}
          ${badgeHtml}
          <img class="grid-cover" src="${item.col2 || 'https://via.placeholder.com/200x280'}" loading="lazy">
          <div class="grid-title-overlay">${item.col1}</div>
        </a>`);
    });
  }

  // 表格初始装载
  function renderInitialTableDOM(dataArray) {
    let tHtml = '';
    dataArray.forEach(item => {
      let tagsHtml = (item.col8 || []).map(t => `<span class="lib-tag">${t}</span>`).join('');
      tHtml += `
        <tr onclick="window.location.href='${item.link}'">
          <td><img class="mini-cover" src="${item.col2 || 'https://via.placeholder.com/30x40'}" loading="lazy"></td>
          <td style="font-weight:bold; color:#409EFF;">${item.col1}</td>
          <td>${item.col3}</td><td>${item.col4}</td><td>${item.col5}</td><td>${item.col6}</td>
          <td><span style="color:#e6a23c; font-weight:bold;">${item.col18 || ''}</span></td>
          <td>${item.col7}</td>
          <td style="text-align:left;">${tagsHtml}</td>
          <td class="col-summary" title="${item.col9}">${item.col9}</td>
          <td>${item.col10}</td><td style="font-weight:bold; font-size:1.1em; color:#409EFF;">${item.col11}</td>
          <td style="color:#888; font-style:italic; text-align:left;">${item.col12}</td>
          <td>${item.col13}</td><td>${item.col15}</td><td>${item.col16}</td><td>${item.col17}</td>
          <td>${item.r1}</td><td>${item.r2}</td><td>${item.r3}</td><td>${item.r4}</td><td>${item.r5}</td>
          <td><a href="${item.col14}" target="_blank" onclick="event.stopPropagation();">${item.col14 ? '🔗' : ''}</a></td>
        </tr>`;
    });
    document.getElementById('table-tbody').innerHTML = tHtml;

    $(document).ready(function() {
        tableEngine = $('#koyso-library-table').DataTable({
            "order": [[ 14, "desc" ]], 
            "columnDefs": [ { "orderable": false, "targets": [0, 22] } ],
            "pageLength": 50,
            "lengthMenu": [ 20, 50, 100, 500 ],
            "language": {
                "lengthMenu": "每页展示 _MENU_ 份档案",
                // 🌟 遗漏四修复：找回了欧尼酱原汁原味的汉化文案！
                "info": "表格视图: 当前显示第 _START_ 至 _END_ 份，共 _TOTAL_ 份档案馆藏",
                "infoEmpty": "档案馆空空如也...",
                "zeroRecords": "抱歉，没有任何档案穿透了当前的赛博防线。",
                "paginate": { "first": "首页", "last": "末页", "next": "下一页", "previous": "上一页" }
            }
        });
    });
  }

  // 视图无损切换
  window.switchView = function(v) { 
    curView = v; 
    document.getElementById('btn-grid').classList.toggle('active', v === 'grid'); 
    document.getElementById('btn-table').classList.toggle('active', v === 'table'); 
    if (v === 'grid') {
      document.getElementById('grid-container').style.display = 'grid';
      document.getElementById('table-container').style.display = 'none';
    } else {
      document.getElementById('grid-container').style.display = 'none';
      document.getElementById('table-container').style.display = 'block';
      if(tableEngine) tableEngine.columns.adjust().draw();
    }
  };
</script>