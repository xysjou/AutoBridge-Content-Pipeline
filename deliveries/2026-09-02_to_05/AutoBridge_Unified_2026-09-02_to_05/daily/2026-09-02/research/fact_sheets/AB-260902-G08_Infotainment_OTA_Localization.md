# RESEARCH SHEET — AB-260902-G08

- **ARTICLE_ID**: AB-260902-G08
- **CONTENT_TYPE**: PROCUREMENT_GUIDE
- **TOPIC**: 中国车出口的车机语言、导航、App 与 OTA 海外适配
- **PRIMARY_KEYWORD**: Chinese car infotainment English language OTA overseas localization
- **SEARCH_INTENT**: 进口商确认中国版车机在海外能否切换语言、使用本地导航/App、接收 OTA
- **TARGET_READER**: 平行进口商、海外经销商、车队运营方
- **TARGET_COUNTRY / REGION**: 全球（中国车出口/平行进口）
- **SUGGESTED_URL**: /guides/chinese-car-infotainment-ota-localization/
- **USER PROBLEM**: 中国本土版车机以中文为主、导航为中国地图、应用商店只有中国 App、车联网账号与 OTA 服务器在境内，车辆到海外后出现语言不通、导航不可用、手机互联不稳、OTA 无法升级等问题，买家需在采购前判断并制定适配方案。
- **历史去重**: 历史库无"车机语言/OTA/软件本地化"主题，搜索意图不重复。

## VERIFIED FACTS
| Fact | Source | URL | Checked | Confidence |
|------|--------|-----|---------|-----------|
| 中国主流品牌车机多为自研 Android 系统（BYD DiLink、NIO SkyOS、小鹏 Xmart OS 等），默认中文语言层，本土生态面向中文用户 | Electric Auto China（行业站） | https://www.electricautochina.com/the-ultimate-2026-b2b-export-guide-for-top-rated-chinese-car-brands-pr/ | 2026-09-02 | SINGLE_SOURCE |
| 平行进口中国 EV 在乌克兰、俄、哈、阿联酋、沙特、巴西、泰国等市场常出现仅中文 UI、中国地图导航、无主账号访问权限等问题 | NEV Fix（行业服务商） | https://nevfix.net/blog/byd-sealion-07-ukraine-localization-case.html | 2026-09-02 | SINGLE_SOURCE |
| BYD 部分车型可通过主账号（master account）免费切换英文 UI，无需硬件；完整小语种本地化需专门处理 | NEV Fix（行业服务商） | https://nevfix.net/blog/byd-sealion-07-ukraine-localization-case.html | 2026-09-02 | SINGLE_SOURCE |
| 海外用户集中反馈：UI 翻译生硬/拼写错误、排版混乱、按钮含义模糊，数字钥匙、Android Auto/CarPlay、导航、辅助驾驶连接不稳 | 车家号（汽车之家）/火猫网络 | https://chejiahao.m.autohome.com.cn/info/26145241?isfrom=pc | 2026-09-02 | CROSS_CHECKED |
| 出口版与本土版软件方案不同：如腾势 Z 欧洲版基于 Android Automotive（Google built-in）并内置 Gemini，国内版用自研 DiLink + 璇玑大模型 | 雪球（转引官方发布） | https://xueqiu.com/9837237227/399831947 | 2026-09-02 | SINGLE_SOURCE |
| 进口商应逐项核验：系统语言、本地导航地图/充电点覆盖、手机互联（CarPlay/Android Auto）、官方 App 在目标国可用性与账号/服务器接入、OTA 海外可达性 | StarVia Auto（出口服务商） | https://www.starviaauto.com/en/blog/making-chinese-ev-software-work-locally | 2026-09-02 | SINGLE_SOURCE |
| 车机多语言出海标准覆盖英语/法语/西语及阿拉伯语等 RTL 从右向左书写方向的语法与布局适配（以东软 OneCoreGo 行业方案为例） | 赛迪网 | http://www.ccidnet.com/hlw/93237.jhtml | 2026-09-02 | SINGLE_SOURCE |

## TIME-SENSITIVE FACTS
- **2026 出口许可对英文 HMI 的要求（出口检验需展示英文界面截图）**：URL: https://www.electricautochina.com/the-ultimate-2026-b2b-export-guide-for-chinese-car-os-english-version/ ；日期：2026；适用：中国出口侧（行业站口径，须以海关/商务部官方要求核验）。
- **各品牌 OTA/车机版本更新频繁**：URL: https://www.starviaauto.com/en/blog/making-chinese-ev-software-work-locally ；日期：2026；适用：全球（以品牌官方海外版本为准）。

## UNRESOLVED QUESTIONS
- "2026 出口检验强制英文 HMI"目前仅行业站口径，须以海关/商务部官方文件核验，写作时不写成既定法规。
- 各品牌（BYD/吉利/长安/长城等）出口版车机语言清单与 OTA 服务器区域策略未逐一取得官方说明，写作给方法论与检查清单，不逐品牌下结论。
- 第三方刷机/改机的合规性与质保影响未获官方立场，须提示风险（可能失去质保/违反当地无线电与软件合规）。
