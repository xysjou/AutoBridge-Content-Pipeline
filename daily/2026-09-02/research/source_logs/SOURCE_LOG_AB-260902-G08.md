# SOURCE LOG — AB-260902-G08 车机语言/OTA 本地化
**SOURCE_LOG_VERSION**: SL-v2-20260908-review-repair（2026-09-08 受控补源；OTA 监管补 MIIT/SAMR/gov.cn，国际框架补 UNECE R156；T1 官方且 scope 匹配方可 VERIFIED）

## SOURCE 01（T1 官方一手）
- Source Name: 工信部、市场监管总局《关于进一步加强智能网联汽车产品准入、召回及软件在线升级管理的通知》
- Organization: 工业和信息化部
- URL: https://www.miit.gov.cn/jgsj/zbys/wjfb/art/2025/art_fa604619ed45484386f37422d01f5527.html
- Source Tier/Type: T1 / government_primary
- Market: CN
- Source Scope: MATCHED
- Facts Supported: OTA 备案/报告、不得借 OTA 隐瞒缺陷或替代召回
- Checked Date: 2026-09-08
- Confidence: VERIFIED
- Official Source: YES

## SOURCE 02（T1 官方一手）
- Source Name: 市场监管总局 OTA 备案/召回官方解读
- Organization: 国家市场监督管理总局
- URL: https://www.samr.gov.cn:8007/zw/zfxxgk/fdzdgknr/zlfzs/art/2025/art_f2adade1d7e34eef801b095fdba71840.html
- Source Tier/Type: T1 / government_primary
- Market: CN
- Source Scope: MATCHED
- Facts Supported: OTA 备案系统、申报要素（IP/域名、ECU 版本、升级范围）
- Checked Date: 2026-09-08
- Confidence: VERIFIED
- Official Source: YES

## SOURCE 03（T1 官方收录）
- Source Name: 中国政府网政策库（智能网联准入/召回/OTA 管理）
- Organization: 中国政府网/国务院
- URL: https://www.gov.cn/zhengce/zhengceku/202503/content_7009422.htm
- Source Tier/Type: T1 / government_primary
- Market: CN
- Source Scope: MATCHED
- Facts Supported: 发布主体与监管要求交叉印证
- Checked Date: 2026-09-08
- Confidence: VERIFIED
- Official Source: YES

## SOURCE 04（T1 标准组织一手）
- Source Name: UNECE Regulation No.156（SUMS/SU 型式批准）
- Organization: United Nations Economic Commission for Europe (UNECE)
- URL: https://unece.org/sites/default/files/2021-03/R156e.pdf
- Source Tier/Type: T1 / standards_body_primary
- Market: INT（国际框架；逐国采纳另核）
- Source Scope: MATCHED（国际型式批准框架，不替代任一国家法规）
- Facts Supported: SUMS 软件更新管理体系、SU 型式批准、OTA 过程安全与告知义务
- Checked Date: 2026-09-08
- Confidence: VERIFIED
- Official Source: YES（标准组织）

## SOURCE 05（T3 行业站）
- Source Name: 2026 B2B Export Guide for Top Rated Chinese Car Brands（软件本地化章节）
- Organization: Electric Auto China
- URL: https://www.electricautochina.com/the-ultimate-2026-b2b-export-guide-for-top-rated-chinese-car-brands-pr/
- Source Tier/Type: T3 / industry_guide
- Market: CN→GLOBAL
- Source Scope: SUPPORTING
- Facts Supported: 自研车机默认中文、DiLink/SkyOS/Xmart OS
- Checked Date: 2026-09-02
- Confidence: SINGLE_SOURCE
- Official Source: NO

## SOURCE 06（T3 行业站；其"强制英文 HMI"主张被降级）
- Source Name: Chinese Car OS English Version B2B Export Guide
- Organization: Electric Auto China（与 SOURCE 05 同母机构归一）
- URL: https://www.electricautochina.com/the-ultimate-2026-b2b-export-guide-for-chinese-car-os-english-version/
- Source Tier/Type: T3 / industry_guide
- Market: CN→GLOBAL
- Source Scope: SUPPORTING；**"出口强制英文 HMI"无法规来源，已 BLOCKED**
- Facts Supported: 英文 HMI/刷机成本（行业口径，待官方核验）
- Checked Date: 2026-09-02
- Confidence: UNVERIFIED（该强制主张）
- Official Source: NO

## SOURCE 07（T3 服务商案例）
- Source Name: BYD Sea Lion 07 Ukraine Localization Case
- Organization: NEV Fix（车机本地化服务商）
- URL: https://nevfix.net/blog/byd-sealion-07-ukraine-localization-case.html
- Source Tier/Type: T3 / service_vendor_case
- Market: CN→多国
- Source Scope: SUPPORTING（单一案例，非品牌通则）
- Facts Supported: 平行进口仅中文 UI/中国地图/无主账号；BYD 主账号切英文（个案）
- Checked Date: 2026-09-02
- Confidence: SINGLE_SOURCE
- Official Source: NO

## SOURCE 08（T3 汽车媒体）
- Source Name: 中国汽车出海，智能化为何"水土不服"
- Organization: 汽车之家·车家号
- URL: https://chejiahao.m.autohome.com.cn/info/26145241?isfrom=pc
- Source Tier/Type: T3 / auto_media
- Market: CN→EU
- Source Scope: SUPPORTING
- Facts Supported: 海外用户 UI 翻译/手机互联问题
- Checked Date: 2026-09-02
- Confidence: CROSS_CHECKED
- Official Source: NO

## SOURCE 09（T3 财经社区转引）
- Source Name: 腾势 Z 海外适配 Google Gemini（国内外两套座舱方案）
- Organization: 雪球（转引官方发布）
- URL: https://xueqiu.com/9837237227/399831947
- Source Tier/Type: T3 / finance_community_repost
- Market: CN→EU
- Source Scope: SUPPORTING（须以品牌官方为准）
- Facts Supported: 出口版 Android Automotive/Google built-in vs 国内自研
- Checked Date: 2026-09-02
- Confidence: SINGLE_SOURCE
- Official Source: NO

## SOURCE 10（T3 出口服务商）
- Source Name: Making Chinese EV Software Work Locally
- Organization: StarVia Auto
- URL: https://www.starviaauto.com/en/blog/making-chinese-ev-software-work-locally
- Source Tier/Type: T3 / export_vendor_checklist
- Market: CN→GLOBAL
- Source Scope: SUPPORTING（方法清单）
- Facts Supported: 语言/导航/手机互联/App/OTA 核验清单
- Checked Date: 2026-09-02
- Confidence: SINGLE_SOURCE
- Official Source: NO

## SOURCE 11（T3 行业媒体）
- Source Name: 东软 OneCoreGo 多语言出海标准
- Organization: 赛迪网（CCID）
- URL: http://www.ccidnet.com/hlw/93237.jhtml
- Source Tier/Type: T3 / industry_media
- Market: GLOBAL
- Source Scope: SUPPORTING
- Facts Supported: RTL 阿拉伯语布局适配、区域法规定制（行业方案示例）
- Checked Date: 2026-09-02
- Confidence: SINGLE_SOURCE
- Official Source: NO

**归一化与完整性说明**：Electric Auto China 两页=1 母机构；车家号=汽车之家。Source Name 与 URL 主体一致，无 .example/localhost 占位。去重后独立 URL=11，SOURCE_ORG_COUNT_NORMALIZED=10。OTA 监管与 R156 国际框架由 T1 直接支持，"强制英文 HMI"等无法规来源主张已 BLOCKED，CLAIM_TRACEABILITY=PASS。
