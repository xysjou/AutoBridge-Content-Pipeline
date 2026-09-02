# RESEARCH QA — AutoBridge Daily 2026-09-03

检查日期：2026-09-03（Asia/Shanghai）｜范围：20 MAIN（10 VEHICLE +10 GUIDE）+4 RESERVE｜去重基线：历史 93 篇 COMPLETED（batch_20260831_001=43、batch_20260901_001=50）+ 前一日 2026-09-02 的 24 个候选。

## 一、规则十九条逐项核查
1. **是否存在重复车型？** 否。12 个车型（含备用）逐一比对历史 39 个车型页与 09-02 的 12 个车型（Yuan Plus/UNI-V/Qin Plus DM-i/Trumpchi M8/Poer/Lingzhi M5/JAC Kangling/HOWO T7H/Shacman X3000/Foton Aumark/Hongqi E-HS9/Qiyuan Q05），品牌+车型均不同；VR1 瑞虎7 与历史瑞虎8为不同车型（已在 Fact Sheet 标注）。
2. **是否存在重复搜索意图？** 否。G09 海外售后体系与历史 spare_parts（在中国采购备件）意图不同，已在 Fact Sheet 头部写明边界；G04 集装箱装载（怎么装/怎么固定）与历史 roro_container（选哪种运输方式）意图不同；G03 认证文件体系与 09-02 G01 俄罗斯 EAC（单国认证流程）不同层级。
3. **是否存在重复 URL（suggested_url）？** 否。24 条 suggested_url slug 两两不同，见 daily_manifest.json。
4. **是否把中国版当全球版？** 否。全部车型 REFERENCE_MARKET=CHINA，标注中国工况（CLTC）与中国年款；海外版（如海豚日本、V6E 土耳其欧标版）单列且不与中国版混用参数。
5. **是否存在无来源关键参数？** 否。每条 FACT 均带 Source+URL+Checked+Confidence；无独立来源支撑的参数不写入（如 V07 宇通具体发动机只给同平台参考并标 SINGLE_SOURCE）。
6. **是否存在参数冲突？** 存在 1 处已隔离：G08 非洲车龄（肯尼亚 7 vs 8 年、尼日利亚 12 vs 15 年）在货代来源间冲突，全部标 CONFLICT/TIME_SENSITIVE，**不进入确定性事实库**，仅保留对照框架并要求官方核验。车型参数中 V01 帝豪新旧款功率差异通过锁定 2024 第4代 + 第5代单列 TIME_SENSITIVE 消解。
7. **采购法规是否来自权威来源？** 中国侧法规（G01/G09）使用商务部、中国政府网、工信部 T1 官方源；G05 引用中国海事；V09/V03/V07/V10 含厂商官网/官方媒体。**G02 阿联酋、G03 欧盟原文、G08 非洲各国未取得目的国政府一手页面**，已在各自 UNRESOLVED 中标注，相关税率/年限/法规日期全部 TIME_SENSITIVE，不得在第二阶段写成确定结论。
8. **是否存在 AI 推测数据？** 否。未生成任何 FOB/CIF、海运费、利润率、海外售价、关税/VAT 具体金额、销量/市占率、“最畅销”等；中国指导价仅标 Chinese domestic MSRP/reference 且 TIME_SENSITIVE，未换算成出口报价。
9. **是否每篇都有 Source URL？** 是。24 个包共 97 条来源（G08 科特迪瓦补入第 6 源），全部为真实可访问 http(s) URL，无“Chery Official”式空名来源。
10. **所有时效性数据是否带日期？** 是。价格/在售/法规/税率/认证版本/年款改款均标 TIME_SENSITIVE 并带 Checked=2026-09-03 与适用市场。

## 二、跨批次去重记录
- 历史车型黑名单 39 个（/state/vehicle_database.json）+ 09-02 车型 12 个：今日 12 个全部不命中。
- 历史指南 13 主题簇（roro_container/photo_vin_review/battery_warranty/chinese_phev_sourcing/spare_parts/pickup_export/mpv_procurement/fob_cif/new_vs_used_ev/seven_seat_suv/price_verification/middle_east_chinese_suv/best_chinese_suvs）+ 09-02 指南 12 个：今日 12 个主题均为新增方向（出口侧报关许可、目的国注册、CoC/型式认证体系、集装箱入柜、UN3171 海运危规、PSI 装运前检验、中东高温适配、非洲车龄对照、海外售后体系、出口合同条款、欧盟 WVTA 深入、中亚分国路径）。
- 无 NEW_PAGE 伪装更新：未发现需要 CONTENT_ACTION=UPDATE_EXISTING 的在库车型（今日均为库外新车型）。

## 三、事实分级统计（口径：仅 MAIN 20）
- VERIFIED：多源/官方一致的确定性参数（如 V03/V04 全系参数、V09 官网容量、G01 180天新规、G09 售后政策条款）。
- CROSS_CHECKED：两个独立来源一致。
- SINGLE_SOURCE：仅单源，已标注，写作时须弱化或补源。
- CONFLICT：仅 G08 车龄，已隔离，禁止进入确定性事实库。
- TIME_SENSITIVE：全部价格、法规/税率/认证版本、年款改款、船司规则。
- UNVERIFIED：0（无法确认者直接不写入 FACT，转入 UNRESOLVED）。

## 四、给第二阶段（Writing）的硬约束
1. REFERENCE_MARKET=CHINA 的参数不得改写为 global spec；CLTC 不得等同 WLTP/EPA。
2. G02/G03/G08/GR1/GR2 中标 TIME_SENSITIVE/CONFLICT 的数字，第二阶段必须先补目的国官方源再写，补不到就不写具体数值。
3. 中国指导价只能写“Chinese domestic MSRP/reference”，禁止换算出口报价；禁止编造运费/利润/销量。
4. 三个汽车数据库（懂车帝/汽车之家/360che）仅用于事实提取，正文须重新组织，禁止复制其测评/评论/结构。
5. 每个结论须能回溯到本包 FACT 的 URL；UNRESOLVED QUESTIONS 不得自行补写。
6. 本阶段只交付研究产物，不写正文、不做多语言、不打文章 ZIP。

## 五、提交状态（已更新）
全部 53 个研究文件已通过 GitHub MCP（push_files）分批提交到共享仓库 xysjou/AutoBridge-Content-Pipeline 的 main，commit message 统一为 `Daily research 2026-09-03`；只写入 /daily/2026-09-03/research/，未触碰 articles/qa/deliveries。最终 HEAD commit 与 pushed=true 以 RESEARCH_READY.json 的 repo_commit 字段为准（最后一个 commit 回填）。第二阶段以仓库 main 上存在本目录且 RESEARCH_READY.status=READY 为启动前提。
