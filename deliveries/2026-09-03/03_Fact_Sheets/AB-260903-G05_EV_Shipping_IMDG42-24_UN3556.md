# RESEARCH SHEET (RE-RESEARCHED, CURRENT) — AB-260903-G05
# Supersedes AB-260903-G05_EV_Shipping_UN3171_IMDG.md (old IMDG 40-20 / blanket-UN3171 basis)

ARTICLE_ID: AB-260903-G05
CONTENT_TYPE: PROCUREMENT_GUIDE
TOPIC: 电动/混动车辆海运危险品合规（IMDG Code Amendment 42-24：UN3556/3557/3558、SP961/962）
PRIMARY_KEYWORD: ev shipping un3556 imdg 42-24 compliance
SEARCH_INTENT: 指导出口商按当前 IMDG 42-24 正确分类、备单、标记并满足船公司层要求
TARGET_READER: Importer / Dealer / Fleet Buyer / Procurement Manager / 货代订舱
TARGET_SCOPE: 全球海运（ocean），对照公路 ADR/RID 仅作区分
SUGGESTED_URL: /guides/ev-shipping-un3556-imdg-compliance/
OFFICIAL_SOURCE_AVAILABLE: YES (IMO primary for version/effective date)
RESEARCH_VERDICT: RESEARCH_PASS (core classification/SP facts primary+cross-checked; carrier SOC layer kept TIME_SENSITIVE)
CURRENT_VERSION: IMDG Code, 2024 Edition incorporating Amendment 42-24
CURRENT_AMENDMENT: 42-24
EFFECTIVE_DATE / MANDATORY_FROM: voluntary from 2025-01-01; **MANDATORY FROM 2026-01-01** (sea transition off UN3171 ended 2025-12-31)
RE_RESEARCH_DATE: 2026-09-04
RE_RESEARCH_TRIGGER: R4 P0 + CURRENT_STANDARD_VERSION_GATE + DEPENDENCY_UPDATE_PROPAGATION

## USER PROBLEM
出口商仍按旧版把所有锂电整车统一写成 UN3171；需要知道 42-24 下正确 UN 编号、SP961/962 豁免与全套要求边界、集装箱/RoRo 差异、UN38.3、标记标牌、以及哪些是船公司层要求。

## VERIFIED / GRADED FACTS (Reference scope = global ocean, IMDG 42-24)

### FACT 01
- Field: 当前版本与强制日期
- Value: IMDG Code 2024 Edition（含 Amendment 42-24）自 2026-01-01 起强制；2025 为过渡年（可在 41-22 与 42-24 间一致选用其一）
- Source: International Maritime Organization (IMO) 官方 IMDG Code 页
- URL: https://www.imo.org/en/publications/pages/imdg%20code.aspx
- Source Scope: 全球海运，规则发布机构本身（T1 PRIMARY）
- Checked Date: 2026-09-04
- Confidence: VERIFIED

### FACT 02
- Field: 锂电整车正确 UN 编号
- Value: **UN3556 VEHICLE, LITHIUM ION BATTERY POWERED，Class 9，危险标签 Label 9A**；旧的通用 UN3171（BATTERY-POWERED VEHICLE）对普通锂离子电池驱动车辆自 2026-01-01 起不再是当前分类（海运允许沿用至 2025-12-31）
- Source: IMO（版本/日期，VERIFIED）+ Maersk 42-24 客户通告 + DG 专业指南（编号/标签，CROSS_CHECKED）
- URL: https://www.imo.org/en/publications/pages/imdg%20code.aspx ; https://www.maersk.com.cn/~/media_sc9/maersk/local-information/files/asia-pacific/japan/export/advisory---others-and-document/maersk-customer-advisory-regulatory-changes-imdg-code-amendment-42-24-japanese.pdf ; https://sakerhetsradgivarna.se/farligt-gods/guide/un-3556-adr-rid-imdg
- Source Scope: 全球海运；UN 编号/标签由两家独立专业来源一致，版本日期为 IMO 一手
- Checked Date: 2026-09-04
- Confidence: VERIFIED (编号映射经 owner 永久规则 CURRENT_STANDARD_VERSION_GATE 确认；标签/过渡细节 CROSS_CHECKED)

