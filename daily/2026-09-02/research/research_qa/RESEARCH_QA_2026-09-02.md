# Research QA — 2026-09-02（AutoBridge Daily Research, Stage 1）
- 运行日期：2026-09-02
- 去重基线：共享仓库 `batches/` 两个已完成批次，共 **93 篇**历史文章
  - batch_20260831_001 = 43（COMPLETED）
  - batch_20260901_001 = 50（COMPLETED，active v2，QA_READY）
- 派生去重索引（本次新建于 /state/）：article_manifest.json（93）、vehicle_database.json（39 车型页）、guide_database.json（54 指南，13 个主题簇）、published_urls.json（历史无 URL 字段，置空并说明）
- 候选：20 MAIN（10 车型 + 10 指南）+ 4 RESERVE（2 + 2）= 24
## 一、跨批次历史去重（接入共享仓库后新增的强制检查）
### 1. 车型去重（模型 / Search Intent / URL）
历史 39 个车型页中，中国品牌为 BYD Song Plus DM-i、BYD Seal、Chery Tiggo 8、GWM Haval H6、GAC AION Y Plus、Geely New Coolray、MG ZS；其余为海外品牌。
本日 12 个车型（Yuan Plus / UNI-V / Qin Plus DM-i / Trumpchi M8 / Great Wall Poer / Lingzhi M5 / JAC Kangling / HOWO T7H / Shacman X3000 / Aumark 冷藏 + 备用 Hongqi E-HS9、Qiyuan Q05）**逐一比对均无历史车型页，无同模型、同意图、同 URL**。
- 特别排除：Aion Y Plus 已存在（AB50_001），备用位已改用 Hongqi E-HS9，正确避开。
- 结论：**12/12 车型 NEW，无重复。**
### 2. 采购指南主题簇去重
历史 54 篇指南归并为 13 个主题簇：roro_container(7)、photo_vin_review(6)、battery_warranty(5)、chinese_phev_sourcing(5)、spare_parts(5)、pickup_export(5)、mpv_procurement(5)、fob_cif(5)、new_vs_used_ev(4)、seven_seat_suv(3)、price_verification(2)、middle_east_chinese_suv(1)、best_chinese_suvs(1)。
**判定为重复/高度重叠并已替换（4 篇，替换记录写入 daily_manifest.json）：**
| 槽位 | 原选题 | 命中历史簇 | 处置 | 替换为 |
|---|---|---|---|---|
| G03 | 中国 VIN 17 位解码（GB16735） | photo_vin_review(6)，含 global v2 | REPLACED | 中国汽车出口供应商审核与尽调 |
| G07 | Incoterms EXW/FOB/CIF/DDP | fob_cif(5) | REPLACED | 车辆进口海运货物保险 ICC A/B/C |
| G08 | RoRo vs Container | roro_container(7)，直接重复 | REPLACED | 车机语言/App/OTA 海外适配 |
| G10 | EV 电池质保转移 | battery_warranty(5) | REPLACED | 商用车/卡车车队批量采购 |
**保留但写明意图边界（1 篇）：**
- G04 二手中国 EV 出口前**技术检测清单**（SOH/事故/泡水/调表）：历史 new_vs_used_ev(4) 解决"买新还是买二手"的**决策**，本篇是已决定买二手后的**检测操作**，搜索意图不同；Fact Sheet 头部已写入边界，写作禁止回到决策对比。
**其余指南确认无历史同主题：** G01 俄罗斯 EAC/OTTC、G02 沙特 SASO、G05 充电标准兼容、G06 右舵、G09 智利 FTA、GR1 T/T vs L/C、GR2 泰国 EV3.5，以及 4 个新替换题，均不落入 13 个历史簇。
## 二、规则十九条 Research QA 逐项
| # | 检查项 | 结果 | 说明 |
|---|---|---|---|
| 1 | 是否存在重复车型 | PASS | 12 车型对 39 历史车型页 0 重复 |
| 2 | 是否存在重复搜索意图 | PASS | 4 篇重叠指南已替换；G04 意图边界已书面区分 |
| 3 | 是否存在重复 URL | PASS | 24 个 suggested_url 互不相同，且不与历史 slug 冲突 |
| 4 | 是否把中国版当全球版 | PASS | 车型参数一律 REFERENCE_MARKET=CHINA，标注年款/配置/来源；未取得海外官方版不写 global spec |
| 5 | 是否存在无来源关键参数 | PASS（附缺口） | 每条关键事实带 URL+日期+市场；V01/V03/V05/V07/VR2 未取得品牌官网页，关键参数为≥2 独立数据库 CROSS_CHECKED，未拔高为 VERIFIED |
| 6 | 是否存在参数冲突 | PASS | 冲突项标 CONFLICT 并不进入确定性事实库；本批无未解决的关键参数 CONFLICT |
| 7 | 采购法规是否来自权威来源 | PASS（附限制） | G01/G03/G09 含政府/官方机构一手来源（T1）；G02/G07/G08 部分主张来自行业源，已单列 TIME_SENSITIVE 与 UNRESOLVED，写作时须复核 |
| 8 | 是否存在 AI 推测数据 | PASS | 无 FOB/CIF/运费/利润率/海外售价/关税/销量/"最畅销"等编造；中国指导价仅标 domestic reference，不换算出口报价 |
| 9 | 是否每篇都有 Source URL | PASS | 24 份 Source Log 均为真实 URL（无裸写"BYD Official"），共 123 条来源记录（MAIN 104 + RESERVE 19） |
| 10 | 是否所有时效性数据带日期 | PASS | 法规/税率/认证/费率/在售状态均标 TIME_SENSITIVE + URL + 适用国 + 日期；无法核实者入 UNRESOLVED QUESTIONS |
## 三、READY 门槛结论
- 20 个 MAIN 全部满足：意图明确、历史无重复、核心资料足够、关键事实无严重冲突、来源合理、重要信息可核验 → research_status = READY。
- 4 个 RESERVE 完整度同 MAIN，仅优先级为 RESERVE。
- 无 REJECTED。
- **STATUS = READY**（非 PARTIAL；缺口为"可在写作阶段补强官方页"的非阻断项，已在 RESEARCH_READY.json 与各 Fact Sheet 的 UNRESOLVED 中如实登记）。
## 四、给第二阶段的硬约束（随包移交）
1. 只能使用 VERIFIED / CROSS_CHECKED 作为确定性事实；SINGLE_SOURCE 须表述为"据某来源"；CONFLICT/UNVERIFIED 不得写成事实。
2. TIME_SENSITIVE 项（俄 EAC、沙特 SASO、智利关税、泰国 EV3.5、保险费率、出口资质名录、车机 HMI 要求）写作当日必须重新核验并写日期。
3. 中国市场参数不得写成全球规格；不得把国内指导价换算成 AutoBridge 报价。
4. UNRESOLVED QUESTIONS 不允许第二阶段自行补写，需回传研究阶段。
5. 本阶段不写正文、不做多语言、不打包文章 ZIP。
