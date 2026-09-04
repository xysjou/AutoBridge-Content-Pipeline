# RESEARCH QA — AutoBridge Daily Research 2026-09-04

> Stage 1 自检报告（只研究，不写正文）。门规版本：LESSONS_LEARNED.md PART 0 + PART 1（commit 33eff0e3，含 2026-09-03 Permanent Upgrade）。
> 总包数 24（MAIN 20 / RESERVE 4）；来源记录合计 89 条（T1=16 / T2=32 / T3=33 / T4=8）；判定 {'RESEARCH_PASS': 17, 'RESEARCH_CONDITIONAL': 7, 'RESEARCH_FAIL': 0}。

## 0. 选题清单与三级判定
### 0.1 MAIN 车型（10）
| Article ID | 类型 | 优先级 | 车型 | Verdict | 来源数 | 含T1官方 |
|---|---|---|---|---|---|---|
| AB-260904-V01 | VEHICLE_P | MAIN | Chery 奇瑞 Arrizo 8 艾瑞泽8 | RESEARCH_PASS | 3 | NO |
| AB-260904-V02 | VEHICLE_P | MAIN | BYD 比亚迪 Qin L DM-i 秦L DM-i | RESEARCH_PASS | 4 | NO |
| AB-260904-V03 | VEHICLE_P | MAIN | Wuling 上汽通用五菱 Bingo 缤果 | RESEARCH_PASS | 5 | NO |
| AB-260904-V04 | VEHICLE_P | MAIN | GWM Haval 长城哈弗 Jolion(中国市场名:哈弗初恋) | RESEARCH_CONDITIONAL | 4 | NO |
| AB-260904-V05 | VEHICLE_P | MAIN | Chery 奇瑞(风云/Fulwin) Fulwin T9 风云T9 | RESEARCH_PASS | 5 | YES |
| AB-260904-V06 | VEHICLE_P | MAIN | GAC Trumpchi 广汽传祺 Trumpchi E8 PHEV 传祺E8(新能源) | RESEARCH_PASS | 5 | YES |
| AB-260904-V07 | VEHICLE_P | MAIN | JAC 江淮 T9 Hunter(中国市场名:悍途) | RESEARCH_PASS | 5 | YES |
| AB-260904-V08 | VEHICLE_P | MAIN | JMC 江铃 Shunda 顺达 轻卡(载货车) | RESEARCH_PASS | 4 | NO |
| AB-260904-V09 | VEHICLE_P | MAIN | Dongfeng 东风商用车 Tianlong KL 天龙KL 牵引车 | RESEARCH_PASS | 4 | NO |
| AB-260904-V10 | VEHICLE_P | MAIN | Dongfeng 东风商用车 Tianjin KR 天锦KR 冷藏车 | RESEARCH_PASS | 4 | NO |
### 0.2 MAIN 采购指南（10）
| Article ID | 类型 | 优先级 | 主题 | Verdict | 来源数 | 含T1官方 |
|---|---|---|---|---|---|---|
| AB-260904-G01 | PROCUREME | MAIN |  出口车辆HS编码归类:87.02/87.03/87.04/87.05与挂车8716怎么分 | RESEARCH_PASS | 3 | YES |
| AB-260904-G02 | PROCUREME | MAIN |  中国侧出口商品检验与申报:车辆出口要不要商检、怎么办 | RESEARCH_PASS | 3 | YES |
| AB-260904-G03 | PROCUREME | MAIN |  出口车辆原产地证书:CO/普惠制/自贸协定优惠产地证怎么办 | RESEARCH_PASS | 3 | YES |
| AB-260904-G04 | PROCUREME | MAIN |  车辆海运提单怎么选:船东单MBL/货代单HBL/电放/海运单SWB | RESEARCH_CONDITIONAL | 4 | NO |
| AB-260904-G05 | PROCUREME | MAIN |  车辆出口装运前整备PDI与防护:断电/油量/胎压/车身防护怎么做 | RESEARCH_CONDITIONAL | 3 | NO |
| AB-260904-G06 | PROCUREME | MAIN |  中国车出海的排放与燃油适配:国六标准、汽柴油含硫与海外燃油匹配 | RESEARCH_CONDITIONAL | 3 | NO |
| AB-260904-G07 | PROCUREME | MAIN |  车辆识别代号VIN与铭牌合规:17位结构/WMI/出口车铭牌要核对什么 | RESEARCH_PASS | 3 | YES |
| AB-260904-G08 | PROCUREME | MAIN |  动力电池与备件海运合规:UN3480/3481、UN38.3与IMDG 42-24现行分类 | RESEARCH_PASS | 5 | YES |
| AB-260904-G09 | PROCUREME | MAIN |  出口车辆随车文件包:合格证/一致性证书/技术参数表/底盘证怎么备 | RESEARCH_PASS | 4 | YES |
| AB-260904-G10 | PROCUREME | MAIN |  车辆出口国际物流费用构成:O/F、THC、DOC、BAF等项目怎么核对 | RESEARCH_CONDITIONAL | 4 | NO |
### 0.3 RESERVE（4）
| Article ID | 类型 | 优先级 | 题目 | Verdict | 来源数 | 含T1官方 |
|---|---|---|---|---|---|---|
| AB-260904-VR1 | VEHICLE_P | RESERVE | Changan Nevo 长安启源 Qiyuan A07 启源A07 | RESEARCH_PASS | 3 | NO |
| AB-260904-VR2 | VEHICLE_P | RESERVE | SAIC Maxus 上汽大通 Xintu V80 新途V80 厢式轻客 | RESEARCH_PASS | 3 | NO |
| AB-260904-GR1 | PROCUREME | RESERVE |  拉美车辆准入认证:巴西(L-CVM/INMETRO/IBAMA)与墨西哥(NOM)分国框架 | RESEARCH_CONDITIONAL | 2 | NO |
| AB-260904-GR2 | PROCUREME | RESERVE |  车辆出口知识产权:商标海关备案、OEM授权与平行出口侵权边界 | RESEARCH_CONDITIONAL | 3 | NO |

