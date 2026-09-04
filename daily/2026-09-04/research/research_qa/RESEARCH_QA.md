# AutoBridge Daily Research QA — 2026-09-04（独立审核整改版 v1.1）

> 本文件为第一阶段 Research 自检，不代表文章已写完/可上线/Codex 已审。
> 启动门：REPO_HEAD_SHA@pull=`ad84c58400aefc9b12baac1cbae9f5ea2bc2d36a`；LESSONS_LEARNED_SHA=`b4c46a7c28ba06227f0f4250bcc951048e701f2f`；LESSONS_READ_AT=2026-09-04 Asia/Shanghai；PRE-RESEARCH-SYNC=PASS（LOCAL_HEAD=ORIGIN_MAIN 后才改）。
> 批次状态：**READY_WITH_CONDITIONS**；MAIN PASS/COND/FAIL = 15/5/0；WRITING_READY=20/20；FACT_SHEET_VERSION=v1.1-2026-09-04；来源合计 120 条。

## 一、规则十九条逐项自检
- **1. 是否存在重复车型？** 无。24包与 /state 车型库(59)、09-02/09-03历史五重去重(车型/关键词/意图/URL/主题)无碰撞；V04为Jolion中外拆分专题、V07为T9/悍途身份澄清,均非重复建页。
- **2. 是否存在重复搜索意图？** 无。G01归类/G02中国侧商检/G04提单/G08危规等意图互不重叠,与历史指南无 cannibalization。
- **3. 是否存在重复URL？** 无。全部改为相对常绿路径且唯一;占位 .example 已清零(残留包:无)。车型Hub采用无年款/无-specs后缀常绿URL(EVERGREEN_MODEL_URL_BY_DEFAULT)。
- **4. 是否把中国版当全球版？** 否。车型 REFERENCE_MARKET 一律 CHINA;V04海外HEV/澳版数据 market 已逐Fact改为 OVERSEAS(具体国),不再标CHINA;V06 E8 PHEV与荣耀HEV分线;海外市场版本单列不并参。
- **5. 是否存在无来源关键参数？** 否。每条重要Fact均带 source/url/market/trim/checked/confidence;V04中国版扭矩/变速箱因仅有澳版来源已撤出确定事实并入BLOCKED/UNRESOLVED。
- **6. 是否存在参数冲突？** 无未处理CONFLICT(现存CONFLICT字段:无)。V07身份内部矛盾已消除,单一判定SAME_MODEL(双侧JAC OEM)。
- **7. 采购法规是否来自权威来源？** 是。法规/标准类T1官方源数量:G01=4, G02=5, G03=3, G04=1, G06=8, G07=4, G08=4, G09=7。G02补商检法实施条例(海关总署PDF)+互联网+海关指南+2024年163号抽查公告+BEV出口许可证(商务部);G04补全国人大《海商法》2025修订;G06补生态环境部/SAMR;G08补UNECE/UN+MSA;G09补SAMR现行/计划双状态。
- **8. 是否存在AI推测数据？** 否。无FOB/CIF/运费/利润率/海外售价/关税VAT/销量/市占率/最畅销等编造;中国指导价仅chinese_domestic_msrp+TIME_SENSITIVE且不换算出口报价;G10只讲费用项目不给金额。
- **9. 是否每篇都有Source URL？** 是。24份Source Log共120条来源,逐条真实URL+Organization+Domain+Tier+Scope+Checked+Official;无URL来源包:无;无'品牌名无URL'。
- **10. 是否所有时效性数据带日期？** 是。价格/在售/法规/税率/费率/标准版本/出口许可均标TIME_SENSITIVE并注公告号/施行日/核对日;G01标2026版税则,G04标海商法2026-05-01施行,G06标修改单2026-05-01。
- **11. T4弱源是否被当关键事实唯一依据？** 否。G05原T4数值阈值(留油5%/绑扎/胎压/SOC/车头朝向)已撤出,改WW/Höegh承运人官方(燃油≤1/4两家CROSS_CHECKED、BEV≤50%SOC Höegh),未取到的绑扎/朝向/胎压改为items to confirm with carrier/OEM并入BLOCKED。
- **12. 标准是否确认现行版本(CURRENT_STANDARD_VERSION_GATE)？** 是。G06=GB18352.6-2016+XG1-2026(2026-05-01)与GB17691-2018分列、GB19147-2016现行;G07=GB16735-2019现行(标准正文直接支持);G08=IMDG42-24+UN手册Rev.8/Amend1;G01=税则2026;均带版本/修订/生效日/一手URL。
- **13. 草案是否被当现行(DRAFT_STANDARD_IS_NOT_CURRENT_STANDARD)？** 否。G09 CURRENT_STANDARD=GB/T21085-2020(现行,推荐性);强制版20260041-Q-339/GB21085—XXXX单列DRAFT/FUTURE(正在批准/征求意见,未生效),禁止标CURRENT MANDATORY。
- **14. 车型别名是否有OEM证明(MODEL_ALIAS_REQUIRES_OEM_PROOF)？** 是。V04补GWM官网'哈弗初恋海外版JOLION'→基础车名SAME_MODEL(HEV动力仍分列);V07双侧JAC官方站→SAME_MODEL并删除矛盾BLOCKED;无OEM证明的关系只标RELATED。
- **15. 来源市场路径是否正确(SOURCE_MARKET_PATH_CHECK)？** 是。逐条核对URL国家/主体/标题;V04澳/泰/越来源不再标CHINA;UNECE标INTERNATIONAL;RoRo承运人标INTERNATIONAL(具名承运人政策)。
- **16. 官方源范围是否匹配(PRIMARY_SOURCE_SCOPE_MUST_MATCH)？** 是。轻型标准不套重型(G06分列);MIIT准入文件只支撑'准入引用'不替代标准正文(G07);具名承运人指南只适用该承运人(G05);法律框架不替代逐HS目录判定(G02)。
- **17. 事实级置信是否合规(CONFIDENCE_IS_FACT_LEVEL)？** 是。跨市场不构成CROSS_CHECK(V04轴距/功率已降SINGLE);同一事实两独立来源一致才CROSS_CHECK;标准正文/立法机关/政府一手且范围匹配才VERIFIED;二级门户/媒体不升VERIFIED。
- **18. 生产Manifest是否含占位/测试URL(PLACEHOLDER_URL_BLOCK)？** 否。.example/localhost/test/staging/dummy 全部清除(发现占位包:无);suggested_url为相对生产路径。
- **19. 共享文件与文件边界？** 整改只写 daily/2026-09-04/research/ 与 LESSONS_LEARNED.md(追加永久规则);未改 articles/qa/deliveries;改前等效pull(HEAD ad84c584),禁force push。

