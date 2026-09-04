# AutoBridge Daily Research QA — 2026-09-04（v1.2：独立审核整改 + Final Cleanup + 发布级Source Gate）
> 本文件为第一阶段 Research 自检，不代表文章已写完/可上线/Codex 已审。
> 启动门：REPO_HEAD_SHA@pull=`ad84c58400aefc9b12baac1cbae9f5ea2bc2d36a`；LESSONS_LEARNED_SHA=`b4c46a7c28ba06227f0f4250bcc951048e701f2f`；PRE-RESEARCH-SYNC=PASS。
> 事实层（Final Cleanup 后）：MAIN PASS/COND/FAIL=15/5/0；**发布级标准套用后（最终口径）：MAIN 4/16/0，全包24=4/20/0，SOURCE_GATE_PASS=6/24，WRITING_READY=20，BATCH_STATUS=READY_WITH_CONDITIONS**。

## 一、规则十九条逐项自检
1. 重复车型：无。24包与/state车型库及09-02/09-03历史五重去重(车型/关键词/意图/URL/主题)无碰撞;V04 Jolion中外拆分、V07 T9/悍途身份澄清均非重复建页。
2. 重复搜索意图：无。G01归类/G02商检/G04提单/G08危规等互不重叠,与历史指南无cannibalization。
3. 重复URL：无。全部相对常绿路径且唯一;.example/localhost/test/staging/dummy扫描=0;车型Hub无年款/-specs后缀(EVERGREEN_MODEL_URL_BY_DEFAULT)。
4. 中国版当全球版：否。车型REFERENCE_MARKET一律CHINA;V04海外HEV/澳版market逐Fact改OVERSEAS(具体国);V06 PHEV与荣耀HEV分线;V07出口OEM标EXPORT不升CHINA VERIFIED。
5. 无来源关键参数：否(即不存在)。每条重要Fact带source/url/market/trim/checked/confidence;V04中国版扭矩/变速箱仅澳版来源已撤出确定事实入BLOCKED。
6. 参数冲突：无未处理CONFLICT。V07身份内部矛盾已消除,唯一判定SAME_MODEL(双侧JAC OEM),配置市场分离。
7. 采购法规权威源：是。法规/标准T1官方源数量 G01=4/G02=5/G03=3/G04=1(NPC海商法)/G06=8/G07=4/G08=4(UNECE+MSA+49CFR)/G09=7;G02未取得现行法检目录整车逐10位税号清单故CONDITIONAL。
8. AI推测数据：无。无FOB/CIF/运费/利润率/海外售价/关税VAT/销量/市占率/最畅销;中国指导价仅chinese_domestic_msrp+TIME_SENSITIVE不换算出口报价;G10只讲费用项目不给金额。
9. 每篇Source URL：是。24份Source Log共120条,逐条真实URL+Organization+Domain+Tier+Market+Scope+Checked+Official,无'品牌名无URL'。
10. 时效数据带日期：是。价格/在售/法规/税率/费率/标准版本/出口许可均TIME_SENSITIVE并注公告号/施行日/核对日(G01税则2026、G04海商法2026-05-01、G06修改单2026-05-01、G08 IMDG42-24强制2026-01-01)。
11. T4当关键事实唯一依据：否。G05原T4阈值撤出,改WW/Höegh承运人官方并标CARRIER_SPECIFIC;11467清单改EDITORIAL_RECOMMENDATION;未取到的绑扎/朝向/胎压items to confirm入BLOCKED。
12. 现行版本门(CURRENT_STANDARD_VERSION_GATE)：是。G06=GB18352.6-2016+XG1-2026(2026-05-01)与GB17691-2018分列、GB19147-2016;G07=GB16735-2019标准正文;G08=IMDG42-24+UN手册Rev.8/Amend1(UN3556-3558,散电池UN3480/3481,不回退UN3171);G01=税则2026;均带版本/修订/生效日/一手URL。
13. 草案当现行(DRAFT_STANDARD_IS_NOT_CURRENT_STANDARD)：否。G09 CURRENT=GB/T21085-2020;20260041-Q-339/GB21085—XXXX单列DRAFT/FUTURE(current_requirement=false);multistage唯一草案依据已降UNVERIFIED移出正文。
14. 车型别名OEM证明(MODEL_ALIAS_REQUIRES_OEM_PROOF)：是。V04补GWM官网'初恋海外版JOLION'(CHINA OEM Primary)→车名SAME_MODEL,HEV动力仍分列;V07双侧JAC官方站→SAME_MODEL;无OEM证明只标RELATED。
15. 来源市场路径(SOURCE_MARKET_PATH_CHECK)：是。逐条核对URL国家/主体/标题;V04澳/泰/越不标CHINA;UNECE/IMDG标INTERNATIONAL;RoRo承运人标具名CARRIER_SPECIFIC。
16. 官方源范围匹配(PRIMARY_SOURCE_SCOPE_MUST_MATCH)：是。轻型不套重型(G06分列);MIIT准入引用不替代标准正文(G07);具名承运人指南只适用该承运人(G05);法律框架不替代逐HS目录判定(G02)。
17. 事实级置信(CONFIDENCE_IS_FACT_LEVEL)：是。跨市场/年款/动力不构成CROSS_CHECK;同一事实两独立可靠来源一致才CROSS_CHECK;一手且scope匹配才VERIFIED;二级门户/媒体不升VERIFIED。
18. 占位URL(PLACEHOLDER_URL_BLOCK)：否(即不存在)。生产JSON扫描.example/localhost/test/staging/dummy=0;suggested_url为相对生产常绿路径。
19. 共享文件与边界：整改只写daily/2026-09-04/research/与根LESSONS_LEARNED.md(PART1-5);未改articles/qa/deliveries;改前等效pull,禁force push;误建临时文件x已删除。

