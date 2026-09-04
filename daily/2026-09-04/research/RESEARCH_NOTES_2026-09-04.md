# RESEARCH NOTES — 2026-09-04（独立审核整改 v1.1）

## 0. 启动门 STARTUP_HEAD_SHA_GATE
- REPO_HEAD_SHA@pull = ad84c58400aefc9b12baac1cbae9f5ea2bc2d36a
- LESSONS_LEARNED_SHA = b4c46a7c28ba06227f0f4250bcc951048e701f2f
- LESSONS_READ_AT = 2026-09-04 Asia/Shanghai
- 改前 LOCAL_HEAD=ORIGIN_MAIN；该HEAD仅改LESSONS与09-03,未占用09-04 research,无并发覆盖。

## 1. 本轮范围（只修审核点名项，不重做20篇）
整改包：V04、V07、G01、G02、G04、G05、G06、G07、G08、G09；URL整改覆盖全部24包。未改Writing已动正文，未碰articles/qa/deliveries。

## 2. 判定变化
- G02 PASS→CONDITIONAL：法律框架只回答“目录内必检”，未取得现行《必须实施检验目录》整车逐10位税号清单前，不对具体车型断言必检/免检。
- G04 CONDITIONAL→PASS：补全国人大《海商法》2025修订（主席令58号，2026-05-01施行）第80/81/87条一手骨架。
- V04 维持CONDITIONAL：市场误标已纠、GWM官网证明“初恋海外版=JOLION”（基础车名SAME_MODEL），但中国版扭矩/变速箱仅澳版来源，入BLOCKED待二源。
- 其余：V07消矛盾定SAME_MODEL；G01换2026税则；G05换承运人官方；G06换现行标准；G07换标准正文；G08补UN一手；G09拆分现行/草案，均PASS。

## 3. 汇总
- MAIN：PASS 15 / CONDITIONAL 5 / FAIL 0；WRITING_READY 20/20。
- 全24包：PASS 17 / CONDITIONAL 7 / FAIL 0。
- 批次状态：READY_WITH_CONDITIONS（存在MAIN CONDITIONAL且无FAIL）。来源合计 120 条（T1占比显著提升，法规/标准类全部具备官方一手）。

## 4. 新增永久规则（已按独立审核要求写入 LESSONS_LEARNED.md PART 4）
STARTUP_HEAD_SHA_GATE / DRAFT_STANDARD_IS_NOT_CURRENT_STANDARD / PLACEHOLDER_URL_BLOCK / BATCH_STATUS_TAXONOMY。

## 5. 版本与交接
FACT_SHEET_VERSION=v1.1-2026-09-04（替代v1.0）；RESEARCH_LOCK=false；MAIN WRITING_AI_READY=true、RESERVE=false；Writing如已读v1.0必须重读v1.1。