## 二、独立审核问题处置台账
| 包 | 审核问题 | 处置 | 处置后判定 |
|---|---|---|---|
| 启动机制 | LESSONS版本33eff0e3过期,未记SHA | 记录REPO_HEAD/LESSONS_SHA/READ_AT;新增STARTUP_HEAD_SHA_GATE永久规则 | PASS |
| V04 | 澳源误标CHINA;别名缺OEM | 逐Fact改OVERSEAS;补GWM官网OEM同名;跨市场降级;中国版扭矩/变速箱入BLOCKED | CONDITIONAL(重复错误已纠正) |
| G02 | 未核现行法检目录不得PASS | 补官方框架+逐HS判定规则+抽查公告+BEV许可证;未取得逐税号清单故降CONDITIONAL | CONDITIONAL |
| G04 | 缺现行海商法一手 | 补NPC《海商法》2025修订(2026-05-01)第80/81/87条 | PASS |
| G05 | T4支撑关键操作 | 补WW/Höegh承运人官方;未取到的绑扎/朝向/胎压改confirm with carrier/OEM | CONDITIONAL |
| G06 | 标准过期/以轻概全/头条核心 | 改MEE/SAMR现行+2026修改单;轻型GB18352.6与重型GB17691分列;GB19147现行页 | CONDITIONAL(海外限值仍BLOCKED) |
| G09 | 草案当现行 | CURRENT=GB/T21085-2020;20260041-Q-339单列DRAFT/FUTURE | PASS |
| G01 | 2018资料当2026主依据 | 改财政部《税则(2026)》+海关2026执行公告;补8701;删头条核心 | PASS |
| G07 | 以MIIT引用替代标准正文 | 改GB16735-2019标准正文/SAMR;VIN结构事实VERIFIED;首字母产地绝对化撤出 | PASS |
| G08 | UN38.3/3480/3481缺UN一手 | 补UNECE Rev.8/Amend1+49CFR173.185;保留MSA IMDG | PASS |
| V07 | 别名VERIFIED与BLOCKED自相矛盾 | 双侧JAC OEM→唯一判定SAME_MODEL,删旧BLOCKED | PASS |
| URL | autobridge.example占位 | 24包全部改相对常绿路径,车型Hub去年款/-specs后缀 | PASS |
| 批次状态 | 有CONDITIONAL却标READY | 改READY_WITH_CONDITIONS;输出MAIN PASS/COND/FAIL与逐篇WRITING_AI_READY | READY_WITH_CONDITIONS |