## 二、三台机器QA门（Final Cleanup，扫24包）
- MARKET_CONFIDENCE_GATE：CHINA Fact为VERIFIED须有CHINA Primary,否则FAIL。
- DRAFT_SOURCE_GATE：来源含draft/征求意见/计划且VERIFIED+current_requirement=TRUE =>FAIL(只扫来源)。
- T4_BODY_GATE：T4-only Fact进确定性正文且无EDITORIAL_RECOMMENDATION也未进BLOCKED=>FAIL。
- 首扫命中6处标签层问题(G08国际规则market/UN一手源、V04别名主体、G10舱单费EDITORIAL),按只改标注不新研究处置;**复扫scanned=24 fail_count=0 result=PASS**。

## 三、REPEATED_ERROR复核
- V04 SOURCE_MARKET_PATH_CHECK：整改前REPEATED_ERROR=TRUE/HIGH,整改后海外market归位+补GWM OEM,RESOLVED=TRUE。
- G06 CURRENT_STANDARD_VERSION_GATE：整改前TRUE/HIGH,整改后现行版本+修改单+生效日+一手URL齐备且轻重分列,RESOLVED=TRUE。
- 除两项闭环外未发现LESSONS已禁错误再现。

## 四、发布级 Source Gate（最终口径，PART 5）
- 门槛：MAIN原则上SOURCE_URL_COUNT>=6且SOURCE_ORG_COUNT>=4,scope匹配,关键URL当天重开核验;只统计既有真实来源,不补造不凑数。
- SOURCE_GATE_PASS=6/24：G01 6/6、G02 7/5、G06 10/7、G07 6/6、G08 8/8、G09 9/8。
- 与事实verdict取交集后 **MAIN发布级RESEARCH_PASS=4=G01/G07/G08/G09**;RESEARCH_CONDITIONAL=16;RESEARCH_FAIL=0。G02/G06数量门PASS但事实层CONDITIONAL(法检逐税号清单/海外排放限值),仍为CONDITIONAL。
- MAIN_GATE_FAIL(14个,数量不足)：G03 3/3、G04 5/5、G05 7/3、G10 4/4;V01 3/3、V02 4/3、V03 5/5、V04 5/5、V05 5/5、V06 5/5、V07 5/5、V08 4/2、V09 4/4、V10 4/2。RESERVE：VR1 3/3、VR2 3/2、GR1 2/2、GR2 3/3。
- 处置：事实达标仅来源深度不足者降CONDITIONAL并加[PUBLISH_GATE]BLOCKED;CONDITIONAL+READY=TRUE可起草,发布/Codex Review前必须补足;V08/V10机构数仅2缺口最大,G05机构数3需补不同主体carrier/OEM/terminal。
- 车型身份八件套逐包入交接;未单独锁定GENERATION/PRODUCTION_BOUNDARY/DRIVETRAIN者标NOT_LOCKED_IN_FACT_SHEET待补,不臆造。GR1拉美=Brazil/Mexico两国T1未齐COUNTRY_EVIDENCE_INCOMPLETE,COUNTRY_SPECIFIC_ONLY=true,保持RESERVE。

## 五、CONDITIONAL包BLOCKED边界（Writing必须遵守）
- V04：中国版扭矩/变速箱具体值(仅澳版市场不匹配)、海外HEV与中国1.5T的1:1等同、任何出口价格。
- G02：任一具体车型/10位税号当前是否落法检目录(未取现行目录整车逐税号清单,TIME_SENSITIVE,申报时以海关现行目录+监管条件核验)。
- G05：绑扎/破断/车头朝向/胎压具体值(items to confirm with carrier/OEM)、统一SOC百分比(仅Höegh一家不得泛化)、T4固定数值。
- G06：海外Euro/EPA限值与EN燃油规格精确数值、国六与海外标准等效性结论。
- G10：任何具体金额(T4旧值/波动值不得写成当前确定收费)、据此估算到岸成本/利润(禁算)。
- 14个数量不足MAIN：[PUBLISH_GATE]Review前补足>=6URL/>=4机构,补源scope匹配当天重开,禁凑无关来源。

## 六、NEW_LESSON_CANDIDATE（仅候选,待独立审核,不自行写入永久规则）
- 专用车上装第三方型号高度混淆且无官网时直接换题而非CONDITIONAL(fact出现≥2个不同型号代码即触发)。
- 卡车之家原创仅以今日头条镜像可检索时,Source Name写卡车之家但domain如实填m.toutiao.com并降一级。
- (注:发布级Source Minimum/身份锁/地区代表国/物流具体性/交接字段/baseline与完成块六条已由项目主直接确认为永久规则,写入LESSONS PART5,非候选。)

## 七、QA结论
- 20个MAIN无FAIL、无未处理冲突、无占位URL、关键法规均有T1;发布级标准下4个MAIN达发布级PASS、16个CONDITIONAL(14个卡来源数量+G02/G06事实层),均带明确BLOCKED且WRITING_AI_READY=TRUE可起草;0 FAIL。
- RESEARCH_QA=PASS(附CONDITIONAL边界);RESEARCH_BASELINE_CHANGED=TRUE(发布级轮在Writing开工后更新verdict/来源门),Writing须以RESEARCH_COMPLETE_COMMIT_SHA为baseline重读Fact Sheet/Handoff,CONDITIONAL不得把BLOCKED写成确定事实。
