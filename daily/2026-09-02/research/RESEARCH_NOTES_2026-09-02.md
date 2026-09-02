# Research Notes — 2026-09-02（Stage 1 方法与过程留痕）
## 1. 启动与历史读取（等效 git pull）
- 通过 GitHub MCP 读取共享仓库 `xysjou/AutoBridge-Content-Pipeline` main 分支：根目录、`batches/index.json`、两份批次 manifest（batch_20260831_001=43、batch_20260901_001=50，合计 93 篇 COMPLETED）。
- 仓库实际历史载体为 `batches/`（规则文本假设的 /state//daily//rules/ 当时尚不存在）。本次据 batches 派生 /state 四个去重索引，并新建 /daily/2026-09-02/research/。
- 未修改 articles/、qa/、deliveries/ 等第二阶段目录；未新建独立仓库。
## 2. 选题与类别覆盖
- 车型 12（10 MAIN+2 备用）跨类别覆盖：EV SUV、ICE 轿跑、PHEV 轿车、MPV、皮卡、VAN、轻卡、牵引车、自卸车、冷藏车、大型电 SUV、插混 SUV——避免连续堆新能源 SUV。
- 指南 12（10 MAIN+2 备用）覆盖：目的国进口合规（俄/沙特/智利/泰国）、供应商审核、二手检测、充电兼容、左右舵、海运保险、车机本地化、车队批量采购、付款方式。
## 3. 采集逻辑
- 乘用车：懂车帝 + 汽车之家 + 太平洋/易车/中关村在线，尽量叠加品牌官网；关键参数≥2 独立来源比对。
- 商用车：360che 卡车之家（公告级参数）+ 厂商官网（福田奥铃、中国重汽、陕汽、东风风行）+ 必要的底盘/发动机来源。
- 采购指南：法规/关税/认证优先官方机构（商务部、贸促会/CIETAC、中国驻智利使馆经商处、泰国 BOI、GB 标准、UNECE/CHAdeMO 等）；汽车媒体仅用于车型背景与中国市场配置。
## 4. 事实分级口径
- VERIFIED：官方 + 数据库一致；CROSS_CHECKED：两个独立可靠来源一致；SINGLE_SOURCE：仅一个来源；CONFLICT/UNVERIFIED：不进入确定性事实库；TIME_SENSITIVE：价格/在售/法规/税率/费率，带 URL+日期+适用国。
- 全部中国版参数 REFERENCE_MARKET=CHINA，不写成全球规格；未取得海外官方版本不混配。
## 5. 历史去重重做记录（关键）
- 初次本地研究因尚未接入共享仓库，误标 CLEAN_START；接入 batches/93 篇真实历史后重做全站去重。
- 替换 4 篇重叠/重复指南（G03/G07/G08/G10），保留并书面区分 G04 意图边界，12 车型全部干净。详见 research_qa/RESEARCH_QA_2026-09-02.md 与 daily_manifest.json 的 dedup_baseline。
## 6. 访问受限处理
- 遇到需要登录/验证码/反爬的页面不绕过，记 SOURCE_ACCESS_FAILED 并换公开来源；本批未出现阻断性访问失败。
## 7. 遗留待办（移交第二阶段，不自行补写）
- 部分车型缺品牌官网一页式确认（V01/V03/V05/V07/VR2），写作前可补；当前为多源 CROSS_CHECKED。
- G02/G07/G08 的部分一手监管/承保口径、G02 泰国与 G09 智利的现行税率/补贴，属 TIME_SENSITIVE，写作当日复核。
- state/published_urls.json 待第二阶段发布真实 slug 后回填。
## 8. 本阶段边界
不写正文、不生成 12 语言、不打文章 ZIP；产出仅 Fact Sheets / Source Logs / Research QA / Daily Manifest / RESEARCH_READY，供第二阶段 Writing Pipeline 在本 commit push 后启动。