## 三、REPEATED_ERROR 复核
- V04 SOURCE_MARKET_PATH_CHECK：整改前 REPEATED_ERROR=TRUE/SEVERITY=HIGH；整改后海外来源market全部归位、补OEM证据，**RESOLVED=TRUE**。
- G06 CURRENT_STANDARD_VERSION_GATE：整改前 REPEATED_ERROR=TRUE/HIGH；整改后现行版本+修改单+生效日+一手URL齐备且轻重分列，**RESOLVED=TRUE**。
- 除上述两项已闭环外，本批未发现LESSONS_LEARNED已禁错误再次出现。

## 四、CONDITIONAL 包 BLOCKED 边界（Writing 必须遵守）
- **AB-260904-V04**：BLOCKED=['中国版扭矩/变速箱具体值(现仅澳版来源,市场不匹配)', '海外HEV与中国1.5T的1:1配置等同', '任何出口价格']
- **AB-260904-G02**：BLOCKED=['任一具体车型/10位税号当前是否落入法检目录(本批未取得现行目录整车逐税号清单,申报时须以海关现行目录+该税号监管条件核验,TIME_SENSITIVE)']
- **AB-260904-G05**：BLOCKED=['绑扎方式/破断强度/车头朝向/胎压调整具体值(无OEM运输手册或船公司正式指南前为items to confirm with carrier/OEM)', '统一SOC固定百分比(仅获Höegh一家,不得泛化)']
- **AB-260904-G06**：BLOCKED=['海外Euro/EPA限值与EN燃油规格精确数值', '国六与海外标准等效性结论']
- **AB-260904-G10**：BLOCKED=['任何具体金额(如小柜/大柜THC人民币数、报关费区间)均为T4旧值或市场波动值,一律不得写成当前确定收费', '不得据此估算AutoBridge到岸成本/利润(禁算)']

## 五、NEW_LESSON_CANDIDATE（仅候选，待独立审核，不自行写入永久规则）
- 专用车上装第三方型号高度混淆且无官网时直接换题而非CONDITIONAL（检测：fact出现≥2个不同型号代码即触发）。
- 卡车之家原创仅以今日头条镜像可检索时,Source Name可写卡车之家但domain如实填m.toutiao.com并降一级。

## 六、QA 结论
- 20个MAIN无FAIL、无未处理冲突、无占位URL、关键法规均有T1;5个CONDITIONAL带明确BLOCKED清单仍可写(WRITING_AI_READY=TRUE)。
- RESEARCH_QA = PASS（附CONDITIONAL边界）；Writing AI 须以 v1.1 Fact Sheet 为准，CONDITIONAL 包不得把BLOCKED内容写成确定事实。
