# RESEARCH REMEDIATION HANDOFF — batch 2026-09-03 (executed 2026-09-04)

STATUS: **RESEARCH_REMEDIATION_COMPLETE**
SCOPE: G01, G02, G03, G05, G08, G10 (current-batch fix; NOT deferred)
RULE APPLIED: RULE_INSTALLATION_DOES_NOT_COMPLETE_CURRENT_TASK — writing a lesson does not complete the batch; current Fact Sheets / Source Logs / status / handoff are all updated now.
BODY ARTICLES: NOT rewritten in this stage (Writing AI R5 only; gated by WRITING_AI_READY and the per-sheet FACTS_ALLOWED/NOT_ALLOWED lists).
CHECKED DATE for all new facts: 2026-09-04.

Per-article confidence uses the PART-1 tiers: T1 = OEM/government/customs/tax/standards/UNECE/official legal DB with matching SOURCE_SCOPE; media agreement never auto-VERIFIED.

---

## AB-260903-G01 — China Vehicle Export Licence
PRIMARY_SOURCES_ADDED:
- 商务部等四部门 **2025年第54号公告**（MOFCOM 官方公告页）https://www.mofcom.gov.cn/zcfb/blgg/gg/2025/art/2025/art_b483d5aaebbb46e1999748d569d1ca99.html （+外贸司/许可证局两处官方镜像）
- **2026年度汽车和摩托车出口许可申报通知**（商务部外贸司）https://wms.mofcom.gov.cn/zcfb/wmgl/art/2025/art_4fffefa930ec42c1875859eac89ff1e4.html
- 复用既有 gov.cn 二手车通知、工信部令第50号（REUSE_STRONGEST_VERIFIED_SOURCE）。
CORE_FACTS_VERIFIED: 54号公告=四部门、2025-09-26、2026-01-01 施行、对象为仅装驱动电机且带 VIN 的载人车辆、参考 HS 8703801090、实施出口许可证管理（VERIFIED）；二手车许可证与≤180天售后确认书（VERIFIED）；六类企业/产品准入（VERIFIED）。
BLOCKED_FACTS: 移除 Toutiao/每日经济新闻作为核心法规依据；不写死当年税则十位编码监管条件；不外推到全部新能源/商用车（HS_FIRST）；无来源的配额/名单/办理时长数字禁用。
RESEARCH_STATUS: **RESEARCH_PASS**
WRITING_AI_READY: **TRUE**

## AB-260903-G02 — UAE Import / Registration
PRIMARY_SOURCES_ADDED:
- Dubai Customs 官方英文清关页（5% duty、invoice/PL/B-L/ID）https://www.dubaicustoms.gov.ae/en/eServices/ServicesForIndividuals/Pages/ClearanceOfPersonalEffects.aspx
- Dubai Customs 二手折旧估价官方 PDF；
- **UAE Federal Tax Authority** VATGEC1（进口 VAT 5%，计税基础=CIF+关税）tax.gov.ae；
- **UAE 联邦政府门户 u.ae** 车辆注册单证页（海关证明/转让/出口/占有凭证 + Emirates ID/护照/保险）；
- **MoIAT** UAE CoC/ECAS 官方服务页 https://www.moiat.gov.ae/en/services/issue-conformity-certificates-for-regulated-products ；**GSO** 机动车技术法规清单（Euro6b 节点）。
CORE_FACTS_VERIFIED: 清关 5% 关税（Dubai Customs，VERIFIED）；进口 VAT 5%、CIF+关税基础（FTA，VERIFIED）；注册单证类别（u.ae，VERIFIED）；MoIAT 承继 ESMA 发 UAE CoC、GSO 定 GCC 法规（VERIFIED）；清关→VCC→合规→检测→保险→RTA(Mulkiya) 顺序。
BLOCKED_FACTS: 写死的注册/牌照/检测费金额；把轻型车税率外推商用卡车（HS_FIRST）；把 MoIAT CoC 当 RTA 注册；媒体“10 年车龄”当法规。
RESEARCH_STATUS: **RESEARCH_PASS**（规费金额 TIME_SENSITIVE，不写死）
WRITING_AI_READY: **TRUE**

## AB-260903-G03 — CoC / Type Approval
PRIMARY_SOURCES_ADDED:
- **EUR-Lex Reg.(EU) 2018/858** 合并版 + 原版（WVTA；Art.36 制造商每车 CoC）；
- **UNECE 1958 Agreement Rev.3** 官方 PDF + GRRF-84-18 批准标记 + 1958 状态页；
- **EAEU TR CU 018/2011 = Customs Union Commission Decision No.877 (2011-12-09)**，哈萨克斯坦司法部官方法律库 adilet.zan.kz（注明经 EEC 2018-12-25 №219 更新）。
CORE_FACTS_VERIFIED（严格分立，禁止互替）: WVTA=欧盟车型批准；CoC=制造商为每辆已批准车型车辆出具的随车证书（非批准本身）；UNECE e/E-mark=零部件/系统/STU 级批准（E+缔约方号），≠整车 WVTA、≠CoC；OTTS=EAEU 车型批准文书，EAC=欧亚合格标志，二者不同且不与欧盟文件互换。
BLOCKED_FACTS: “有 E-mark=整车批准/可欧盟注册”；“EAC=OTTS”；未核当前修订版写死 TR CU 018 条款号；认证商(T3)办理周期/费用当法定要求；中国出厂合格证=目的国 CoC。
RESEARCH_STATUS: **RESEARCH_PASS**（EAEU 当前合并版直链 TIME_SENSITIVE，以决定号877+成员方官方法律库定案）
WRITING_AI_READY: **TRUE**

