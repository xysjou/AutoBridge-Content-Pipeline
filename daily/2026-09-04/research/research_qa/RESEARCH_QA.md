# AutoBridge Daily Research QA — 2026-09-04（独立审核整改版 v1.1 + Final Cleanup v1.2）

> 本文件为第一阶段 Research 自检，不代表文章已写完/可上线/Codex 已审。
> 启动门：REPO_HEAD_SHA@pull=`ad84c58400aefc9b12baac1cbae9f5ea2bc2d36a`；LESSONS_LEARNED_SHA=`b4c46a7c28ba06227f0f4250bcc951048e701f2f`；LESSONS_READ_AT=2026-09-04 Asia/Shanghai；PRE-RESEARCH-SYNC=PASS。
> 批次状态：**READY_WITH_CONDITIONS**；MAIN PASS/COND/FAIL = 15/5/0；WRITING_READY=20/20；来源合计 120 条。

## 一、规则十九条逐项自检
- **1. 是否存在重复车型？** 无。24包与 /state 车型库、09-02/09-03历史五重去重(车型/关键词/意图/URL/主题)无碰撞；V04为Jolion中外拆分专题、V07为T9/悍途身份澄清,均非重复建页。
- **2. 是否存在重复搜索意图？** 无。G01归类/G02中国侧商检/G04提单/G08危规等意图互不重叠,与历史指南无 cannibalization。
- **3. 是否存在重复URL？** 无。全部为相对常绿路径且唯一;占位URL已清零。车型Hub采用无年款/无-specs后缀常绿URL。
- **4. 是否把中国版当全球版？** 否。车型 REFERENCE_MARKET 一律 CHINA;V04海外HEV/澳版数据 market 逐Fact为 OVERSEAS(具体国);V06 E8 PHEV与荣耀HEV分线;V07出口OEM数值与中国市场分列(export towing单独标EXPORT)。
- **5. 是否存在无来源关键参数？** 否。每条重要Fact均带 source/url/market/trim/checked/confidence;V04中国版扭矩/变速箱、V07中国动力单一T3均按规则降级并标注终核要求。
- **6. 是否存在参数冲突？** 无未处理CONFLICT。V07身份内部矛盾已消除,单一判定SAME_MODEL(双侧JAC OEM)。
- **7. 采购法规是否来自权威来源？** 是。法规/标准类均以政府/海关/标准组织/UNECE/全国人大T1为骨架(G01税则2026、G02商检框架、G04海商法2025修订、G06排放标准、G07 VIN国标正文、G08 IMDG/UN一手、G09现行合格证国标)。
- **8. 是否存在AI推测数据？** 否。无FOB/CIF/运费/利润率/海外售价/关税VAT/销量/市占率/最畅销等编造;中国指导价仅chinese_domestic_msrp+TIME_SENSITIVE且不换算出口报价;G10只讲费用项目不给金额。
- **9. 是否每篇都有Source URL？** 是。24份Source Log共120条来源,逐条真实URL+Organization+Domain+Tier+Scope+Checked+Official。
- **10. 是否所有时效性数据带日期？** 是。价格/在售/法规/税率/费率/标准版本/出口许可均标TIME_SENSITIVE并注公告号/施行日/核对日。
- **11. T4弱源是否被当关键事实唯一依据？** 否。G05 T4数值阈值已撤出,改WW/Höegh承运人官方;T4仅支撑EDITORIAL_RECOMMENDATION编辑建议清单;G10舱单费同改编辑建议。
- **12. 标准是否确认现行版本？** 是。G06=GB18352.6-2016+XG1-2026(2026-05-01)与GB17691-2018分列;G07=GB16735-2019;G08=IMDG42-24+UN手册Rev.8/Amend1;G01=税则2026;均带版本/修订/生效日/一手URL。
- **13. 草案是否被当现行？** 否。G09 CURRENT=GB/T21085-2020(现行);20260041-Q-339/GB21085—XXXX单列DRAFT/FUTURE;multistage因唯一草案依据已降UNVERIFIED并移出正文。
- **14. 车型别名是否有OEM证明？** 是。V04补GWM官网→基础车名SAME_MODEL(HEV动力分列);V07双侧JAC官方站→SAME_MODEL;无OEM证明只标RELATED。
- **15. 来源市场路径是否正确？** 是。V04澳/泰/越不标CHINA;V07 jacen=EXPORT/pickup.jac=CHINA;UNECE/IMDG标INTERNATIONAL;RoRo承运人标INTERNATIONAL且CARRIER_SPECIFIC。
- **16. 官方源范围是否匹配？** 是。轻型不套重型(G06);MIIT准入引用不替代标准正文(G07);承运人指南只适用该承运人(G05);法律框架不替代逐HS目录判定(G02)。
- **17. 事实级置信是否合规？** 是。跨市场不构成CROSS_CHECK(V04/V07);同一事实两独立来源一致才CROSS_CHECK;T1且scope匹配才VERIFIED;二级门户/媒体不升VERIFIED。
- **18. 生产Manifest是否含占位/测试URL？** 否。.example/localhost/test/staging/dummy 全部清除(生产JSON扫描=0);suggested_url为相对生产路径。
- **19. 共享文件与文件边界？** 本轮只写 daily/2026-09-04/research/;未改 articles/qa/deliveries;未新增/改写 LESSONS_LEARNED;改前确认main HEAD、禁force push。

