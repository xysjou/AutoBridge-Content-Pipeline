# RESEARCH SHEET (RE-RESEARCHED, CURRENT) — AB-260903-G08

ARTICLE_ID: AB-260903-G08
CONTENT_TYPE: PROCUREMENT_GUIDE
TOPIC: 非洲二手车进口车龄/舵向/检验门槛——仅保留有官方一手来源的国家（Kenya、Nigeria），其余不给硬数字
PRIMARY_KEYWORD: africa used car import age limit kenya nigeria official
SEARCH_INTENT: 用官方来源确定具体国家车龄计算基准、舵向限制与检验要求，并教采购者到官方核验
TARGET_READER: Importer / Dealer / Auto Trader / Procurement Manager
TARGET_SCOPE: Kenya（VERIFIED）、Nigeria（官方门户存在但含一处自相矛盾，CONDITIONAL）；其他非洲国家本轮无一手源 → 不写死数字
SUGGESTED_URL: /guides/africa-used-car-age-limits-kenya-nigeria/
OFFICIAL_SOURCE_AVAILABLE: PARTIAL（Kenya 全官方；Nigeria 官方门户+禁限清单文本）
RESEARCH_VERDICT: RESEARCH_CONDITIONAL（Kenya 可定案；Nigeria 以当前官方门户 15 年为准但须装运前复核；accuracy > coverage，其余国家删除硬数字）
RE_RESEARCH_DATE: 2026-09-04
RE_RESEARCH_TRIGGER: R4 P0（Kenya KRA/KEBS、Nigeria Trade Portal/Customs 一手源；找不到官方允许删国家）

## USER PROBLEM
采购者拿到的“非洲车龄表”数字互相矛盾（肯 7/8、尼日 10/12/15），且常把“制造年/首次登记年”混用，导致到港退运。

## KENYA（官方可定案）

### FACT K1
- Field: 车龄上限与计算基准
- Value: 自用二手乘用车自**首次登记年份(year of first registration)**起不得超过 **8 年**；且**首次登记年与制造年相差不得超过 1 年**。即 2026-01-01 起仅首次登记于 2019 年及以后的车辆可进
- Source: KRA 官方进口流程页 + KEBS 标准 DKS 1515:2025 / KS 1515:2000
- URL: https://www.kra.go.ke/individual/importing/learn-about-importation/procedures-for-motor-vehicle ; https://kebs.azurewebsites.net/wp-content/uploads/2025/05/DKS-1515_2025-Road-vehicles-%E2%80%94-Inspection-of-road-vehicles-%E2%80%94-Code-of-practice_.pdf
- Source Scope: Kenya 税务机关(KRA) + 标准局(KEBS)，T1 PRIMARY
- Checked Date: 2026-09-04
- Confidence: VERIFIED

### FACT K2
- Field: 法规/标准依据
- Value: Legal Notice No.78 of 15 July 2005；道路车辆检验行为准则 KS 1515:2000（更新为 DKS 1515:2025）
- Source: KRA + KEBS
- URL: https://www.kra.go.ke/news-center/blog/1075-what-you-need-to-know-when-importing-a-motor-vehicle ; https://www.kebs.org/wp-content/uploads/2023/12/NOTICE-TO-IMPORTERS-OF-USED-SECONDHAND-MOTOR-VEHICLES.pdf
- Source Scope: Kenya 官方（T1）
- Checked Date: 2026-09-04
- Confidence: VERIFIED

### FACT K3
- Field: 舵向限制与例外
- Value: **禁止左舵(LHD)车辆在 Kenya 注册（右舵 RHD-only）**；救护车、消防车、大型工程车等特殊用途车辆为例外
- Source: KEBS DKS 1515:2025（§4.7.2 例外）+ KRA
- URL: https://kebs.azurewebsites.net/wp-content/uploads/2025/05/DKS-1515_2025-Road-vehicles-%E2%80%94-Inspection-of-road-vehicles-%E2%80%94-Code-of-practice_.pdf
- Source Scope: Kenya 标准局（T1）
- Checked Date: 2026-09-04
- Confidence: VERIFIED

## NIGERIA（官方门户 CONDITIONAL）