判定口径：RESEARCH_PASS / RESEARCH_CONDITIONAL 均可作为 READY 交第二阶段，但 CONDITIONAL 必须在 Fact Sheet 内列出 BLOCKED_FACTS、FACTS_ALLOWED_IN_BODY、FACTS_NOT_ALLOWED_IN_BODY；RESEARCH_FAIL 不得交接。本批 FAIL=0。

## 1. 规则十九条逐项核对（原 Daily Pipeline 规则十九）
1. **是否存在重复车型？** 否。已对照 /state/vehicle_database.json（39 历史车型）、09-02（12）、09-03（12）五重去重；本批 12 个车型（含备用）均未在历史出现同车型主页。
2. **是否存在重复搜索意图？** 否。逐题比对 13 个历史指南簇与 09-02/09-03 指南，本批 12 个指南意图均为新增（见 §3 去重对照）。
3. **是否存在重复 URL（slug）？** 否。机器校验 24 个 suggested_url 全部唯一。
4. **是否把中国版当成全球版？** 否。所有车型 fact.market=CHINA；V04 Jolion 明确拆分"中国版=哈弗初恋 1.5T"与"海外 HEV（澳/越）"，海外参数单列且不并入；V07 T9 海外牵引/货载值标注为海外厂方数据；未把任何中国配置写成 global spec。
5. **是否存在无来源关键参数？** 否（机器扫描）。除显式标 UNVERIFIED 的字段外，每条 fact 均带 source 名与真实 URL；G10"不给金额"为方法性事实，已挂 4 个费用结构来源。
6. **是否存在参数冲突？** 无未解决 CONFLICT。V09 天龙 KL 功率存在 343kW（总功率）/337kW（净功率）两种口径，已在同一 fact 内注明为口径差异而非冲突；V04/V06 的不同动力版本（HEV vs PHEV、长短轴）按 trim 分列，不做平均、不任选。
7. **采购法规是否来自权威来源？** 中国侧法规类（G01/G02/G03/G07/G09）均取得 T1：国务院/海关总署令 270 号与 277 号官方 PDF、工信部 GB 标准官方 PDF、地方政府/公安部规范转载；G08 危险品运输取得**中国海事局 msa.gov.cn 官方 IMDG 42-24 中文文本 PDF**。G04/G05/G10 为操作/行业实践类（非法定事项），以 T2/T3 支撑定义，凡 T4 数值一律列入 BLOCKED。G06 涉海外排放限值未取到 UNECE 一手源，相关精确限值列入 BLOCKED，判 CONDITIONAL。
8. **是否存在 AI 推测数据？** 否。未生成任何 FOB/CIF、海运费、利润率、海外售价、关税/VAT、销量/市占率、"最畅销"类数据；中国指导价一律标 chinese_domestic_msrp 且 TIME_SENSITIVE、注明"禁换算出口报价"。
9. **是否每篇都有 Source URL？** 是。89 条来源全部含 http(s) 真实 URL、Organization、Domain、Source Type/Tier、Market、Scope、Checked Date、Authority Level、Official YES/NO；无"BYD official"式无 URL 条目。
10. **是否所有时效性数据带日期？** 是。价格、在售、法规版本、费率类均标 TIME_SENSITIVE 并在 fact/sheet 内注明以现行官方为准、Checked=2026-09-04。
11–19（补充一致性）：目录结构 fact_sheets/source_logs/reserves/research_qa 齐全；manifest 字段齐全且 research_status 仅用 READY/RESERVE/REJECTED；CONFLICT/UNVERIFIED 未进入确定性事实库；REFERENCE_MARKET 车型=CHINA；三个汽车网站仅用于参数提取与交叉验证，未复制测评/评论/文章结构；无登录/验证码绕过（受限即换源）。