## 二、独立审核问题处置台账（v1.1）
| 包 | 审核问题 | 处置 | 处置后判定 |
|---|---|---|---|
| 启动机制 | LESSONS版本过期,未记SHA | 记录REPO_HEAD/LESSONS_SHA/READ_AT;STARTUP_HEAD_SHA_GATE | PASS |
| V04 | 澳源误标CHINA;别名缺OEM | 逐Fact改OVERSEAS;补GWM OEM;跨市场降级;中国扭矩/变速箱入BLOCKED | CONDITIONAL(重复错误已纠正) |
| G02 | 未核现行法检目录不得PASS | 补官方框架+逐HS判定规则;未取得逐税号清单降CONDITIONAL | CONDITIONAL |
| G04 | 缺现行海商法一手 | 补NPC《海商法》2025修订(2026-05-01)第80/81/87条 | PASS |
| G05 | T4支撑关键操作 | 补WW/Höegh承运人官方;未取到项改confirm with carrier/OEM | CONDITIONAL |
| G06 | 标准过期/以轻概全/头条核心 | MEE/SAMR现行+2026修改单;轻重分列 | CONDITIONAL(海外限值仍BLOCKED) |
| G09 | 草案当现行 | CURRENT=GB/T21085-2020;强标计划单列DRAFT/FUTURE | PASS |
| G01 | 2018资料当2026主依据 | 财政部《税则(2026)》+海关2026公告;补8701 | PASS |
| G07 | 以MIIT引用替代标准正文 | GB16735-2019标准正文/SAMR | PASS |
| G08 | UN38.3/3480/3481缺UN一手 | UNECE Rev.8/Amend1+49CFR;保留MSA IMDG | PASS |
| V07 | 别名VERIFIED与BLOCKED矛盾 | 双侧JAC OEM→唯一判定SAME_MODEL | PASS |
| URL | 占位URL | 24包改相对常绿路径 | PASS |
| 批次 | 有COND却标READY | READY_WITH_CONDITIONS+逐篇WRITING_AI_READY | READY_WITH_CONDITIONS |

## 三、REPEATED_ERROR 复核
- V04 SOURCE_MARKET_PATH_CHECK：**RESOLVED=TRUE**（海外来源归位+OEM证据）。
- G06 CURRENT_STANDARD_VERSION_GATE：**RESOLVED=TRUE**（现行版本+修改单+生效日+一手URL，轻重分列）。
- 本批未发现LESSONS_LEARNED已禁错误再次出现。

## 四、CONDITIONAL 包 BLOCKED 边界（Writing 必须遵守）
- **V04**：中国版扭矩/变速箱具体值(仅澳版来源,市场不匹配)；海外HEV与中国1.5T的1:1等同；任何出口价格。
- **G02**：任一具体车型/10位税号当前是否落入法检目录(未取得整车逐税号清单,以海关现行目录+监管条件核验,TIME_SENSITIVE)。
- **G05**：绑扎/破断/车头朝向/胎压具体值(items to confirm with carrier/OEM)；统一SOC固定百分比(仅Höegh一家不得泛化)；T4数值；把承运人政策写成法规/全球统一。
- **G06**：海外Euro/EPA限值与EN燃油规格精确数值；国六与海外标准等效性结论。
- **G10**：任何具体金额(T4旧值/波动值不得写成当前确定收费)；不得据此估算到岸成本/利润。

## 五、NEW_LESSON_CANDIDATE（仅候选，待独立审核，不自行写入永久规则）
- 专用车上装第三方型号高度混淆且无官网时直接换题而非CONDITIONAL。
- 卡车之家原创仅以今日头条镜像可检索时,Source Name写卡车之家但domain如实填m.toutiao.com并降一级。

---

# FINAL RESEARCH CLEANUP — 2026-09-04（仅 V07 / G05 / G09；机器门全量扫描 24 包）

> 按 Final Cleanup 指令执行：**不重做全部 20 篇、不新增 LESSONS_LEARNED 规则**，只提高既有永久规则执行率；另新增三台**机器 QA 门**（检测逻辑，非新 Lesson）。