### FACT 03
- Field: 并列新增车辆 UN 编号
- Value: **UN3557 VEHICLE, LITHIUM METAL BATTERY POWERED；UN3558 VEHICLE, SODIUM-ION BATTERY POWERED**，同为 Class 9，与 UN3556 并列，从旧 UN3171 中按电池化学体系拆出
- Source: DG 专业指南 + 42-24 解读（两家一致）
- URL: https://sakerhetsradgivarna.se/farligt-gods/guide/un-3556-adr-rid-imdg ; https://shashikallada.com/wp-content/uploads/2026/07/Ebook-Shipping-Vehicles-Under-IMDG-Code-Amendment-42-24.pdf
- Source Scope: 全球海运（T3 两源一致，无 IMO 免费全文逐条；编号体系与 FACT02 同源）
- Checked Date: 2026-09-04
- Confidence: CROSS_CHECKED

### FACT 04
- Field: SP961（IMDG 专属，豁免路径）
- Value: 满足 SP961 条件（典型：车辆以自身动力开上/开下 RoRo 船并停放于车辆处所/特殊类别处所/RoRo 处所/露天甲板，或主管机关按 SOLAS II-2/Reg.20 指定的货物处所，且电池无泄漏迹象）时，**无需标记、标签、标牌、危险品申报单(DGD)及额外特殊操作**。SP961.1 **不适用于装在集装箱内的车辆**——集装箱车辆改走 SP962
- Source: DG 专业指南（SP 条文整理）+ Maersk 通告（SP962 标牌变更侧面印证）
- URL: https://sakerhetsradgivarna.se/farligt-gods/guide/un-3556-adr-rid-imdg
- Source Scope: 海运 IMDG 专属（公路对应 SP666，编号不同，不可混用）
- Checked Date: 2026-09-04
- Confidence: CROSS_CHECKED

### FACT 05
- Field: SP962（IMDG 专属，不满足 SP961 时的全套 Class 9 要求）
- Value: 不满足 SP961（含**集装箱装载整车**这一中国出口最常见情形）时按 Class 9 全套：电池无泄漏、符合 SP388、防损/防短路/防意外启动；**需要 DGD**；**积载类别 A**；**人员须按 1.3 章培训**；仅当车辆被包装/板条箱完全包覆、无法直接识别时才适用 5.2 包件标记标签（标 “UN3556 VEHICLE, LITHIUM ION BATTERY POWERED” + 9A 标签）与 5.3 货物运输单元标牌（Placard No.9；单一 UN3556 且毛重>4000kg 还须显示 “UN3556”）
- Source: DG 专业指南 + Maersk 42-24 通告（SP962 标牌）
- URL: https://sakerhetsradgivarna.se/farligt-gods/guide/un-3556-adr-rid-imdg ; https://www.maersk.com.cn/~/media_sc9/maersk/local-information/files/asia-pacific/japan/export/advisory---others-and-document/maersk-customer-advisory-regulatory-changes-imdg-code-amendment-42-24-japanese.pdf
- Source Scope: 海运 IMDG 专属
- Checked Date: 2026-09-04
- Confidence: CROSS_CHECKED

### FACT 06
- Field: UN38.3 适用性
- Value: 车辆内安装的锂电池须满足《联合国试验和标准手册》第 38.3 节（UN38.3）测试；**例外**：预生产原型、或产量≤100 台且装车用于测试的电池可不受此限
- Source: DG 专业指南（引 UN Manual of Tests & Criteria 38.3）
- URL: https://sakerhetsradgivarna.se/farligt-gods/guide/un-3556-adr-rid-imdg
- Source Scope: 全球（UN 模型条例层面，海运/公路一致）
- Checked Date: 2026-09-04
- Confidence: CROSS_CHECKED

