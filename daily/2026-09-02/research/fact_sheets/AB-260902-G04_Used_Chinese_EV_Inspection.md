# RESEARCH SHEET — AB-260902-G04
- **ARTICLE_ID**: AB-260902-G04
- **CONTENT_TYPE**: PROCUREMENT_GUIDE
- **TOPIC**: 二手中国电动车出口前检测清单（电池 SOH / 事故 / 泡水 / 调表）
- **PRIMARY_KEYWORD**: used Chinese EV inspection checklist battery SOH accident
- **SEARCH_INTENT**: 出口商采购二手中国电动车前的验车与电池健康核验方法
- **TARGET_READER**: 中国二手车出口商、海外二手 EV 买家
- **TARGET_COUNTRY / REGION**: 全球（中国二手 EV 出口）
- **SUGGESTED_URL**: /guides/used-chinese-ev-inspection/
- **FACT_SHEET_VERSION**: FS-v2-20260908-review-repair（2026-09-08 依独立 Review 基线 4b446ab 做 SOURCE_SCOPE/CLAIM_TRACEABILITY 受控补源；不改正文文风、不重新选题）
- **USER PROBLEM**: 二手 EV 与燃油车验车逻辑完全不同，出口前需核验电池健康度（SOH）、事故/泡水/火烧历史、里程真实性（调表）、三电系统状态，避免出口后理赔与认证失败。
- **历史去重（意图边界）**: 历史库 4 篇 new_vs_used_ev 搜索意图为"新车还是二手更划算"的采购决策；本篇为已决定买二手后的出口前技术检测操作清单，属不同搜索意图，不重复。

## VERIFIED FACTS（官方/一手，scope 匹配）
| Fact | Source | URL | Checked | Confidence |
|------|--------|-----|---------|-----------|
| 二手车出口企业须对出口车辆进行检测，凭具备资质的第三方检测机构出具的检测报告等材料办理出口手续；明确二手车出口企业条件与禁止出口情形（达到报废标准等不得出口） | 商务部、公安部、海关总署等《关于二手车出口有关事项的公告》（2024年第6号公告） | https://wms.mofcom.gov.cn/zcfb/wmgl/art/2024/art_52f62edf8132411fa206542d851edfc7.html | 2026-09-08 | VERIFIED |
| 二手车出口前置监管：2019年起开展二手车出口业务即要求第三方检测机构出具检测报告，严禁达到报废标准、在抵押/质押期等车辆出口 | 商务部等《关于支持在条件成熟地区开展二手车出口业务的通知》 | https://www.mofcom.gov.cn/zfxxgk/gkml/art/2021/art_29ef062444784bd5af9400546a1ecb75.html | 2026-09-08 | VERIFIED |
| 进一步加强二手车出口管理：二手车出口企业应履行产品质量与售后责任，注册登记不满一定期限的车辆出口须提交《售后维修服务确认书》等材料（自 2026-01-01 施行，TIME_SENSITIVE，以官方原文为准） | 商务部等四部门《关于进一步加强二手车出口管理工作的通知》 | http://www.mofcom.gov.cn/zcfb/dwmygl/art/2025/art_543d1fcc6a1048d5bf301a8d59ed723e.html | 2026-09-08 | VERIFIED / TIME_SENSITIVE |
| 同上政策中国政府网收录文本（交叉印证发布主体与施行时间） | 中国政府网 | https://www.gov.cn/zhengce/zhengceku/202511/content_7048644.htm | 2026-09-08 | VERIFIED / TIME_SENSITIVE |
| 二手车鉴定评估的国家标准框架为 GB/T 30323-2013《二手车鉴定评估技术规范》；行业技术资料将电池 SOH 定义为当前可用容量/额定容量，并以事故车、泡水车、火烧车判别为评估要点 | 中国汽车流通协会（CADA，行业协会 T2，引 GB/T 30323-2013） | https://www.cada.cn/Content/ueditor/net/upload/file/20180708/6366665897945162707573052.pdf | 2026-09-08 | CROSS_CHECKED（行业标准框架，非出口强制门槛） |