## A. 三篇处置
### V07 JAC T9（维持 RESEARCH_PASS，v1.2）
- 逐 Fact 做 SOURCE_MARKET_PATH_CHECK + PRIMARY_SOURCE_SCOPE_MUST_MATCH：`jacen`=EXPORT Primary，`pickup.jac`=CHINA Primary，车家号=CHINA T2，搜狐/太平洋=CHINA T3。
- 出口 Primary 市场非 CHINA 不得升 VERIFIED：标轴车长/轴距/货箱 VERIFIED→**CROSS_CHECKED**（出口OEM+中国T2一致）。
- 中国动力(engine/125kW/410N·m/ZF8AT/分时四驱)中国侧仅搜狐 T3，降 **SINGLE_SOURCE**，正文标“以厂商配置单终核”，不得称双源。
- `towing 3500kg`→`towing_capacity_export`，market=EXPORT、VERIFIED（出口Primary scope匹配），禁止当中国公告/全系值。
- `payload 1000kg` 因存在 CHINA Primary 与出口OEM一致，中国市场 VERIFIED 成立。
- MODEL_ALIAS **SAME_MODEL 保留**，身份与配置市场分开判断。

### G05 PDI（维持 RESEARCH_CONDITIONAL，v1.2）
- WW/Höegh 规则全部显式标 **CARRIER_SPECIFIC（具名承运人政策，非法规、非全球统一）**：燃油≤1/4(两家CROSS_CHECKED)、无kill-switch二手车系固后断12/24V(WW)、BEV≤50%SOC(Höegh)、RoRo须可自行开上开下(WW+Höegh)。
- 原仅T4(11467)支撑的PDI_SCOPE/交接单/拍照清单改 **EDITORIAL_RECOMMENDATION=TRUE**，口径“AutoBridge recommended pre-shipment checklist”，不得写成 industry mandatory procedure。
- 绑扎/破断/车头朝向/胎压/统一SOC仍 UNVERIFIED（items to confirm with carrier/OEM）。

### G09 文件包（维持 RESEARCH_PASS，v1.2）
- `multistage` 唯一依据为 MIIT GB21085 **征求意见稿**，按 DRAFT_SOURCE_GATE 由 VERIFIED 降 **UNVERIFIED**，移出 FACTS_ALLOWED_IN_BODY，进入 BLOCKED/UNRESOLVED，待 GB/T21085-2020 正文或现行规章证实。
- `mfg_cert` 现行依据只保留 openstd+全国标准信息平台两个 T1；草案剥离由 `draft_future_standard` 单列（TIME_SENSITIVE，current_requirement=false）。CURRENT_STANDARD 仍 GB/T21085-2020 不变。

## B. 三台机器 QA 门（自动检测，扫描全部 24 包）
- **MARKET_CONFIDENCE_GATE**：CHINA Fact 为 VERIFIED 时必须存在 CHINA Primary；仅靠非 CHINA Primary => FAIL。
- **DRAFT_SOURCE_GATE**：仅当**来源**含 draft/征求意见/计划/正在批准且 VERIFIED+current_requirement=TRUE => FAIL（只扫来源，不扫 value/note）。
- **T4_BODY_GATE**：T4-only Fact 进确定性正文且无 EDITORIAL_RECOMMENDATION、也未进 BLOCKED => FAIL。
- 首扫命中 6 处标签层问题，按“只改标注/来源层级、不新研究”处置：G08 两条国际规则 market 改 INTERNATIONAL（中国 MSA 执行）、UN3480/3481 改用已采集 UNECE/49CFR/MSA 一手 T1（撤 T4）；V04 别名来源主体确认为 GWM 中国 OEM 官网（CHINA Primary）；G10 舱单申报费改 EDITORIAL_RECOMMENDATION（无金额、非强制）。
- **复扫：scanned_packages=24，fail_count=0，result=PASS**（三门均无命中）。机器门原始结果见 MACHINE_QA_GATES_2026-09-04.json。

## C. 状态重算（按事实，不凑数）
- MAIN：PASS=15 / CONDITIONAL=5（V04、G02、G05、G06、G10）/ FAIL=0；WRITING_READY=20。
- 全包 24：PASS=17 / CONDITIONAL=7 / FAIL=0。BATCH_STATUS=**READY_WITH_CONDITIONS**。
- V07、G09 修正后核心意图仍成立维持 PASS；G05 维持 CONDITIONAL（BLOCKED 见 Fact Sheet/Handoff）。
- 生产 JSON 占位符扫描结果：0。

## 六、QA 结论
- 20 个 MAIN 无 FAIL、无未处理冲突、无占位URL、关键法规均有 T1；5 个 CONDITIONAL 带明确 BLOCKED 仍可写（WRITING_AI_READY=TRUE）。
- RESEARCH_QA = PASS（附 CONDITIONAL 边界）；Writing AI 须以 v1.2（V04/V07/G05/G08/G09/G10）/ v1.1（其余）Fact Sheet 为准，CONDITIONAL 包不得把 BLOCKED 写成确定事实。
