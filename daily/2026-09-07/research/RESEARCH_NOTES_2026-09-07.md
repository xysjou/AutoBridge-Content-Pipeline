# RESEARCH_NOTES 2026-09-07

## 启动门 (STARTUP_HEAD_SHA_GATE)
- REPO_HEAD_SHA(start)=7c0e5b7e59cb0a2edd4bfe240c5b9642833f1c53（origin/main 最新）
- LESSONS_LEARNED blob=8890f8366e4f28156d6eb3f4027b2b496f507d18（PART0-6）；READ_AT=2026-09-07 startup (Asia/Shanghai)；PRE_RESEARCH_SYNC=PASS
- 历史基线：article_manifest(153篇)/published_urls(80)/vehicle_database(79)/guide_database(53) + 09-06 daily_manifest 已读，五重去重通过，24包全部NEW_PAGE。

## 选题与覆盖
- 车型覆盖：SUV(V01捷途大圣)、Sedan(V02奕炫/V04 MONA M03)、MPV(V03 G90)、SUV-新能源(V05深蓝S05增程+纯电)、Pickup(V06凯程F70)、Van(V07全顺T8)、Light Truck(V08庆铃KV100)、Heavy Tractor(V09解放J7)、Special(V10中联ZTC250H汽车吊)；动力含ICE/BEV/EREV/柴油，未连续全选新能源SUV。
- 指南覆盖：中国侧制度/流程(G01知产备案/G02许可证与两用物项目录/G03 9710-9810/G04主动披露/G05铁路快通/G06退运/G07综保区/G09不可抗力与仲裁/G10电子口岸)、目的国单国(G08坦桑)。

## 来源策略与替换
- 中文通用搜索对目的国政府深层子页命中率低（连续三批复现）：坦桑用英文 site:tra.go.tz / tbs.go.tz 仍empty，仅货代11467(T4)与过期媒体→G08判CONDITIONAL且FACTS_ALLOWED为空，税率/车龄/PVoC生效日全BLOCKED。
- 加纳(site:gra.gov.gh empty)、越南(仅11467+2015/2019旧镜像)未获对方政府一手→GR1/GR2判RESEARCH_FAIL留RESERVE、sources为空、禁止写作。
- G09补到全国贸促会总会ccpit.org页面（不可抗力证明办理平台rzccpit），与省级贸促会同母机构归一为CCPIT，核心意图PASS；CIETAC仲裁规则细节缺官网一手，BLOCKED。
- V10中联ZTC250H：未取到该型号官方载荷表，百科QY25H431为不同型号禁止套用，仅保留ZTC产品线身份(SINGLE)，主臂/性能表全BLOCKED。
- V09解放J7：国五CA6DM3(550Ps/2300N·m，2018上市来源)明确标历史款，国六CA6SX1(至600Ps)为现售线但仅SINGLE，分排放代际禁止混。

## 状态汇总
- MAIN: PASS=9, CONDITIONAL=11, FAIL=0；WRITING_READY=20；BATCH_STATUS=READY_WITH_CONDITIONS。
- 10个车型均CONDITIONAL（无品牌OEM同trim一手，规格最高CROSS_CHECKED/SINGLE_SOURCE）。
- 指南PASS=9：G01,G02,G03,G04,G05,G06,G07,G09,G10；CONDITIONAL=1：G08坦桑；MAIN无FAIL。
- 发布级来源门(≥6 URL/≥4 ORG)通过 0/20；未达者可在事实边界内起草、发布前补源。

## 关键边界（给Writing）
- 禁把中国版写成global；全顺T8≠福特全球Transit、KV100≠ISUZU全球ELF；禁任何无来源FOB/CIF/运费/税率/海外售价/销量；国内指导价仅reference且TIME_SENSITIVE。
- 年款/动力/排放差异：V01大圣115/135kW、V02奕炫1.5L/马赫1.5T、V07全顺2.0T/2.3T、V09 J7国五/国六——必须分trim/代际，禁止取最大值代表全系。
- G08坦桑、GR1/GR2：税率/车龄/PVoC一律'confirm with TRA/TBS/GRA/GSA/越南海关'，FAIL包禁止写作。

## NEW_LESSON_CANDIDATE（不自行升级，待独立审核）
1) 英文 site:官方域 对非洲目的国(TRA/GRA)深层税则页仍可能empty，单国指南SOP需search发现根域后用web.fetch逐层取子页；根站/检索为空都不能用货代T4补位，宁可CONDITIONAL/FAIL。
2) 同一名义吨位的专用车（如中联QY25H与ZTC250、徐工QY25K）参数严禁跨型号套用；专用车上装参数必须型号一致的OEM载荷表/公告，百科相邻型号只能证明产品线存在。