## SUPPORTING FACTS（媒体/行业，方法层；不得表述为法定门槛）
| Fact | Source | URL | Checked | Confidence |
|------|--------|-----|---------|-----------|
| SOH 反映当前容量与新车容量比值，是二手 EV 核心指标；作为经验参考，SOH 明显偏低时更换电池成本高 | 易车 | https://hao.m.yiche.com/wenzhang/107776270/ | 2026-09-02 | SINGLE_SOURCE |
| 检测方法：车机/仪表读取电池健康状态，或第三方检测报告（含 SOH 与电芯最大压差） | 易车 | https://hao.m.yiche.com/wenzhang/107776270/ | 2026-09-02 | SINGLE_SOURCE |
| 现场充电验证：从 20% 充到 80%，对比实际充入度数判断衰减（方法参考） | 懂车帝（视频，T4 方法参考） | https://www.iesdouyin.com/share/video/7618925618490849457 | 2026-09-02 | SINGLE_SOURCE |
| 事故/水泡/火烧专项筛查、查维保与出险记录、检查电池包底部护板拆装痕迹、里程与电池循环次数一致性（方法参考） | 懂车帝（视频，T4 方法参考） | https://www.iesdouyin.com/share/video/7678314679869430004 | 2026-09-02 | SINGLE_SOURCE |
| 磷酸铁锂/三元锂老化加速的经验阈值参考（非法规） | 抖音行业内容（T4） | https://www.iesdouyin.com/share/video/7674527923274474225 | 2026-09-02 | SINGLE_SOURCE |

## FACTS_ALLOWED_IN_BODY（可写成确定事实）
- 中国二手车出口须经第三方检测并取得检测报告、企业资质与禁出情形（VERIFIED，商务部 2019/2024/2025 文件）。
- 注册不满规定期限车辆出口的售后维修服务确认书要求与 2026-01-01 施行节点（TIME_SENSITIVE，须标注以官方原文为准）。
- 二手车鉴定评估国家标准框架 GB/T 30323-2013 与 SOH 的技术定义（CROSS_CHECKED，行业标准框架）。
- SOH/事故/泡水/调表的检测方法论（媒体方法层，表述为"建议/常见做法"，不表述为强制）。

## FACTS_NOT_ALLOWED_IN_BODY / BLOCKED_FACTS（不得写成确定事实）
- **"SOH≥80% 才能通过 EU/东盟等认证"**：仅 Jingsuncar 单一行业站口径，**不存在经核验的通用法定 SOH 门槛**，不得写成法规或认证强制要求；只能写"部分行业经验以 80% 作为采购参考线，具体以目的国认证机构/买家要求为准（confirm before purchase）"。来源：https://www.jingsuncar.com/news/2026-must-see-guide-for-buying-used-new-energy-85493284.html
- 具体目的国对二手 EV 的 SOH/电池强制阈值（须逐国取官方认证法规，本篇不下结论）。
- 各品牌官方电池质保/SOH 判定标准原文（未取得品牌官方条款）。
- 统一的 OBD 诊断接口/第三方检测机构资质与报告格式（未标准化）。

## TIME-SENSITIVE FACTS
- 二手车出口企业资质、车龄/注册期限与售后确认书要求、检测机构要求：以商务部/海关/公安当期公告为准（2026-01-01 节点，2026-09-08 核验）。
- 目的国二手 EV 准入与认证阈值：逐国、逐年变化。

## CONFLICT_LIST
- 无来源间数值冲突；"80%"为行业经验值与"法定门槛"之间的定性冲突，已按 BLOCKED 处理（不赋予法定地位）。

## UNRESOLVED QUESTIONS
- 各目的国二手 EV 准入 SOH/电池法规阈值（需逐国官方源，另立国别指南）。
- 各品牌 SOH 官方判定与质保条款原文。

## SOURCE GATE（发布级）
- SOURCE_URL_COUNT = 11；SOURCE_ORG_COUNT_NORMALIZED = 6（商务部[含wms/www子站,归一]、中国政府网、中国汽车流通协会CADA、易车、懂车帝/抖音[字节系归一]、Jingsuncar）。
- 官方一手（T1）= 商务部×3 + 中国政府网×1；行业协会 T2 = CADA；其余为媒体/视频方法层。
- RESEARCH_STATUS = RESEARCH_PASS（核心搜索意图"出口前要不要检测、检测什么、依据是什么"已由主管部门一手来源 VERIFIED；认证阈值类主张已显式 BLOCKED）。
- WRITING_AI_READY = TRUE。