### FACT N1
- Field: 车龄上限与计算基准
- Value: Nigeria Single Window Trade Portal（HS 8702–8705）载明 **超过 15 年的车辆禁止进口**；Nigeria Customs 进口禁限清单文本（HS 8703.10.00–8703.90.0000）表述为“**自制造年份(year of manufacture)起超过 15 年**的二手机动车禁止进口”。注意：计算基准在官方语境为**制造年**（与 Kenya 的“首次登记年”不同）
- Source: Nigeria Single Window Trade Portal（.gov.ng 官方）+ Customs Import Prohibition List 文本
- URL: https://tip.nsw.gov.ng/procedures/automobiles
- Source Scope: Nigeria 官方单一窗口（T1）；禁限清单文本经法律事务所转载（辅助）
- Checked Date: 2026-09-04
- Confidence: CROSS_CHECKED（15 年/制造年：官方门户 + 禁限清单文本一致）；TIME_SENSITIVE（见 N3）

### FACT N2
- Field: 其他官方门户要素
- Value: 门户载明 HS 8702–8705、在关税之外另征 **National Automotive Council (NAC) levy**
- Source: Nigeria Single Window Trade Portal
- URL: https://tip.nsw.gov.ng/procedures/automobiles
- Source Scope: Nigeria 官方（T1）；具体税率不在本轮定案
- Checked Date: 2026-09-04
- Confidence: SINGLE_SOURCE（仅该门户），税费数字不写死

### FACT N3
- Field: 冲突与门户自相矛盾（BLOCKED）
- Value: (a) 同一官方门户页写 “Right-hand drive only permitted”，与 Nigeria 公认 **左舵(LHD)** 事实冲突，说明该页存在录入错误，**舵向不得仅凭此页下定论**；(b) 多家 2026 媒体称车龄收紧为 **12 年**（另有 10 年旧说法），但**均无 Nigeria Customs/官方一手文本**支持。故 12 年/10 年禁止写入正文
- Source: 官方门户 vs Legit/WheelZAR/234Drive/Carsooq/FIDI（T3/T4，冲突）
- URL: https://tip.nsw.gov.ng/procedures/automobiles
- Source Scope: 冲突证据
- Checked Date: 2026-09-04
- Confidence: CONFLICT

## TIME-SENSITIVE FACTS
- Nigeria 是否在 2026 把 15 年收紧为 12 年：无官方文本，装运前必须向 Nigeria Customs Service 复核（TIME_SENSITIVE）。
- Kenya “2019 及以后首次登记”的滚动年份每年 1 月 1 日变化。
- 两国税费/检验费金额本轮不定案。

## FACTS ALLOWED IN BODY
- Kenya：8 年、自首次登记年算、首登与制造相差≤1 年、RHD-only（特殊用途例外）、Legal Notice 78/2005、KS/DKS 1515、需装运前符合性检验（KEBS/QIE 路径可概述并链官方）。
- Nigeria：按当前官方单一窗口/禁限清单，二手乘用车(HS8703)自**制造年**起超过 15 年禁止进口；另征 NAC levy；**必须注明“以 Nigeria Customs 当期禁限清单为准、装运前复核”**。
- 方法论：先分“制造年 vs 首次登记年”，再查舵向，再查装运前检验，最后对官方禁限清单 HS 编码。

## FACTS NOT ALLOWED IN BODY
- Nigeria “12 年/10 年”任何确定表述（无一手源）。
- 仅凭 tip.nsw.gov.ng 该页写“Nigeria 只允许右舵”（与事实冲突，属门户错误）。
- 任何埃塞俄比亚、坦桑尼亚、乌干达等其他非洲国家的具体年限数字（本轮无一手源 → 删除，不给硬数字，只可提示“逐国向官方核验”）。
- 具体关税/VAT/levy 百分比、检验费金额（未一手定案）。
- 把 Kenya 的“首次登记年”基准套用到 Nigeria。

## UNRESOLVED QUESTIONS
- Nigeria Customs Service 官网(customs.gov.ng)当期 Import Prohibition List 原始 PDF/公告（用于彻底定案 15 vs 12 与舵向）——写作阶段如仍未取得，维持 CONDITIONAL 表述。
- 其他非洲国家：待后续逐国官方研究，本轮不补。
