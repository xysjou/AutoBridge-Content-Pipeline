# RESEARCH SHEET — AB-260902-G08

- **ARTICLE_ID**: AB-260902-G08
- **CONTENT_TYPE**: PROCUREMENT_GUIDE
- **TOPIC**: 中国车出口的车机语言、导航、App 与 OTA 海外适配
- **PRIMARY_KEYWORD**: Chinese car infotainment English language OTA overseas localization
- **SEARCH_INTENT**: 进口商确认中国版车机在海外能否切换语言、使用本地导航/App、接收 OTA
- **TARGET_READER**: 平行进口商、海外经销商、车队运营方
- **TARGET_COUNTRY / REGION**: 全球（中国车出口/平行进口）
- **SUGGESTED_URL**: /guides/chinese-car-infotainment-ota-localization/
- **FACT_SHEET_VERSION**: FS-v2-20260908-review-repair（2026-09-08 依独立 Review 基线 4b446ab 做 SOURCE_SCOPE/CLAIM_TRACEABILITY 受控补源；OTA 监管与国际型式批准框架补 T1 一手）
- **USER PROBLEM**: 中国本土版车机以中文为主、导航为中国地图、应用商店只有中国 App、车联网账号与 OTA 服务器在境内，车辆到海外后出现语言不通、导航不可用、手机互联不稳、OTA 无法升级等问题，买家需在采购前判断并制定适配方案。
- **历史去重**: 历史库无"车机语言/OTA/软件本地化"主题，搜索意图不重复。

## VERIFIED FACTS（官方/标准一手，scope 匹配）
| Fact | Source | URL | Checked | Confidence |
|------|--------|-----|---------|-----------|
| 智能网联汽车 OTA（软件在线升级）实行备案/报告管理：企业开展 OTA 应按规定向工业和信息化、市场监管等主管部门备案，不得通过 OTA 隐瞒已备案车辆存在的缺陷或替代召回 | 工业和信息化部、国家市场监督管理总局《关于进一步加强智能网联汽车产品准入、召回及软件在线升级管理的通知》 | https://www.miit.gov.cn/jgsj/zbys/wjfb/art/2025/art_fa604619ed45484386f37422d01f5527.html | 2026-09-08 | VERIFIED |
| OTA 备案系统与申报要素（IP/域名、ECU 软硬件版本、升级范围与影响）的官方监管口径 | 国家市场监督管理总局（缺陷调查中心/召回管理）官方解读 | https://www.samr.gov.cn:8007/zw/zfxxgk/fdzdgknr/zlfzs/art/2025/art_f2adade1d7e34eef801b095fdba71840.html | 2026-09-08 | VERIFIED |
| 上述 OTA/智能网联准入与召回管理要求的中国政府网政策库收录文本（交叉印证发布主体与要求） | 中国政府网 | https://www.gov.cn/zhengce/zhengceku/202503/content_7009422.htm | 2026-09-08 | VERIFIED |
| 出口市场侧：联合国 UNECE R156 确立软件更新管理体系（SUMS）与软件更新（SU）型式批准框架，要求制造商建立 SUMS 并对 OTA 过程、车辆功能安全与告知义务负责（用于说明出口目的国/区域型式批准对 OTA 的合规要求） | UNECE 联合国欧洲经济委员会 R156 正式法规文本（标准组织一手） | https://unece.org/sites/default/files/2021-03/R156e.pdf | 2026-09-08 | VERIFIED（国际标准框架；具体国别是否采纳 R156 须逐国确认） |