### FACT 07
- Field: 受损/缺陷电池车辆
- Value: **UN3556（及 SP961 豁免）不覆盖受损/缺陷锂电池车辆**；此类货物不享受 SP961 豁免，须按受损/缺陷电池专门条款并结合主管机关/船公司条件运输（可能要求特殊批准、特殊包装与路线）。禁止把 UN3556 描述成“受损/缺陷电池分类”
- Source: DG 专业指南 + 42-24 解读
- URL: https://sakerhetsradgivarna.se/farligt-gods/guide/un-3556-adr-rid-imdg
- Source Scope: 全球海运
- Checked Date: 2026-09-04
- Confidence: CROSS_CHECKED

### FACT 08
- Field: SOC（电量）要求层级
- Value: **IMDG 42-24 的 SP961/962 本身不设统一的固定电量百分比上限**；具体 SOC 上限、断电/防启动操作、端子保护等属于**船公司(carrier-specific)订舱层规则**，因 Maersk/MSC/CMA 等而异，订舱前必须以承运船公司当期危险品规则为准
- Source: 多家货代/船公司通告一致（无统一法定数值）
- URL: https://www.topwayshipping.com/dangerous-goods-on-china-uae-routes-2026-imdg-compliance-checklist-before-you-load/
- Source Scope: 船公司层（非 IMDG 法定统一值）
- Checked Date: 2026-09-04
- Confidence: CROSS_CHECKED (boundary fact: “无统一法定SOC%” )；任何具体百分比 = TIME_SENSITIVE 且须船公司确认

## TIME-SENSITIVE FACTS
- 船公司各自 SOC 上限、DGD 格式、订舱截止、是否接受集装箱 EV、堆场危品操作要求：适用=各船公司航线，Checked 2026-09-04，写作/订舱当日须复核。
- IMDG 两年一改版；下一周期前引用须再次核对 CURRENT_VERSION。

## FACTS ALLOWED IN BODY（可作为事实写入正文）
- 42-24 自 2026-01-01 强制、2025 过渡、海运 UN3171 沿用截至 2025-12-31（IMO 一手）。
- 普通锂离子电池驱动整车 = UN3556，Class 9，Label 9A；锂金属=UN3557；钠离子=UN3558。
- SP961 豁免条件与“集装箱内车辆不适用、改走 SP962”；SP962 下 DGD/积载A/1.3培训/5.2+5.3 标记标牌触发条件（完全包覆才需要）。
- UN38.3 安装电池要求及≤100台/原型例外。
- 受损/缺陷车辆不属 UN3556 豁免，走专门条款+主管机关/船公司条件。
- IMDG 不设统一 SOC%，SOC 属船公司层。
- 公路 ADR/RID 编号不同（SP666；ADR 的 UN3171 过渡截至 2025-06-30），可用于区分、不可与海运混用。

## FACTS NOT ALLOWED IN BODY（无一手/超范围，禁止写成事实）
- 任何“IMDG 统一规定 SOC≤30%（或其他固定百分比）”的说法——无条文，属船公司层。
- 把 UN3556 写成受损/缺陷电池条目。
- 把 2026-01-01 后普通锂电整车继续统称 UN3171。
- 未经官方全文逐条核验的 SP 子条款编号细节（如 SP961.2–961.6 对 UN3556 的具体适用争议）只能写“存在解释分歧、从严按 SP962”，不得下定论。
- 任何海运费、危品附加费、保险费率数字。

## UNRESOLVED QUESTIONS（写作阶段不得自行补写）
- 各船公司当期 SOC 上限与单证模板——留作“订舱前向承运人确认”。
- SP666(e)/SP961 在 CTU 载运情形的解释分歧——从严建议 SP962，不替主管机关下结论。