## 2. LESSONS_LEARNED PART 1 新门规逐条核对
- **PRE-RESEARCH ERROR CHECK**：开工前读取 /state 四库本地快照（09-02 拉取）+ 09-02/09-03 manifest + 最新 LESSONS（33eff0e3）。结论 REPEATED_ERROR = **FALSE**。
- **T1–T4 来源分级**：本批 T1=16 / T2=32 / T3=33 / T4=8；T4（顺企网 SEO/抖音百科等）仅作搜索线索，其具体数值全部进 BLOCKED_FACTS，未作为关键事实唯一依据。
- **三级判定（PASS/CONDITIONAL/FAIL）**：17 PASS / 7 CONDITIONAL / 0 FAIL；每个 CONDITIONAL 包均列出 BLOCKED_FACTS 与 allowed/not-allowed 清单。
- **车型身份先确认（BRAND/MODEL/YEAR/TRIM/MARKET/BODY/ENERGY）**：12 车型全部先定身份再采参；不同 trim/动力/轴长分列。
- **MODEL_ALIAS_REQUIRES_OEM_PROOF**：V04 Jolion=初恋、V07 T9=悍途 的中外名称对应**未取得 OEM 官方证明**，一律标 RELATED_MODEL（注明需 OEM 终核），未断言 SAME_MODEL。
- **SOURCE_MARKET_PATH_CHECK**：逐条核对 URL 国家代码/语言/主体；澳版(au)、越版、南非来源均如实标 AUSTRALIA/VIETNAM/EXPORT，未因目标市场而错标（无 Bahrain→UAE 类错误）。
- **PRIMARY_SOURCE_SCOPE_MUST_MATCH**：G01 官方税率表为中国进口侧，仅用于品目条文，不用于出口税率；G06 中国 GB 标准不外推为 Euro 限值；官方但范围不匹配者不升 VERIFIED。
- **商用车 HS-FIRST**：G01 先定 87.01/87.02/87.03/87.04/87.05/8716 再谈流程；V08/V09/V10 分别落在 8704/8701/8704（冷藏），未用一套卡车流程套全部。
- **CURRENT_STANDARD_VERSION_GATE**：G08 已确认现行版本 IMDG **Amendment 42-24 / 决议 MSC.556(108) / 对中国强制 2026-01-01 / 官方 URL=msa.gov.cn PDF**；锂电车辆现行 UN3556（锂金属 UN3557、钠离子 UN3558），**旧 UN3171 仅用于湿/钠金属电池车辆，未作为锂电车辆当前分类**（更正 09-03 G05 旧口径）。
- **EVIDENCE_CEILING_IS_NOT_RESEARCH_PASS**：未用"verify officially/evidence ceiling"代替取证；G06 海外限值、GR1 拉美认证因缺主管机构一手源，分别降为 CONDITIONAL（备用 GR1 明确转正式前补 T1，否则 FAIL 替换）。
- **CONFIDENCE_IS_FACT_LEVEL**：置信度挂在每条 fact；不同来源支撑不同事实时不互凑 CROSS_CHECKED（如两库分别支撑不同字段则各自 SINGLE_SOURCE）。
- **REUSE_STRONGEST_VERIFIED_SOURCE**：中国出口许可/资质类复用历史已确认的官方口径方向；G09 新车出口登记直接采用地方政府转载的公安部规范 + 工信部合格证标准。
- **DEPENDENCY_UPDATE_PROPAGATION**：UN3171→UN3556 的更正已在本批 G08、G05（新能源 SOC 与 G08 联动）、G09（新能源附加文件与 G08 联动）三处一致引用，无残留旧分类。
- **SOURCE_INTEGRITY（名称=URL 主体）**：卡车之家内容经今日头条托管的，Source Name 写"卡车之家（官方号，今日头条）"并如实给 toutiao 域名，未伪装成 360che 官网；政府转载标注"转载，建议回查原文"。机器校验无 SOURCE_INTEGRITY_FAIL。
- **NEW_LESSON_CANDIDATE**：见 RESEARCH_NOTES（仅提候选，不自行写入 LESSONS）。