## SUPPORTING FACTS（行业/媒体，市场现象与方法层）
| Fact | Source | URL | Checked | Confidence |
|------|--------|-----|---------|-----------|
| 中国主流品牌车机多为自研系统（BYD DiLink、NIO SkyOS、小鹏 Xmart OS 等），默认中文、本土生态面向中文用户 | Electric Auto China（行业站） | https://www.electricautochina.com/the-ultimate-2026-b2b-export-guide-for-top-rated-chinese-car-brands-pr/ | 2026-09-02 | SINGLE_SOURCE |
| 平行进口中国 EV 在乌、俄、哈、阿联酋、沙特、巴西、泰等市场常出现仅中文 UI、中国地图、无主账号权限等问题 | NEV Fix（本地化服务商案例） | https://nevfix.net/blog/byd-sealion-07-ukraine-localization-case.html | 2026-09-02 | SINGLE_SOURCE |
| BYD 部分车型可通过主账号（master account）免费切换英文 UI，无需硬件；完整小语种本地化需专门处理（单一服务商案例，非品牌官方通则） | NEV Fix | https://nevfix.net/blog/byd-sealion-07-ukraine-localization-case.html | 2026-09-02 | SINGLE_SOURCE |
| 海外用户反馈 UI 翻译生硬、排版混乱、数字钥匙/Android Auto/CarPlay/导航/辅助驾驶连接不稳 | 汽车之家·车家号 | https://chejiahao.m.autohome.com.cn/info/26145241?isfrom=pc | 2026-09-02 | CROSS_CHECKED |
| 出口版与本土版软件方案不同（如腾势 Z 欧洲版基于 Android Automotive / Google built-in，国内版自研）——财经社区转引官方发布，须以品牌官方为准 | 雪球 | https://xueqiu.com/9837237227/399831947 | 2026-09-02 | SINGLE_SOURCE |
| 进口商逐项核验清单：系统语言、本地导航/充电点、CarPlay/Android Auto、官方 App 目标国可用与账号/服务器接入、OTA 海外可达性 | StarVia Auto（出口服务商） | https://www.starviaauto.com/en/blog/making-chinese-ev-software-work-locally | 2026-09-02 | SINGLE_SOURCE |
| 多语言出海覆盖英/法/西及阿拉伯语等 RTL 布局适配（以东软 OneCoreGo 行业方案为例） | 赛迪网 | http://www.ccidnet.com/hlw/93237.jhtml | 2026-09-02 | SINGLE_SOURCE |

## FACTS_ALLOWED_IN_BODY（可写成确定事实）
- 中国侧 OTA 备案/报告、不得借 OTA 隐瞒缺陷或替代召回（VERIFIED，MIIT+SAMR+gov.cn）。
- 出口市场 SUMS/SU 型式批准框架由 UNECE R156 确立（VERIFIED 国际框架；逐国采纳情况另行确认）。
- 中国本土版车机默认中文/中国地图/本土应用生态、海外可能受限（行业现象，表述为"常见/可能"，多源支撑）。
- 采购前软件/OTA 核验清单（方法层，建议性质）。

## FACTS_NOT_ALLOWED_IN_BODY / BLOCKED_FACTS
- **"2026 出口检验强制英文 HMI / 必须提供英文界面截图"**：仅 Electric Auto China 行业站口径，未取得海关/商务部官方文件，**不得写成中国出口法定强制要求**，保持 UNVERIFIED。来源：https://www.electricautochina.com/the-ultimate-2026-b2b-export-guide-for-chinese-car-os-english-version/
- "BYD 主账号可免费切英文"为单一服务商案例，不得推广为所有品牌通则。
- 腾势 Z 海外 Android Automotive 方案为社区转引，须以品牌官方为准，不作确定结论。
- 逐品牌（BYD/吉利/长安/长城等）出口版语言清单与 OTA 服务器区域策略（未逐一取得官方）。
- 第三方刷机/改机的合规与质保后果（无官方立场，仅作风险提示）。
- 某一具体国家是否强制采纳 R156/SUMS（须逐国官方源）。

## TIME-SENSITIVE FACTS
- OTA 备案/召回监管口径、各品牌 OTA 与车机版本、出口目的国型式批准采纳情况：动态变化，2026-09-08 核验。

## CONFLICT_LIST
- 无来源间直接数值冲突；行业站"出口强制英文 HMI"与官方缺口之间为证据等级问题，已按 BLOCKED 处理。

## UNRESOLVED QUESTIONS
- "2026 出口检验强制英文 HMI"须海关/商务部官方文件核验前不写成法规。
- 逐品牌官方语言清单/OTA 区域策略、第三方刷机合规性。

## SOURCE GATE（发布级）
- SOURCE_URL_COUNT = 11；SOURCE_ORG_COUNT_NORMALIZED = 10（工信部、市场监管总局、中国政府网、UNECE、Electric Auto China、NEV Fix、汽车之家、雪球、StarVia、赛迪网）。
- 官方/标准一手（T1）= MIIT、SAMR、gov.cn、UNECE R156；其余为 T3 行业/媒体。
- RESEARCH_STATUS = RESEARCH_PASS（核心监管事实与国际型式批准框架由一手来源 VERIFIED；行业主张中无法规来源者已显式 BLOCKED）。
- WRITING_AI_READY = TRUE。
