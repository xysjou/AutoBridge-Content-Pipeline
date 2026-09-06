# RESEARCH_NOTES 2026-09-06

## 启动门 (STARTUP_HEAD_SHA_GATE)
- REPO_HEAD_SHA(start)=5d167befa9b037fbd35bf823fecc41b9f09b6b36（origin/main 最新，含Writing AI后续提交）
- LESSONS_LEARNED blob=5a8e7f5f2a255e57b6e63c4d1a3840c549f273a4；READ_AT=2026-09-06 08:05 (Asia/Shanghai)；PRE_RESEARCH_SYNC=PASS
- 历史基线：article_manifest(153篇)/published_urls(80)/vehicle_database(79)/guide_database(53) 已读，五重去重通过。

## 选题与覆盖
- 车型覆盖：Sedan(V01星瑞/V04银河E8/V05风云A8)、SUV(V02博越L)、MPV(V03 iMAX8)、Pickup(V06 T90)、Van(V07 V80)、Light Truck(V08 J6F)、Dump(V09豪沃TX)、Special(V10徐工QY25K5C汽车吊)；动力含ICE/BEV/PHEV/柴油，未连续全选新能源SUV。
- 指南覆盖：中国侧政策性/流程(G01信保/G02 AEO/G03 RCEP/G06木质包装/G08贸易方式/G10人民币)、物流(G04 RoRo订舱)、目的国单国(G05南非/G07肯尼亚/G09尼日利亚)。

## 来源策略与替换
- 中文通用搜索对目的国政府站命中率低（复现既有教训）：改用 web.fetch 直连，ITAC/NRCS/SARS/KEBS/KRA/Nigeria Customs/SON 根站或具体页可达。
- 南非：ITAC import-control 具体页取得强T1（276管制税号、所有二手货需许可、3-5工作日、Act71/91），NRCS LOA、SARS征管到位；具体税率未取SARS当期税则→BLOCKED，判CONDITIONAL。
- 肯尼亚/尼日利亚：机构与制度(KEBS PVOC、SONCAP+单一窗口迁移)官方到位，但'8年车龄'/尼国车龄与各项税率仅有媒体/T4→严格UNVERIFIED+BLOCKED，判CONDITIONAL，绝不给数。
- 墨西哥/哈萨克斯坦：未获SAT/DOF、egov/eec一手→GR1/GR2 判 RESEARCH_FAIL 留RESERVE，禁止写作。
- V10徐工QY25K5C：未取到该型号官方性能样本，仅保留品牌(年报)与'汽车吊不属特种设备目录'(政府事故报告)为VERIFIED，主臂/发动机/性能表全部BLOCKED。

## 状态汇总
- MAIN: PASS=5, CONDITIONAL=15, FAIL=0；WRITING_READY=20；BATCH_STATUS=READY_WITH_CONDITIONS。
- 10个车型均CONDITIONAL（无品牌OEM同trim一手，规格最高CROSS_CHECKED/SINGLE_SOURCE）。
- 指南PASS=5：G02,G03,G06,G08,G10；CONDITIONAL=5：G01,G04,G05,G07,G09；MAIN无FAIL。
- 发布级来源门(≥6 URL/≥4 ORG)通过 0/20；未达者可在事实边界内起草、发布前补源。

## 关键边界（给Writing）
- 禁把中国版写成global；禁任何无来源FOB/CIF/运费/税率/海外售价/销量；国内指导价仅reference且TIME_SENSITIVE。
- 年款/版本差异：V01星瑞175 vs 200kW、V03 iMAX8功率、VR1坦克300——必须分trim，禁止取最大值代表全系。
- G07/G09车龄与税率、G05税率、G04绑扎/SOC等操作值一律'confirm with authority/carrier'。
- GR1/GR2 RESEARCH_FAIL，禁止写作，待对方主管机构官方源后重评。

## NEW_LESSON_CANDIDATE（不自行升级，待独立审核）
1) 中文通用搜索几乎检索不到目的国政府深层子页（KRA/SARS/SON具体税则页），但 web.fetch 直连官方域可行；单国指南SOP应改为'search发现根域→fetch逐层取具体子页'，根站可达≠核心事实已证，税率/车龄仍须具体官方子页，否则CONDITIONAL。
2) 汽车起重机等专用车：上市公司年报/政府事故报告只能证明品牌与监管分类，不能证明具体型号起重性能，专用车上装参数必须取厂商官方载荷表/公告，建议在车型门增加'special-vehicle upfit spec requires OEM load chart'检查。