## AB-260903-G05 — EV Shipping (re-based to IMDG 42-24)
PRIMARY_SOURCES_ADDED:
- **IMO 官方 IMDG Code 页**（2024 Edition / Amendment 42-24 / mandatory 2026-01-01）https://www.imo.org/en/publications/pages/imdg%20code.aspx
- Maersk 42-24 客户通告（承运人层）；DG 专业指南（SP961/962、UN38.3）；IMDG42-24 eBook（UN3557/3558）。
- 新建 Fact Sheet `AB-260903-G05_EV_Shipping_IMDG42-24_UN3556.md`；旧 UN3171/40-20 sheet 标注 **SUPERSEDED**；新 Source Log `SOURCE_LOG_AB-260903-G05_IMDG42-24.md`；新 slug `/guides/ev-shipping-un3556-imdg-compliance/`。
CORE_FACTS_VERIFIED: 42-24 自 2026-01-01 强制、海运 UN3171 过渡截至 2025-12-31（IMO VERIFIED）；普通锂电整车=**UN3556** Class9/Label9A，锂金属=**UN3557**，钠离子=**UN3558**；SP961=满足条件（如自开上/下 RoRo、指定处所、无泄漏）豁免标记/标牌/DGD，**集装箱内车辆不适用、改 SP962**；SP962=全套 Class9（DGD、积载A、1.3培训，完全包覆才触发5.2/5.3标记标牌）；UN38.3 及≤100台/原型例外；**UN3556 不覆盖受损/缺陷电池**。
BLOCKED_FACTS: “IMDG 统一 SOC≤X%”（无法定统一值，属船公司层）；把 UN3556 写成受损/缺陷分类；2026 后继续统称 UN3171；任何危品附加费/海运费数字；对 SP961 在 CTU 情形的解释分歧下定论（从严按 SP962）。
RESEARCH_STATUS: **RESEARCH_PASS**（版本/日期 VERIFIED；SP 机制两独立来源 CROSS_CHECKED；carrier SOC=TIME_SENSITIVE）
WRITING_AI_READY: **TRUE**

## AB-260903-G08 — Africa Used-Car Age Limits
PRIMARY_SOURCES_ADDED:
- **Kenya KRA** 进口流程/指南（官方）×2；**KEBS DKS1515:2025** 检验标准 PDF + 进口商通知 PDF（官方）。
- **Nigeria Single Window Trade Portal** tip.nsw.gov.ng（官方门户，HS8702-8705）+ Nigeria Customs 禁限清单文本（律所转载，辅）。
CORE_FACTS_VERIFIED:
- Kenya（VERIFIED）：二手乘用车自**首次登记年**起 ≤**8 年**、首登与制造相差 ≤1 年；**RHD-only**（救护/消防/大型工程例外）；Legal Notice 78/2005、KS/DKS1515；2026 年仅首登 2019+ 可进。
- Nigeria（CROSS_CHECKED，CONDITIONAL）：当前官方门户/禁限清单=自**制造年**起 **>15 年**禁（HS8703），另征 NAC levy；须注明以 Nigeria Customs 当期清单为准、装运前复核。
BLOCKED_FACTS: Nigeria “12 年/10 年”确定说法（无一手源，禁用）；仅凭该门户“Right-hand drive only”下舵向结论（该页与 Nigeria LHD 事实冲突，系门户错误）；**埃塞/坦桑/乌干达等其他非洲国家无一手源 → 删除一切硬数字（accuracy>coverage）**；禁止把 Kenya“首登年”基准套用到 Nigeria；未定案税费数字。
RESEARCH_STATUS: **RESEARCH_CONDITIONAL**（Kenya 可定案；Nigeria 受 FACTS_ALLOWED 约束可写；其余国家不写）
WRITING_AI_READY: **TRUE**（带约束：只写 Kenya 完整结论 + Nigeria 条件性结论）

## AB-260903-G10 — Export Sales Contract
PRIMARY_SOURCES_ADDED:
- **最高人民检察院官方《民法典》第三编合同全文**（Art.595/596/597 逐字）https://www.spp.gov.cn/spp/ssmfdyflvdtpgz/202008/t20200831_478413.shtml
- 云南司法厅 / 开封人大政府转载（交叉一致）。
CORE_FACTS_VERIFIED: **Art.596 买卖合同法定内容要素逐字 = VERIFIED**（名称/数量/质量/价款/履行期限地点方式/包装/检验标准方法/结算/合同文字及效力）；595 定义、597 无权处分定位。
BLOCKED_FACTS: FindLaw/华律/法师兄等二手法律网站**不得 VERIFIED**（最高 CROSS/SINGLE，仅辅助）；“法定按日‰违约金”（不存在统一法定比例）；把范本条款当强制；虚构 AutoBridge 一手经办经验。
RESEARCH_STATUS: **RESEARCH_PASS**（法定条款 VERIFIED；实践层 CROSS_CHECKED）
WRITING_AI_READY: **TRUE**

---

## AGGREGATE
- RESEARCH_PASS: G01, G02, G03, G05, G10 (5)
- RESEARCH_CONDITIONAL: G08 (1, WRITING_AI_READY with bounded facts)
- WRITING_AI_READY = TRUE: all 6
- Primary (T1) sources newly added: 20+ across the six packages
- Hard-number country coverage removed for lack of primary source: all G08 African countries except Kenya/Nigeria
- Superseded research files: AB-260903-G05_EV_Shipping_UN3171_IMDG.md, SOURCE_LOG_AB-260903-G05.md (kept, marked superseded for audit)
- NEXT: Writing AI R5 may remediate these six article bodies only within FACTS_ALLOWED_IN_BODY; G05 adopts the new slug; no other 14 articles need research action.
