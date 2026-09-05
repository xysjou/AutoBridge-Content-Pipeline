# RESEARCH_NOTES 2026-09-05

## 启动门 (STARTUP_HEAD_SHA_GATE)
- REPO_HEAD_SHA(start)=93ff98b2b5e929be5dc0b2dc4f1b27800ef5493f
- LESSONS_LEARNED blob=5a8e7f5f2a255e57b6e63c4d1a3840c549f273a4；READ_AT=2026-09-05 07:49 (Asia/Shanghai)；PRE_RESEARCH_SYNC=PASS
- 历史基线：article_manifest / published_urls(60) / vehicle_database(69) / guide_database(84) 已读，五重去重通过。

## 选题与替换记录
- 车型覆盖：Sedan(V01)、SUV(V02/V05)、MPV(V03)、BEV两厢(V04)、Pickup(V06)、Van(V07)、Light Truck(V08)、Dump(V09)、Tractor(V10)；未连续全选新能源SUV。
- 商用车换题：东风多利卡D6/解放虎VN（仅58二手+头条镜像，年款混杂）→V08骏铃V6；红岩杰狮C6→V09德龙M3000S；徐工QY25K5C（型号混淆）→V10欧曼EST。三者仍无360che canonical/OEM，判CONDITIONAL，关键质量参数BLOCKED。
- 指南替换：原拟 Uzbekistan/Philippines/Peru 单国进口，两轮检索未获对方海关/税务一手源，按 EVIDENCE_CEILING：乌/菲降RESERVE并判RESEARCH_FAIL，Peru本轮不建包；MAIN改用 SAFE外汇收汇(G06)/出口管制筛查(G07)/TIR(G10)，均取得主管机构一手。

## 状态汇总
- MAIN: PASS=9, CONDITIONAL=11, FAIL=0；WRITING_READY=20；BATCH_STATUS=READY_WITH_CONDITIONS。
- 10个车型均CONDITIONAL（无品牌OEM一手，核心尺寸/动力多为CROSS_CHECKED/SINGLE_SOURCE，电池供应商/出口规格等BLOCKED）。
- 指南PASS=9：G01,G02,G03,G04,G06,G07,G08,G09,G10；CONDITIONAL=1：G05(CKD缺WCO/目的国官方)。
- 发布级来源门(≥6 URL/≥4 ORG)通过 0/20；未达者可在事实边界内起草、发布前补源。

## 关键边界（给Writing）
- 禁止把中国版写成global；禁止任何无来源FOB/CIF/运费/税率/海外售价/销量；国内指导价仅reference且TIME_SENSITIVE。
- CONFLICT：V02电池供应商、V06柴油扭矩、V10年款排放、VR1代际尺寸——隔离不得任选。
- GR1/GR2 RESEARCH_FAIL，禁止写作，待 customs.uz / Philippines BOC·LTO·BIR 官方源后重评。

## NEW_LESSON_CANDIDATE（不自行升级，待独立审核）
1) 中文通用搜索引擎对目的国政府站点(customs.uz/BOC/SUNAT)命中率低，单国进口指南应预置英文/当地语言+site:官方域检索与UNECE/WCO数据源，否则默认CONDITIONAL/FAIL。
2) 卡车之家内容大量以 m.toutiao.com 镜像被检索到；Source Log须按真实domain降一级(T3)且不得记为360che canonical，建议后续直接定位360che.com或工信部公告。
