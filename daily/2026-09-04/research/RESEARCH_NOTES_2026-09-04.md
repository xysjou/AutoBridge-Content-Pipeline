# RESEARCH NOTES 2026-09-04
## 概况
- 期次：2026-09-04（周五，Asia/Shanghai）。Stage 1 研究，只产出 Fact Sheet / Source Log / QA / Manifest，不写正文、不多语言、不打包。
- 产出：MAIN 车型 10 + MAIN 指南 10 + RESERVE 4 = 24 包；来源 89 条（T1=16 / T2=32 / T3=33 / T4=8）；判定 17 PASS / 7 CONDITIONAL / 0 FAIL；MAIN_READY=20 → RESEARCH_READY.STATUS=READY。
- 门规：按 LESSONS_LEARNED PART 1（commit 33eff0e3）执行，为 09-03 永久升级后首个执行日。

## 采集与来源说明
- 乘用车：懂车帝/汽车之家/搜狐车型库/中关村在线等两个独立结构化库交叉（CROSS_CHECKED 上限），重要参数标注待品牌官网终核；本批未取到品牌英文官网，故车型参数不标 VERIFIED，official_source_available=NO，符合"两个数据库一致≠VERIFIED"。
- 商用车：以卡车之家（360che 体系，部分内容托管于今日头条，已如实标注域名）+ 工信部批次公示/政府源交叉。
- 法规：中国侧优先国务院/海关总署/工信部/海事局/贸促会官方 PDF（T1）；G08 关键标准拿到 msa.gov.cn 官方 IMDG 42-24 文本。

## 关键标准更新（本期落实）
- IMDG Amendment 42-24，决议 MSC.556(108)，2026-01-01 起对中国强制；锂电驱动车辆现行 UN3556（锂金属 UN3557、钠离子 UN3558），新增 P912；旧 UN3171 收窄到湿/钠金属电池车辆设备。散装锂电=UN3480、与设备同装/内含=UN3481，运输前需 UN38.3 摘要。

## 未解决问题（UNRESOLVED，第二阶段不得自行补写）
- G04《海商法》提单条文官方 URL；G06 UNECE R83/R49、EN228/EN590 一手 URL；G08 联合国 UN38.3 手册与 IMO 英文页面 URL；G07 GB16737/WMI 分配查询入口；G09 GB21085 正式发布版与一致性证书国标号；GR1 拉美主管机构 T1；GR2 国务院条例原文 URL。

## NEW_LESSON_CANDIDATE（仅候选，待独立审核，不自行写入 LESSONS）
1. Error Pattern：汽车起重机/专用车上装参数在第三方百科型号高度混淆（QY25E/QY25K5D/QY50K5D）。Suggested Rule：专用车若底盘型号或额定参数在两个来源不一致且无厂商官网，应直接换题而非 CONDITIONAL 保留。Detection：fact 中出现≥2 个不同型号代码即触发。
2. Error Pattern：卡车之家(360che)大量原创内容仅以今日头条镜像可检索。Suggested Rule：Source Name 可写卡车之家但 domain 必须如实填 m.toutiao.com 并降一级权威，不得标注为 360che.com 官方页。

## 推送状态
- 研究文件先生成于本地暂存 repo_stage_0904；生成时 GitHub MCP 连接器未挂载，RESEARCH_READY.pushed_to_github=false。连接器恢复后用 push_files 分批提交，commit message 固定 "Daily research 2026-09-04"，只写 /daily/2026-09-04/research/，提交后回读核验并把 pushed 改为 true、补 commit sha。