## 3. 历史去重与替换记录
- **车型去重**：避开历史 39 + 09-02 12 + 09-03 12。品类覆盖：Sedan(V01/V02)、Small BEV(V03)、SUV(V04/V05)、MPV(V06)、Pickup(V07)、Light Truck(V08)、Tractor(V09)、Refrigerated(V10)；备用 Sedan EREV/BEV(VR1)、Van(VR2)。本批未出现"连续全选新能源 SUV"，ICE/柴油商用车占比过半。
- **选题替换（来源质量不达标即换，不硬凑）**：
  - 原拟 V10 徐工 QY25K5 汽车起重机 → 官方规格页未取到、第三方型号(QY25E/QY25K5D/QY50K5D)互相冲突，**替换为东风天锦 KR 冷藏车 DFH5180XLC**（卡车之家双源 + 工信部 410 批公示交叉）。
  - 原拟 VR2 江铃特顺 → 多为国五旧款且与福特全顺资料混杂，**替换为上汽大通新途 V80**（搜狐/太平洋双源，分功率/轴长）。
- **指南去重**：本批 G01–G10、GR1/GR2 与历史 13 簇及两期指南意图均不重叠；G02（中国法定检验）刻意区别于 09-03 G06（第三方 PSI），G08（散装电池 UN3480/3481 + 整车 UN3556 现行版）区别于 09-03 G05（旧 UN3171 整车），G07（VIN 结构/铭牌合规）区别于历史 photo_vin_review（二手车验车）。
- **UPDATE_EXISTING 判定**：本批无"仅加年份重复建页"；未发现需要 UPDATE_EXISTING 的历史同车型（09-03 文章由另一 AI 在写，按用户要求本批不回改历史文件）。

## 4. BLOCKED / NOT-ALLOWED 汇总（交第二阶段重点）
- 全部 20 个 MAIN：禁止出现出口报价/到岸价/利润/海运费率/海外售价/关税 VAT 具体数字/销量市占率。
- CONDITIONAL 包的禁用字段：V04（中外版本混写、same model 断言）、V06（HEV/PHEV 混写）、V07（海外牵引货载当中国公告值、same model）、G04（提单法条原文需补《海商法》T1）、G05（留油%/绑扎破断吨数/胎压+10%/SOC 等 T4 数值不得写成标准）、G06（UNECE/Euro/EN 具体限值在补一手源前不得写死）、G10（任何金额不得写成当前收费）。
- 备用 GR1（拉美认证）在补 INMETRO/IBAMA/墨西哥经济部 T1 前不得升 MAIN；GR2 补国务院《知识产权海关保护条例》官方原文后可升。

## 5. 机器校验结果
- 51 个 JSON 全部合法；24 article_id 唯一；24 suggested_url 唯一；置信度枚举合法；除显式 UNVERIFIED 外 fact 均带 URL；source log 全部含真实 URL 与 domain；REFERENCE_MARKET 车型=CHINA。
- 结论：**QA PASS，REPEATED_ERROR=FALSE，可交第二阶段（CONDITIONAL 包按 BLOCKED 清单写作）。**
