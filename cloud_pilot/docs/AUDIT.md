# 只读审计 — 2026-11-02（Work Cloud）

基线 main：`92e97312f1f225023bd663ada41dfadfc9bfd848`，通过 GitHub ref GET 与云端 clone 复核；桌面数据仅作对照。没有访问 Mac、代理或 VPN。

|目录|基线文件数|
|---|---:|
|batches|270|
|daily|2100|
|incoming|61|
|pipeline|8|
|reports|249|
|reviews|36|
|state|4|
|deliveries|2127|
|skills|4|
|.github|3|
|.migration|8|
|根目录其他文件|4|
|合计|4874|

精确路径、Git blob SHA、字节数、模式见 `evidence/baseline-inventory.json`，不是只给抽样数量。递归 Git tree 未截断。93 个 CURRENT：v1=43、v2=39、v3=1、v4=10；版本目录内文件174个。每个 CURRENT 的解析目标和存在性均记录在清单。

已完整读取 README、VERSIONING、LESSONS_LEARNED、skills/README、Research v1.1、Writing v1.3 与 registry。未发现 AGENTS.md 或额外 skills references 文件。两份 Skill 指向的动态规则/状态另行读取，记录 SHA-256；Skill 原件不改。

审计代表样本：

- `batches/index.json`、两个 batch manifests；AB50_024 的 CURRENT=v4 与真实 v4 正文，未把 README 中旧 v2 示例当作现行版本。
- `daily/2026-09-07/research/RESEARCH_HANDOFF_2026-09-07.json`、G01 fact sheet/source log、daily manifest。
- `daily/2026-09-10/qa/FINAL_MANIFEST_2026-09-10.json`：WAITING_FOR_RESEARCH；0篇，不可自行填补。
- `incoming/2026-09-04/AutoBridge_25_v3_Content_Repair_20260904/README.md`：候选，不是上线许可。
- `reviews/2026-09-06/review_handoff_20260902_20260905_5d167bef_GATE.json`：80篇旧基线，无 REVIEW_PASS；不能套给当前 main。
- `reviews/site-pilot-11-20260909/research-return-repair-20260909.json` 与更新的 `WRITING_V4_HANDOFF_20260912.json/.md`：11篇专项，仍有研究/图片/审核阻塞；后者是 Writing handoff，不是假称独立审查通过。
- 全部 `pipeline/*.py`：旧 SQLite/manifest QA，只查标记和长度，不足以承载新付费管线预算/来源核验。
- `state/article_manifest.json`、`published_urls.json`、`vehicle_database.json`、`guide_database.json`：213历史记录、120 URL条目；published_urls 的名称不证明已经上线，条目含 published=false。

对全部相关 JSON/Markdown建立结构索引（2458结构记录及正文路径/哈希）。这不是对全站内容或历史每一句事实的重新审稿。旧数据缺少统一的语义意图字段；真实新选题仍须独立语义去重。没有修复旧文章。

## 推送前 Actions 副作用审计

|现有文件|触发|写入/副作用|本轮处理|
|---|---|---|---|
|`.github/workflows/import-history.yml`|push `.migration/PROCESS`|contents:write；迁移文章、CURRENT；commit/push|文件和触发路径均不改，不 dispatch|
|`.github/workflows/import-history-v2.yml`|push `.migration/PROCESS2`|contents:write；覆盖迁移版本、CURRENT；commit/push|文件和触发路径均不改，不 dispatch|
|`.github/workflows/run-pipeline.yml`|workflow_dispatch + 旧 schedule|运行旧 QA，上传 artifact|不改、不启用、不触发|

现有文件中没有 pull_request / pull_request_target / workflow_run 触发。已读取最近5次运行：均为 main 基线的 schedule/success；这不证明网站已发布。GitHub connector 不支持 actions/workflows 列表端点（400），完整工作流清点依据未截断的 Git tree、三份文件全文和运行列表完成。未检查无权访问的仓库外 webhook。

新文件 `.github/workflows/cloud-pilot-mock.yml` 仅 workflow_dispatch，contents:read，无 secrets、schedule、push、PR触发，checkout不持久化凭据，隔离分支条件，5分钟超时。它在默认分支尚不存在，因此不能声称已在 GitHub Actions 上运行。本轮真实测试在 Work Cloud shell 完成。

未发现实际 AWS/S3/CloudFront 部署程序、站点运行配置、robots/sitemap 配置文件；仓库主要是内容与交接。文章/报告提及的线上状态不是生产配置。两个实际网站均未访问或修改。

所有原有4874文件逐个重新计算 Git blob SHA。新增路径限制在 `cloud_pilot/` 与上述一个新 workflow。发布前再次 GET main；漂移则停下重新判断。新建分支先指向已存在 baseline，再更新到仅含新增隔离文件的提交，避免以历史迁移文件作为新提交触发范围。
